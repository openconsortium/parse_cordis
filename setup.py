from distutils.core import setup

setup(
    name='parse_cordis',
    version='0.1.0',
    author='Peter Vanhee',
    author_email='peter@marzeelabs.org',
    packages=['parse_cordis'],
    url='https://github.com/pvhee/parse_cordis',
    # license='LICENSE.txt',
    description='Useful Cordis scrapers.',
    long_description=open('README.md').read(),
    install_requires=[
        "beautifulsoup4 >= 4.3.2",
        "htmllaundry >= 2.0",
    ],
)