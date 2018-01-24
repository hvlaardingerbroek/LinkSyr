#!/usr/bin/python3
"""Read the SEDRA database

The files of the SEDRA database have been are no longer
available from bethmardutho.org, but a copy is available
in the sedrajs project of Greg Borota on github.com/peshitta.
It contains the following files:
SEDRA3.DOC      - documentation of the database
ROOTS.TXT       - roots records
LEXEMES.TXT     - lexemes records
WORDS.TXT       - words records
ENGLISH.TXT     - english translations records
ETIMOLGY.TXT    - etymology records

BFBS.README.TXT - documentation of the NT text
BFBS.TXT        - the NT text

The BFBS files contain, according to the README file,
   BFBSREC.TXT  - The text of the Syriac New Testament according to the
                  British and Foreign Bible Society's Edition
   FEATURRE.TXT - A list of all the words in BFBSREC.TXT with morphological
                  information.

Although the filenames differ, besides other minor inconsistencies,
the description seems to apply roughly to BFBS.TXT.
"""
from __future__ import print_function
import os
from constants import SedraIII as c

config_filename = 'linksyr.conf'
config_section = 'sedra'
config_fields = ('datadir',
              'roots',
              'lexemes',
              'words',
              'english',
              'etymology',
              'nt')

# Read database location from config file
try: # allow for different module names in python 2 and 3
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
config = ConfigParser()
config.read(config_filename)
config_items = dict(config.items(config_section))

DB_DIR = config_items[config_fields[0]]
DB_FILES = tuple(config_items[s] for s in config_fields[1:6])
NT_FILE = config_items[config_fields[6]]

def main():
    pass

def usage():
    print(__doc__)

if __name__ == "__main__":
        main()
