#!/usr/bin/env python
from sys import stdin, stderr, stdout, argv, exit
import argparse
import subprocess
import os
import platform
from converter import write
from blueprint import blueprint2json,fetch_blueprint

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def readInput():
    content = ""
    for line in stdin:
        content += line

    return content

def check_drafter():
    try: 
        assert subprocess.check_output(['drafter', '-v']).startswith('v0.1')
    except: 
        print >> stderr, ''
        print >> stderr, bcolors.BOLD +'Please install Drafter < v2' + bcolors.ENDC
        print >> stderr, 'Drafter is used to convert Blueprint API to JSON. The preferred version is v0.1.9.'
        print >> stderr, 'Drafter v2 changed the JSON output format to be incomptabile with apiary2postman.'
        print >> stderr, 'Feel free to submit a pull request at GitHub which fixes this at https://github.com/thecopy/apiary2postman'
        print >> stderr, ''
        print >> stderr, 'By using ' + bcolors.BOLD + 'brew:' + bcolors.ENDC
        print >> stderr, '\tbrew install --HEAD https://raw.githubusercontent.com/apiaryio/drafter/b3dce8dda5d48b36e963abeffe5b0de7afecac3d/tools/homebrew/drafter.rb'
        print >> stderr, ''
        print >> stderr, 'By ' + bcolors.BOLD + 'source:' + bcolors.ENDC
        print >> stderr, '\tgit clone https://github.com/apiaryio/drafter'
        print >> stderr, '\tcd drafter'
        print >> stderr, '\tgit checkout b3dce8d ' + bcolors.HEADER + '# This is the commit for release 0.1.9' + bcolors.ENDC
        print >> stderr, '\t./configure'
        print >> stderr, '\tmake'
        print >> stderr, '\tsudo make install'
        exit(3)

def main():

    parser = argparse.ArgumentParser(description='Generate Postman collections from Apiary API/Blueprint', formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Examples:\n\t' + argv[0] + ' --pretty api awattgarde\n\t' 
            + argv[0] + ' --only-collection --output awattgarde_collection.postman api awattgarde\n\t'
            + argv[0] + ' --only-collection json blueprint.json\n\t'
            +'cat blueprint.json | ' + argv[0] + ' json > awattgarde_collection.postman\n\t'  )


    subparsers = parser.add_subparsers(help='',title='subcommands', 
                                   description='valid subcommands')

    parser_blueprint = subparsers.add_parser('blueprint', description='blueprint: Read Blueprint API markup, then convert it using drafter, then generate Postman collection JSON.',
        help='Read Blueprint API markup, then convert it using drafter, then generate Postman collection JSON. Use "blueprint -h" for more help.')

    parser_json = subparsers.add_parser('json', description='json: Use prepared JSON to generate the Postman collection.',help='Use prepared JSON. Use "json -h" for more help.')
    
    parser_api = subparsers.add_parser('api', description='api: Use the Apiary API to fetch the Blueprint markup, then convert it using drafter, then generate Postman collection JSON.',
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
        check_drafter()
        input = blueprint2json(args.blueprint_input.read())
    else:
        # API mode
        check_drafter()

        apikey = None
        if args.key != None:
          apikey = args.key
        else:
            apikey = os.environ.get('APIARY_API_KEY')

        if apikey == None:
            print 'Please provide an api-key or set APIARY_API_KEY'
            exit(4)

        blueprint = fetch_blueprint(args.name[0], apikey)
        input = blueprint2json(blueprint)
        
    output = args.output    
    if args.output != stdout:
        output = output[0]

    write(input, output, args.only_collection, args.pretty)

if  __name__ =='__main__':
    main()

