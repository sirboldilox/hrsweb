#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

def read(fname):
    """Returns a file as a string"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "WebRecords",
    version = "1.0",
    author = "Matt Parker",
    author_email='m.parker-12@student.lboro.ac.uk',
    description = ("Web front end to the health record system database"),
#    long_description = read("Readme.md"),

    license = "MIT",
    classifiers = [
        "Development Status :: 3 - Alpha"
        "Environment :: Web Environment",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux"
        "Topic :: System :: Networking :: Firewalls"
    ],

    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,

    install_requires=[
        'flask',
        'flask-restful',
        'requests'
    ],

    entry_points = {
        'console_scripts': ['webrecords=webrecords.__main__:cmd_entry']
    }

)
