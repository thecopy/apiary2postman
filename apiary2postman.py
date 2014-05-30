#!/usr/bin/env python
from sys import stdin, stdout, argv, exit
import argparse
import subprocess
import os
from converter import write
from apiary import blueprint2json,fetch_blueprint
def readInput():
    content = ""
    for line in stdin:
        content += line

    return content

def check_snowcrash():
    try: 
        subprocess.check_output(['which', 'snowcrash'])
    except: 
        print 'Please install snowcrash:'
        print ''
        print 'By using brew:'
        print '\tbrew install --HEAD https://raw.github.com/apiaryio/snowcrash/master/tools/homebrew/snowcrash.rb'
        print ''
        print 'By source, see:'
        print '\thttps://github.com/apiaryio/snowcrash#build'
        exit(3)

def main():

    parser = argparse.ArgumentParser(description='Generate Postman collections from Apiary API/Blueprint', formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Examples:\n\t' + argv[0] + ' --pretty api awattgarde\n\t' 
            + argv[0] + ' --only-collection --output awattgarde_collection.postman api awattgarde\n\t'
            + argv[0] + ' --only-collection json blueprint.json\n\t'
            +'cat blueprint.json | ' + argv[0] + ' json > awattgarde_collection.postman\n\t'  )


    subparsers = parser.add_subparsers(help='',title='subcommands', 
                                   description='valid subcommands')

    parser_blueprint = subparsers.add_parser('blueprint', description='blueprint: Read Blueprint API markup, then convert it using snowcrash, then generate Postman collection JSON.',
        help='Read Blueprint API markup, then convert it using snowcrash, then generate Postman collection JSON. Use "blueprint -h" for more help.')

    parser_json = subparsers.add_parser('json', description='json: Use prepared JSON to generate the Postman collection.',help='Use prepared JSON. Use "json -h" for more help.')
    
    parser_api = subparsers.add_parser('api', description='api: Use the Apiary API to fetch the Blueprint markup, then convert it using snowcrash, then generate Postman collection JSON.',
        help='Use the Apiary API to fetch the JSON. Use "api -h" for more help.')

    parser.add_argument('--pretty', dest='pretty', action='store_true', default=False,
                        help='generate pretty JSON')
    parser.add_argument('--only-collection', dest='only_collection', action='store_const', 
                        const=True, default=False,
                        help='generate Postman JSON for the first collection only.')
    parser_api.add_argument('key', metavar='api-key', nargs='?',
                        help='the Apiary API token. If not supplied APIARY_API_KEY environment variable is used.') 
    parser_api.add_argument('name', metavar='api-name', nargs=1,
                        help='the name of the api on apiary. I.e. testapi311 for http://docs.testapi311.apiary.io/') 
    parser_json.add_argument('input', metavar='input', type=file, nargs='?', default=stdin,
                        help='input file, formatted as JSON. If not supplied, stdin is used.') 
    parser_blueprint.add_argument('blueprint_input', metavar='input', type=file, nargs='?', default=stdin,
                        help='input file, formatted as Blueprint API Markup. If not supplied, stdin is used.') 
    parser.add_argument('--output', metavar='output', type=argparse.FileType('w'), nargs=1, default=stdout,
                        help='output file. Outputs Postman collection JSON. If not supplied, stdout is used.')

    args = parser.parse_args()

    input = ''
    if hasattr(args, 'input'):
        # JSON mode
        input = args.input.read()
    elif hasattr(args, 'blueprint_input'):
        # blueprint mode
        input = blueprint2json(args.blueprint_input.read())
    else:
        # API mode
        check_snowcrash()

        apikey = None
        if args.key != None:
            apikey = args.key[0]
        else:
            apikey = os.environ.get('APIARY_API_KEY')

        if apikey == None:
            print 'Please provide an api-key or set APIARY_API_KEY'
            exit(4)

        blueprint = fetch_blueprint(args.name[0], apikey)
        input = blueprint2json(blueprint)

    write(input, args.output, args.only_collection, args.pretty)

if  __name__ =='__main__':
    main()

