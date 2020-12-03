from odoo import fields, api, models

class ms_reason_cancel_wizard(models.TransientModel):
    _name = "ms.reason.cancel.wizard"
    _description = "Reason Cancel"
    
    name = fields.Text(string="Reason", required=True)
    
    @api.one
    def action_cancel(self):
        active_ids = self._context.get('active_ids')
        if not active_ids :
            return False
        pemeriksaan_id = self.env['ms.pemeriksaan'].browse(active_ids[:1])
        pemeriksaan_id.pendaftaran_id.note += self.name
        pemeriksaan_id.state = 'cancel'
