#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK


# Get the location where this script is being run
import sys, os
scriptpath = os.path.dirname(os.path.realpath(__file__))
basepath   = os.path.dirname(scriptpath)

import re
import shutil
import argparse
import subprocess
from urllib.parse import urlparse

try:
    import argcomplete
    has_argcomplete = True
except:
    has_argcomplete = False

# Get YAML modules
import ruamel.yaml    
yaml = ruamel.yaml.YAML(typ='rt')
Loader= yaml.load
loaderkwargs = {}
dumperkwargs = {}

validexts = ['.html', '.md', '.ipynb', '.png', '.jpg', '.rst', ]

def is_valid_url(url_string):
    try:
        result = urlparse(url_string)
        return all([result.scheme, result.netloc])
    except:
        return False
    
def is_anchor(fstring, anchorstr='#'):
    if fstring.strip()[0] == anchorstr:
        return True
    else:
        return False

def is_valid_filetype(fname, validfiles):
    extension = os.path.splitext(fname)[1]
    if extension.lower() in validfiles:
        return True
    else:
        return False
    
# From: https://stackoverflow.com/questions/63197371/detecting-all-links-in-markdown-files-in-python-and-replace-them-with-outputs-of
def find_md_links(md):
    """Returns dict of links in markdown:
    'regular': [foo](some.url)
    'footnotes': [foo][3]
    
    [3]: some.url
    """
    # https://stackoverflow.com/a/30738268/2755116

    INLINE_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    FOOTNOTE_LINK_TEXT_RE = re.compile(r'\[([^\]]+)\]\[(\d+)\]')
    FOOTNOTE_LINK_URL_RE = re.compile(r'\[(\d+)\]:\s+(\S+)')

    links = list(INLINE_LINK_RE.findall(md))
    footnote_links = dict(FOOTNOTE_LINK_TEXT_RE.findall(md))
    footnote_urls = dict(FOOTNOTE_LINK_URL_RE.findall(md))

    footnotes_linking = []
        
    for key in footnote_links.keys():
        footnotes_linking.append((footnote_links[key], footnote_urls[footnote_links[key]]))

    return {'regular': links, 'footnotes': footnotes_linking}

def getyamlnode(ydict, key, required=False, default=None):
    if key in ydict:
        return ydict[key]
    elif required:
        print("ERROR: Required key %s not found"%key)
        sys.exit(1)
    else:
        return default
    

def process_yamlfile(yamlfile, dryrun=False, verbose=False, debug=False):
    """
    """
    with open(yamlfile, 'r') as f:
        yamldict = Loader(f, **loaderkwargs)

        destdir    = getyamlnode(yamldict, 'destdir', required=True)
        mdfiles    = getyamlnode(yamldict, 'mdfiles', required=True)
        validtypes = getyamlnode(yamldict, 'validtypes', required=False,
                                 default=validexts)
        
        for mdf in mdfiles:
            basedir   = os.path.dirname(mdf)
            # Copy the first markdown
            copytodir=os.path.join(destdir, basedir)
            print(mdf+" --> "+copytodir)
            if not os.path.exists(copytodir):
                # Create the directory
                os.makedirs(copytodir)
            if not dryrun:
                shutil.copy2(mdf, copytodir)
            
            # Then parse the links
            with open(mdf, 'r') as file:
                file_content = file.read()
                print(mdf)
                print('---')
                mdlinks = find_md_links(file_content)
                for l in mdlinks['regular']:
                    link = l[1]
                    abslink = os.path.join(basedir, link)
                    checklist = [is_valid_url(link),          # Check if link is a url
                                 is_anchor(link),             # Check if link is an anchor
                                 not os.path.exists(abslink), # Check if the file does not exist
                                 os.path.isdir(abslink),      # Check if the link is a directory
                                 not is_valid_filetype(link, validtypes)  # Check if the file has the right extension
                                 ]

                    if debug: print('%-40s '%link+'\t'+repr(checklist))
                    if not any(checklist):
                        # Copy the file
                        copytodir=os.path.join(destdir, basedir, os.path.dirname(link))
                        print(abslink+" --> "+copytodir)
                        if not os.path.exists(copytodir):
                            # Create the directory
                            os.makedirs(copytodir)
                        if not dryrun:
                            shutil.copy2(abslink, copytodir)
                    # write out error messages
                    if verbose and any(checklist):
                        if os.path.exists(abslink) and (not is_valid_filetype(link, validtypes)):
                            print("WARNING: "+abslink + " is not valid filetype")
                        if os.path.isdir(abslink):
                            print("WARNING: "+abslink + " is a directory")
            print()
            
    return

# ========================================================================
#
# Main
#
# ========================================================================
if __name__ == "__main__":
    helpstring = """
    Deploy a markdown page to sphinx website
    """

    exampleyaml = """
# Deploy a page to a website
destdir:  ../.website_src/

# Define the valid file types to copy over (optional)
validtypes: ['.html', '.md', '.ipynb', '.png', '.jpg', '.rst', ]
    
# Markdown files process
mdfiles:
    - README.md
    - setup/README.md
"""
    
    # Handle arguments
    parser     = argparse.ArgumentParser(description=helpstring,
                                         formatter_class=argparse.RawDescriptionHelpFormatter,)
    parser.add_argument('--example', 
                        help="Provide an example of an yaml file",
                        default=False,
                        action='store_true',
                        required=False)
    parser.add_argument('--dryrun', 
                        help="Do a dry run, don't copy over any files",
                        default=False,
                        action='store_true',
                        required=False)
    parser.add_argument('--verbose', 
                        help="Verbose output",
                        default=False,
                        action='store_true',
                        required=False)
    parser.add_argument('--debug', 
                        help="Print out debug information",
                        default=False,
                        action='store_true',
                        required=False)
    parser.add_argument("--extrapaths",
                        nargs='+',
                        type=str,
                        help="Extra paths to include for modules")
    parser.add_argument(
        "inputfile",
        help="input YAML file",
        nargs='*',
        type=str,
    )

    # Load the options
    if has_argcomplete: argcomplete.autocomplete(parser)
    args      = parser.parse_args()
    inputfile = args.inputfile
    example   = args.example
    dryrun    = args.dryrun
    verbose   = args.verbose
    debug     = args.debug
    extrapaths= args.extrapaths
    
    if example:
        print(exampleyaml)
        sys.exit(0)

    # Add extra paths to the system path
    if extrapaths is not None:
        for x in extrapaths: sys.path.insert(1, x)

    # Load the input file
    yamldict = {}
    for yamlfile in inputfile:
        if os.path.exists(yamlfile):
            process_yamlfile(yamlfile, dryrun=dryrun, verbose=verbose, debug=debug)
        else:
            print('%s not found'%yamlfile)

