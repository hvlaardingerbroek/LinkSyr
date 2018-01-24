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


class Root:
    def __init__(self, line):
        self.id = get_address(line[0])
        self.rt_str = line[1]
        self.sort_str = line[2]
        self.attr = int(line[3])

    @property
    def attributes(self):
        return split_bits(self.attr, (1, 2, 13), 16)

    @property
    def attr_values(self):
        return get_values(c.ROOTS_ATTR, self.attributes)


class Lexeme:
    def __init__(self, line):
        self.id = get_address(line[0])
        self.rt_id = get_address(line[1])
        self.lex_str = line[2]
        self.feat = int(line[3])
        self.attr = int(line[4])

    @property
    def features(self):
        return split_bits(self.feat, (4,2,2,2,3,3,3,3,3,3,4), 32)

    @property
    def feat_values(self):
        return get_values(c.LEXEMES_FEAT, self.features)

    @property
    def attributes(self):
        return split_bits(self._attr, (1,1,4,10), 16)

    @property
    def attr_values(self):
        return get_values(c.LEXEMES_ATTR, self.attributes)


class Word:
    def __init__(self, line):
        self.id = get_address(line[0])
        self.lex_id = get_address(line[1])
        self.cons_str = line[2]
        self.voc_str = line[3]
        self.feat = int(line[4])
        self.attr = int(line[5])

    @property
    def features(self):
        return split_bits(self.feat, (2,2,2,1,2,6,2,2,2,2,3,6), 32)

    @property
    def feat_values(self):
        return get_values(c.WORDS_FEAT, self.features)

    @property
    def attributes(self):
        return split_bits(self.attr, (1,4,1,1,9), 16)

    @property
    def attr_values(self):
        return get_values(c.WORDS_ATTR, self.attributes)


class English:
    def __init__(self, line):
        self.id = get_address(line[0])
        self.lex_id = get_address(line[1])
        self.meaning = line[2]
        self.before = line[3]
        self.after = line[4]
        self.comment = line[5]
        self.attr = int(line[6])
        self.ignore = int(line[7])

    @property
    def attributes(self):
        return split_bits(self._attr, (1,1,1,1,1,2,2,2,5), 16)


class Etymology:
    def __init__(self, line):
        self.id = get_address(line[0])    # Record address, e.g. 4:1
        self.lex_addr = get_address(line[1])    # Lexeme address (in LEXEMES.TXT), e.g. 1:1
        self.word_origin = line[2]              # Word Origin, e.g. "a\255h\256r"
        self.attr = int(line[3])

    @property
    def attributes(self):
        return split_bits(self.attr, (4,1,11), 16)

    @property
    def attr_values(self):
        return get_values(c.ETYMOLOGY_ATTR, self.attributes)


class NtWords:
    def __init__(self, line):
        # self._rec_addr = line[0]  # _rec_addr is not unique, so useless
        self.loc_id = line[1]      # _loc_id
        # self._word_addr = line[2]
        # word_addr is a crazy encoded decimal value of two combined
        # hexadecimal values, the first of which is always '02'
        # (the number of the WORDS.TXT file). So to retrieve
        # the word_id, we must convert word_addr to a hex string
        # of eight positions, and convert the rightmost six back
        # to decimal. The leftmost two will always be '02'.
        self.word_id = int('{:08x}'.format(int(line[2]))[2:], 16)
        self.attr = int(line[3])

    @property
    def location(self):
        groups = ((0,2), (2,4), (4,7), (7,9))
        return [self.loc_id[start:end] for start, end in groups]

    @property
    def attributes(self):
        return split_bits(self.attr, (16,), 16)

    @property
    def attr_bits(self):
        return '{0:016b}'.format(self.attr)


def get_address(a):
    return int(a.split(':')[1]) if a != 'NULL' else None

def split_bits(n, groups, bits=16):
    if n<0: n+=(1<<bits) # shift bits https://stackoverflow.com/a/20768199
    b = '{0:0{1}b}'.format(n, bits) # convert to binary
    result = []
    start = None
    for size in groups:
        end = start-size if start is not None else -size
        result.append(int(b[end:start], 2)) # convert slice back to int
        start = end
    return tuple(result)

def get_values(fields, values):
    """Returns a dict with field names and values

    Fields must be a set of the format:
        (('fieldname1', ('value1', value2, ...) | None),
         ('fieldname2', ('value1', value2, ...) | None, ... ))
    Values must be a set of integers with the same length,
    and every integer must correspond to the index of the
    intended value in the subset. So for the result
        ('fieldname1':'value2','fieldname2':'value1')
    in the example above, values must be a set with values:
        (1,0)
    If a field has None in stead of a value-set, the integer
    value is returned with the fieldname.
    """
    # dict comprehension to get  - simple example:
    # >>> a=(('field0',('val00','val01','val02')),('field1',None))
    # >>> b=b=(1,2)
    # >>> {l[0]:(l[1][n] if l[1] else n) for l, n in zip(a,b)}
    # {'field0': 'val01', 'field1': 2}
    return {l[0]:(l[1][n] if l[1] else n) for l, n in zip(fields, values)}

def read_db_file(db_dir, filename):
    from csv import reader
    with open(os.path.join(db_dir, filename), 'r') as f:
        for line in reader(f):
            yield line

# db = tuple(tuple(c(line) for line in read_db_file(DB_DIR, f)) for f,c in zip(DB_FILES, db_classes))
def read_db_files():
    db = []
    for f, c in zip(DB_FILES, (Root, Lexeme, Word, English, Etymology)):
        d = {}
        for line in read_db_file(DB_DIR, f):
            e = c(line)
            d[e.id] = e
        db.append(d)
    return tuple(db)

def read_nt_file():
    return tuple(NtWords(line) for line in read_db_file(DB_DIR, NT_FILE))

db = read_db_files()
nt = read_nt_file()

def main():
    pass

def usage():
    print(__doc__)

if __name__ == "__main__":
        main()
