import os


conf = {
	'secret': os.urandom(12).hex(),
	'debug': True,
	'template folder': './frontend/templates',
	'static folder': './frontend/static',
	'run with torch': True
}