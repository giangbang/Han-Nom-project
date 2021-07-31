import os


conf = {
	'secret': os.urandom(12).hex(),
	'debug': True,
	'template folder': './frontend'
}