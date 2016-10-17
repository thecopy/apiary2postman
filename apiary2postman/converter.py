import json
from sys import stdout
from uuid import uuid4
from time import time

def _buildCollectionResponse(apiary, single_collection):
	environment = createEnvironment(apiary)

	# Create the collection
	collections = parseResourceGroups(
		apiary,
		environment['values'], 
		True,
		single_collection)

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

def _buildFullResponse(apiary, single_collection):
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
		apiary, 
		result['environments'][0]['values'], 
		False,
		single_collection)

	return result

def _createCollection(name, description):
	collection = dict()
	collection['id'] = str(uuid4());
	collection['folders'] = []
	collection['requests'] = []
	collection['name'] = name
	collection['description'] = description
	collection['timestamp'] = int(time())
	collection['synced'] = False
	collection['remote_id'] = 0
	collection['order'] = []
	return collection

def _createFolder(name, description, collection):
	folder = dict()
	folder['id'] = str(uuid4())
	folder['name'] = name
	folder['description'] = description
	folder['order'] = []
	folder['collection_id'] = collection['id']
	folder['collection_name'] = collection['name']	
	return folder

def write(json_data, out=stdout, only_collection=False, pretty=False, single_collection=False):
	json_obj = json.loads(json_data)

	if only_collection:
		result_out = _buildCollectionResponse(json_obj, single_collection)
	else:
		result_out = _buildFullResponse(json_obj, single_collection)

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

def parseResourceGroups(apiary, environment_vals, only_collection, single_collection):
	out = []

	if single_collection:		
		# Create THE collection
		collection = _createCollection(apiary['name'], apiary['description'])
		# Add collection to output
		out.append(collection)

	for resourceGroup in apiary['resourceGroups']:
		if single_collection is False:
			# Create collection per resource group
			collection = _createCollection(resourceGroup['name'], resourceGroup['description'])
			# Add collection to output
			out.append(collection)
		else:
			# Create folder per resource group
			folder = _createFolder(resourceGroup['name'], resourceGroup['description'], collection)
			# Add folder json to collection
			collection['folders'].append( folder )

		for resource in resourceGroup['resources']:	
			if single_collection is False:
				# Create folder per resource
				folder = _createFolder(resource['name'], resource['description'], collection)	
				# Add folder json to collection
				collection['folders'].append( folder )
		
			sub_url = resource['uriTemplate']
			for action in resource['actions']:
				request = dict()
				request['id'] = str(uuid4())
				request['folder'] = folder['id']
				request['version'] = 2
				request['name'] = action['name']
				if single_collection is True:
					# Add resource as prefix
					request['name'] = resource['name'] + ": " + request['name']
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
		
	return out
