#!/usr/bin/env python
import setuptools
from setuptools import setup, find_packages
from distutils.core import setup

VERSION = "1.0"

setup(
    name = "wsgi-seo-js",
    version = VERSION,
    author = 'Alan Justino da Silva',
    author_email = 'alan.justino@yahoo.com.br',
    url = 'http://github.com/alanjds/wsgi-seo-js',
    #download_url = 'https://github.com/alanjds/wsgi-seo-js/tarball/'+VERSION,
    install_requires = [
        'werkzeug',
        'selenium',
    ],
    tests_require = [],
    test_suite = 'tests.suite',
    description = "WSGI middleware that implements Google's Ajax Crawling specs",
    packages = find_packages(),
    include_package_data = True,
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)
