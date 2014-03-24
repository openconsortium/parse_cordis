# from distutils.core import setup
from setuptools import setup

setup(
    name='parse_cordis',
    # version='0.1.0',
    author='Peter Vanhee',
    author_email='peter@marzeelabs.org',
    packages=['parse_cordis'],
    url='https://github.com/openconsortium/parse_cordis',
    # license='LICENSE.txt',
    description='Useful EU Cordis scrapers.',
    long_description=open('README.md').read(),
    install_requires=[
        "beautifulsoup4 >= 4.3.2",
        "htmllaundry >= 2.0",
        "lxml >= 3.2.3",
    ],
    scripts=['bin/parse_project', 'bin/parse_listing', 'bin/parse_listing_new'],
)