from odoo import api, fields, models
from datetime import datetime

class ms_pemeriksaan(models.Model):
    _name = "ms.pemeriksaan"
    _description = "Pemeriksaan"
    _order = "name desc"
    
    @api.one
    @api.depends('pasien_id')
    def _get_usia(self):
        usia = False
        if self.pasien_id :
            usia = datetime.now().year - datetime.strptime(self.pasien_id.tgl_lahir , '%Y-%m-%d').year
        self.usia = usia

    name = fields.Char(string='Pemeriksaan', default='/')
    state = fields.Selection([
         ('draft','Draft'),
         ('confirm','Confirmed'),
         ('cancel','Cancelled')
    ], string='State', default='draft')
    pendaftaran_id = fields.Many2one('ms.pendaftaran', 'Pendaftaran')
    tanggal = fields.Datetime(string='Tanggal', default=fields.Datetime.now())
    pasien_id = fields.Many2one(related='pendaftaran_id.pasien_id', string='Pasien')
    jenis_kelamin = fields.Selection(related='pendaftaran_id.pasien_id.jenis_kelamin', string='Jenis Kelamin')
    usia = fields.Integer(compute='_get_usia', string='Usia')
    poli_id = fields.Many2one(related='pendaftaran_id.poli_id', string='Poli')
    dokter_id = fields.Many2one('res.partner', string='Dokter')
    keluhan = fields.Text(string='Keluhan')
    hasil = fields.Text(string='Hasil Pemeriksaan')
    tindakan = fields.Text(string='Tindakan Pengobatan')
    resep_line = fields.One2many('ms.resep.obat', 'pemeriksaan_id', 'Resep Obat')
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get_sequence('Pemeriksaan','ms.pemeriksaan','PMR/%(y)s/',5)
        return super(ms_pemeriksaan, self).create(vals)
    
    @api.multi
    def action_confirm(self):
        for me_id in self :
            if me_id.state == 'draft':
                inv_line_vals = []
                for line in me_id.resep_line :
                    inv_line_vals.append((0,0,{
                        'product_id': line.product_id.id,
                        'name': line.product_id.name_get()[0][1],
                        'quantity': line.qty,
                        'price_unit': line.product_id.lst_price,
                        'account_id': me_id.pasien_id.property_account_payable_id.id,
                    }))
                self.env['account.invoice'].create({
                    'partner_id': me_id.pasien_id.id,
                    'invoice_line_ids': inv_line_vals,
                })
                me_id.write({'state':'confirm'})
    
    @api.multi
    def action_cancel(self):
        view_id = self.env.ref('ms_puskesmas.view_ms_reason_cancel_wizard')
        return {
            'name': 'Reason Cancel',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'ms.reason.cancel.wizard',
            'views': [(view_id.id, 'form')],
            'view_id': view_id.id,
            'target': 'new',
        }
    
    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != 'draft' :
                raise Warning("Tidak bisa menghapus data pendaftaran yang bukan draft !")
        return super(ms_pemeriksaan, self).unlink()
    
class ms_resep_obat(models.Model):
    _name = "ms.resep.obat"
    _description = "Resep Obat"
    _rec_name = "product_id"
    
    pemeriksaan_id = fields.Many2one('ms.pemeriksaan', 'Pemeriksaan')
    product_id = fields.Many2one('product.product', 'Obat', required="1")
    aturan_minum = fields.Char('Aturan Minum')
    waktu_minum = fields.Selection([
         ('sebelum','Sebelum'),
         ('sesudah','Sesudah'),
    ], 'Sebelum/Sesudah Makan', default='sesudah')
    qty = fields.Float('Quantity')
    satuan_id = fields.Many2one('product.uom', 'Satuan')
    
    @api.onchange('product_id')
    def change_product(self):
        if self.product_id :
            self.satuan_id = self.product_id.uom_id.id
    