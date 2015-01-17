import os
import sys

# Set this to match InkLevel application directory
APP_DIRECTORY = 'SET_THIS_TO_APP_DIRECTORY'
#APP_DIRECTORY = '/home/mc/python-www-apps/hp-info'

# For testing purposes set as 2 item touple that contains app with argument to be
# executed in subprocess
TESTING_COMMAND = ()

# Proper app
def info_app(environ, start_response):
	import json
	import InkLevelHttpConfig

	try:
		f = InkLevelHttpConfig.getCacheFileForRead()
		output = f.read()
	except IOError, io:
		output = '{"error": "Internal error. No cached file!"}'

	status = '200 OK'
	headers = [('Content-type', 'application/json'),
                  ('Content-Length', str(len(output)))]

	start_response(status, headers)
	yield output


# Error handling application
def error_app(environ, start_response):
	output = 'Application directory need to be set for a successful run!'
	status = '200 OK'
	headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]

	start_response(status, headers)
	yield output

if (APP_DIRECTORY != 'SET_THIS_TO_APP_DIRECTORY'):
	if APP_DIRECTORY not in sys.path:
		sys.path.append(APP_DIRECTORY)
	os.chdir(APP_DIRECTORY)
	application = info_app
else:
	application = error_app

