apiary2postman
==============

Tool for generating a Postman collection from the Apiary API, or Blueprint JSON

# Usage

To generate a total environment dump:

    apiary2postman.py api my_api > postman.dump

Or to generate only a collection:

    apiary2postman.py --only-collection api my_api > postman.collection
    
    
# Prerequisites

[Snowcrash](https://github.com/apiaryio/snowcrash#install]) is required.

To install on OS X:

    brew install --HEAD https://raw.github.com/apiaryio/snowcrash/master/tools/homebrew/snowcrash.rb
    
