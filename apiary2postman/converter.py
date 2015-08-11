import json
from sys import stdout
from uuid import uuid4
from time import time

def _buildCollectionResponse(apiary):
	environment = createEnvironment(apiary)

	# Create the collection
	collections = parseResourceGroups(
		apiary['resourceGroups'], 
		environment['values'], 
		True)

	result = {
		'id' : str(uuid4()),
		'name' : apiary['name'],
		'description' : apiary['description'],
	  'timestamp' : int(time()),
	  'remote_id' : 0,
	  'synced' : False,
	  'order' : [],
	  'folders' : [],
	  'requests' : [],
	}

	for collection in collections:
		result['id'] = collection['id']
		result['folders'] += collection['folders']
		result['requests'] += collection['requests']

	return result

def _buildFullResponse(apiary):
	# Create the Environment
	environment = createEnvironment(apiary)

	# Create the Header
	result = {
		'version' : 1,
		'globals' : [],
		'headerPresets' : [],
		'environments' : [ environment ],
	}

	# Create the collection
	result['collections'] = parseResourceGroups(
		apiary['resourceGroups'], 
		result['environments'][0]['values'], 
		False)

	return result

def write(json_data, out=stdout, only_collection=False, pretty=False):
	json_obj = json.loads(json_data)

	if only_collection:
		result_out = _buildCollectionResponse(json_obj)
	else:
		result_out = _buildFullResponse(json_obj)

	if pretty:
		json.dump(result_out, out, indent=2, separators=(',', ': '))
	else:
		json.dump(result_out, out)


def createEnvironment(json_obj):
	environment = dict()
	environment['id'] = str(uuid4())
	environment['name'] = json_obj['name']
	environment['timestamp'] = int(time())
	environment['synced'] = False
	environment['syncedFilename'] = ''
	environment['values'] = []

	
	for metadata in json_obj['metadata']:
		if metadata['name'] == "FORMAT":
			continue

		value = dict()
		value['name'] = metadata['name']
		value['key'] = metadata['name']
		value['value'] = metadata['value']
		value['type'] = 'text'
		environment['values'].append(value)

	return environment

def parseResourceGroups(resourceGroups, environment_vals, only_collection):
	out = []
	for resourceGroup in resourceGroups:
		collection = dict()
		collection['id'] = str(uuid4());
		collection['folders'] = []
		collection['requests'] = []
		collection['name'] = resourceGroup['name']
		collection['description'] = resourceGroup['description']
		collection['timestamp'] = int(time())
		collection['synced'] = False
		collection['remote_id'] = 0
		collection['order'] = []

		for resource in resourceGroup['resources']:		
			folder = dict()
			folder['id'] = str(uuid4())
			folder['name'] = resource['name']
			folder['description'] = resource['description']
			folder['order'] = []
			folder['collection_id'] = collection['id']
			folder['collection_name'] = collection['name']	
		
			sub_url = resource['uriTemplate']
			for action in resource['actions']:
				request = dict()
				request['id'] = str(uuid4())
				request['folder'] = folder['id']
				request['version'] = 2
				request['name'] = action['name']
				request['description'] = action['description']
				request['descriptionFormat'] = 'html'
				request['method'] = action['method']

				request['url'] = "{{HOST}}"+sub_url
				if only_collection:
					for value in environment_vals:
						if value['name'] == 'HOST':
							request['url'] = value['value'] + sub_url

				request['dataMode'] = 'params'
				request['data'] = []

				# Unsupported data				
				request['pathVariables'] = dict()
				request['tests'] = ''
				request['time'] = int(time())
				request['responses'] = []
				request['synced'] = False

				for parameter in resource['parameters']:
					request['url'] = request['url'].replace('{'+ parameter['name'] +'}', parameter['example'])

				headers = []

				for example in action['examples']:
					# Add Headers
					for request_ex in example['requests']:
						for header in request_ex['headers']:
							headers.append(header['name'] + ": " + header['value'])

						if len(request_ex['body']) > 0:
							request['dataMode'] = 'raw'
							request['data'] = request_ex['body']

					# Add Accept header to request based on response model (hack?)
					for response in example['responses']:
						for header in response['headers']:
							if header['name'] != 'Content-Type':
								continue
							if 'Accept: ' + header['value'] not in headers:
								headers.append('Accept: ' + header['value'])
				request['headers'] = '\n'.join(headers)
				# Add reference to collection to this request
				# The collectionId field refers to the parent collection, not the folder
				request['collectionId'] = collection['id']
				# Add reference to the request to the current folder
				folder['order'].append( request['id'] )
				# Add request json to the collection
				collection['requests'].append(request)

			# Add folder json to collection
			collection['folders'].append( folder )
		out.append(collection)
	return out
