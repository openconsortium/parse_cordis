# Parse Cordis
**Python package to easily scrape EU's Cordis pages on European science projects**

## Installation

`parse_cordis` can be installed using [Pip](http://pip.readthedocs.org/en/latest/index.html)

    pip install -e git+git://github.com/openconsortium/parse_cordis.git#egg=parse_cordis

## Shell scripts

Handy shell scripts are provided in `bin/` to run parsing independently.

Returns all information about the project with RCN 105875 from the Cordis database in a nested dictionary structure.

    sh project.parse(105875)

## Credits
 
* http://openconsortium.eu
* Development by @pvhee from @marzeelabs, http://marzeelabs.org
