from urllib2 import Request, urlopen
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
import json

def fetch_blueprint(name, key):	
	request = Request("https://api.apiary.io/blueprint/get/" + name)
	request.add_header('authentication', 'Token ' + key)
	request.add_header('Accept', 'application/json')
	response_body = json.loads(urlopen(request).read())
	return response_body['code']

def blueprint2json(blueprint):
	t = NamedTemporaryFile()
	p = Popen(['snowcrash', '--format', 'json', '--output', t.name], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	p.communicate(blueprint)
	out = t.read()
	t.close()
	return out
	