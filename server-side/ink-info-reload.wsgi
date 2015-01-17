import os
import sys

# Set this to match InkLevel application directory
APP_DIRECTORY = 'SET_THIS_TO_APP_DIRECTORY'
#APP_DIRECTORY = '/home/mc/python-www-apps/hp-info'

# For testing purposes set as 2 item touple that contains app with argument to be
# executed in subprocess
TESTING_COMMAND = ()

# Proper app
def recreate_app(environ, start_response):
	import json
	import InkLevelHttpConfig
	import InkLevelHpInfoParser

	# Handle request
	if (len(TESTING_COMMAND) == 2):
		sys.argv = []
		sys.argv.append('mod_wsgi')
		sys.argv.append(TESTING_COMMAND[0])
		sys.argv.append(TESTING_COMMAND[1])

		output = InkLevelHpInfoParser.invoke(True)
	else:
		output = InkLevelHpInfoParser.invoke(False)

	# Cache if not an error
	if (json.loads(output).has_key("error") == False):
		    f = InkLevelHttpConfig.getCacheFileForWrite()
		    f.write(output)
		    f.close()

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
	application = recreate_app
else:
	application = error_app

