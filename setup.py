"""
Notes
-----
This setup.py should be used to install PyDyPackets (importable as pydypackets)
from the top level folder of this repo.

The function get_resources grabs all files in scripts/resources for copying
into the install directory for runtime access by PyDySetup(.py).

"""

import os
import glob
from setuptools import setup
import fnmatch

from distutils.command.install import INSTALL_SCHEMES

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


package_dir_dict = {'pydypackets': 'src/pydypackets',
                 #'pydypackets_app': 'apps/example',
                 'pydypackets_dontimport': 'scripts'}

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_resources(pkgdir, subdir='resources'):
    # save the current working directory, before changing to pkgdir
    wrkdir = os.path.abspath(os.curdir)
    os.chdir(os.path.join(os.path.split(__file__)[0], pkgdir))
    
    # iterate through all folders in resources and add full paths to match
    matches = []
    for root, dirnames, filenames in os.walk(os.path.join(os.curdir, subdir)):
        for filename in fnmatch.filter(filenames, '[!.]*.*[!~]'):
            # Note that saved path gets appended to, e.g. 'scripts/'
            # Also, combining scripts/ and ./resources/file
            # gives scripts/resources/file
            matches.append(os.path.join(root, filename))

    os.chdir(wrkdir)
    return matches


setup(
    name = "PyDyPackets",
    version = "0.1",
    author = "Eric Relson",
    author_email = "gertlex@gmail.com",
    description = ("A Python-based parser for Dynamixel communication packets."),
    #license = "BSD",
    #keywords = "example documentation tutorial",
    #url = "http://packages.python.org/an_example_pypi_project",

    packages=[
        'pydypackets',
        'pydypackets_dontimport',
        #'pydypackets_app'
        ],
    package_dir=package_dir_dict,

    package_data={'pydypackets_dontimport':
        get_resources(
            os.path.join(os.curdir,
            package_dir_dict['pydypackets_dontimport']))
        }, # won't work for files not within packages!
    include_package_data=True,

    # seems potentially messy
    #install_requires=['PIL', 'numpy', 'lxml', 'pykml', 'pyshp'],

    long_description=read('README.rst'),
    #classifiers=[
    #    "Development Status :: 3 - Alpha",
    #    "Topic :: Utilities",
    #    "License :: OSI Approved :: BSD License",
    #],

    # The below uses config-file-style plain text.
    entry_points="""
    [console_scripts]
    pydylogger = pydypackets_dontimport.pydylogger:main
    pydyparser = pydypackets_dontimport.pydyparser:main
    pydyplotter = pydypackets_dontimport.pydyplotter:main
    
    pydysetup = pydypackets_dontimport.pydysetup:main
    """,
    )

