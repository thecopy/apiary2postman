apiary2postman
==============

Tool for generating a Postman collection from the Apiary API, or Blueprint JSON

Supports

  * Blueprint API Markup
  * Blueprint API JSON from Drafter (Snowcrash)
  * Fetching Blueprint API Markup from Apiary API

    
# Prerequisites

[Drafter](https://github.com/apiaryio/drafter) is required if you want to use Blueprint API markup/Apiary API.

To install on OS X:

    brew install --HEAD https://raw.github.com/apiaryio/drafter/master/tools/homebrew/drafter.rb
  
# Installation

    pip install apiary2postman

# Usage

    apiary2postman json blueprint.json --output postman.json

##### If you have the Blueprint API markup, use the `blueprint` subcommand:

    apiary2postman blueprint some.blueprint > postman.dump
  
###### It is also possible to pipe everything:

    cat some.blueprint | apiary2postman blueprint > postman.dump

##### To generate a total Postman environment dump from Apiary API, use the `api` subcommand:
 
    apiary2postman api my_api > postman.dump

###### Or to generate only a Postman collection from Apiary API:

    apiary2postman --only-collection api my_api > postman.collection

It's also possible to specify the output file using the `--output`.

##### If you have the Blueprint JSON already generated, use the `json` subcommand:

    apiary2postman json some.json > postman.dump
    
###### It is also possible to pipe everything:

    cat some.json | apiary2postman json > postman.dump


