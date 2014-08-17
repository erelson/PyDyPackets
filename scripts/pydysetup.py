"""Script copies template files to the current directory.

If HTML documentation has been generated, updates some copied files with links
to the corresponding documentation. (This doesn't work if MARMOT was installed
via setup.py and this script is invoked via `pydysetup`)
"""

import os
import fileinput
from shutil import copy2, copyfile, copytree, ignore_patterns


def _copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if not os.path.isdir(d):
                copytree(s, d, symlinks, ignore)
        else:
            copy2(s, d)

def main():
    # TODO: verify that this works when proper installation has been set up.
    #pydypath = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
    pydyscriptspath = os.path.split(os.path.abspath(__file__))[0]

    # Determine paths
    templatepath = os.path.join(pydyscriptspath, "resources", "templates")
    thisdir = os.path.abspath(os.curdir)

    # Make needed directories
    #if not os.path.isdir('examples'):
    #    os.mkdir('examples')

    # Copy files
    copyfile(os.path.join(templatepath, "config_example.cfg"),
            os.path.join(thisdir, "pydypackets.cfg"))

    #_copytree(examplespath, thisdir, ignore=ignore_patterns('.git', '*~'))

    # Add link to html documentation for config file if such exists
    # Doesn't currently work for installed package approach. Needs a re-do.
    if os.path.isfile(
            os.path.join(
                pydyscriptspath, "doc", "build", "html", "configGuide.html")):

        for cnt, line in enumerate(fileinput.input(os.path.join(
                thisdir, "config.cfg"), inplace=True)):
            if cnt == 1:
                print "# For instructions and full documentation, " \
                        "see the user manual:\n",
                line = "# file://" + os.path.join(pydyscriptspath, "doc", "build", "html", "configGuide.html") + "\n"

            # Replace the modified line back in the file; the comma is essential
            print line,
        print ''
