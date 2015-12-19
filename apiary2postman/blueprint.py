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
	p = Popen(['drafter', '--format', 'json'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	out, err = p.communicate(blueprint.encode('utf8'))
	return out
	