{
	"name": "Data Kelurahan, Kecamatan, Propinsi Indonesia",
	"version": "1.0", 
	"depends": [
		"base",
	],
	"category": "Sales",
	"description": """\

this module provide kecamatan, kelurahan, and state data for indonesian

""",
	"data": [
		#"data/res.country.state.csv",
		"data/vit.kota.csv",
		"data/vit.kecamatan.csv",
		"data/vit.kelurahan.csv",
		"view/kelurahan.xml",
		"view/kecamatan.xml",
		"view/kota.xml",
		"security/ir.model.access.csv",
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}