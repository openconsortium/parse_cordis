# Parse Cordis
**Python package to easily scrape EU's Cordis pages on European science projects**

Python scrapers for http://cordis.europa.eu/projects/, "The primary information source for EU-funded projects since 1990", converting XML/HTML into structured JSON.

The following python scripts are provided:

* `project_xml.py` parses information from a [single project](http://cordis.europa.eu/projects/rcn/105875_en.html) identified by a RCN (record control number) and returns a structured JSON.
* `listing.py` parses search results from a [project search](http://cordis.europa.eu/search/index.cfm?fuseaction=proj.advSearch), identified by a search key.

## Installation

`parse_cordis` can be installed using [Pip](http://pip.readthedocs.org/en/latest/index.html)

    pip install -e git+git://github.com/openconsortium/parse_cordis.git#egg=parse_cordis

If you'd like to install `parse_cordis` for testing, the recommended way is to do that using [Virtualenv](http://pypi.python.org/pypi/virtualenv).

A `virtualenv` tutorial can be found [here](http://iamzed.com/2009/05/07/a-primer-on-virtualenv/).

After you've setup the virtual environment, you can use pip to install `parse_cordis`.

## Usage via shell scripts

 
    bin/parse_project.py 105875

Returns all information about the project with RCN 105875 from the Cordis database in a nested dictionary structure.

## Usage via Python

In your python app, include `from parse_cordis import project_xml` and then use

    project_xml.parse(105875)

returns a JSON with project information for the project with RCN 105875, and

    listing.parse('A923E997C57FE5AA5CE5E35BD668A0D3', 10)

a list of 10 RCNs for the search identified by the given search key. You can get your own search key from http://cordis.europa.eu/search/index.cfm?fuseaction=proj.advSearch, and taking the value of the `q` in the URL.


## Tests

Tests are provided using [Nose](https://nose.readthedocs.org/en/latest/).

Run the tests independently with

    nosetests -v -s

Automated tests are run via Travis on each commit: https://travis-ci.org/openconsortium/parse_cordis

## Credits
 
* http://openconsortium.eu
* Development by @pvhee from @marzeelabs, http://marzeelabs.org
