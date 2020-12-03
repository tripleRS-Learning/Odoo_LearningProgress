{
    "name"          : "Tutorial Odoo Indonesia",
    "version"       : "1.0",
    "category"      : "New Module",
    "summary"       : "Belajar Membuat Addons",
    "description"   : """
        Pertama kali belajar membuat addons, di versi odoo 10, menggunakan studi kasus puskesmas, dari Tutorial Odoo Indonesia
    """,
    "depends"       : [
        "product",
        "account",
        "ms_base",
    ],
    "data"          : [
        "views/res_partner.xml",
        "views/ms_poli.xml",
        "views/ms_pendaftaran.xml",
        "views/ms_pemeriksaan.xml",
        "views/product_template.xml",
        "views/account_invoice.xml",
        "wizard/ms_reason_cancel_wizard.xml",
        "report/report_resepobat.xml",
        "security/ir.model.access.csv",
    ],
    "demo"          : [],
    "test"          : [],
    "images"        : [],
    "qweb"          : [],
    "css"           : [],
    "application"   : True,
    "installable"   : True,
    "auto_install"  : False,
}