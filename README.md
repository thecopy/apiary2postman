apiary2postman
==============

Tool for generating a Postman collection from the Apiary API, or Blueprint JSON

# Usage

##### If you have the Blueprint API markup, use the `blueprint` subcommand:

    apiary2postman.py blueprint some.blueprint > postman.dump
    
###### It is also possible to pipe everything:

    cat some.blueprint | apiary2postman.py blueprint > postman.dump

##### To generate a total Postman environment dump from Apiary API, use the `api` subcommand:
 
    apiary2postman.py api my_api > postman.dump

###### Or to generate only a Postman collection from Apiary API:

    apiary2postman.py --only-collection api my_api > postman.collection

It's also possible to specify the output file using the `--output`.

##### If you have the Blueprint JSON already generated, use the `json` subcommand:

    apiary2postman.py json some.json > postman.dump
    
###### It is also possible to pipe everything:

    cat some.json | apiary2postman.py json > postman.dump


    
# Prerequisites

[Snowcrash](https://github.com/apiaryio/snowcrash#install) is required.

To install on OS X:

    brew install --HEAD https://raw.github.com/apiaryio/snowcrash/master/tools/homebrew/snowcrash.rb
    
