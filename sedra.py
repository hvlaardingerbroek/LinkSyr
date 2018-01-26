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
# The SEDRA III database is read into the variable db,
# the New Testament text is read into the variable nt.
# TODO
# Not all attributes and features are clearly explained
# in the documentation, so some research may improve
# their usefulness.
# TODO
# The English and Etymology files contain references
# to the relevant lexemes, it would be useful to add
# references back from Lexeme and Word objects, or a
# pivot table.
# TODO
# The database files are now referenced by hardcoded
# adresses (e.g. db[2] for the Words db). That should
# be something like db[words]. Maybe.
# TODO
# Add values for prefix-attribute in constants.py, and
# find a way to reconstruct suffixes, and add relevant
# attributes/methods to Word class.
# TODO
# With the prefixes and suffixes, make a supertag-method
# for the NTWord-class.
# TODO
# Add extensive documentation to classes/methods.

from __future__ import print_function
import os
from constants import NT_BOOKS, SedraIII as c

cfg_filename = 'linksyr.conf'
cfg_section = 'sedra'
cfg_fields = ('datadir',
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
cfg = ConfigParser()
cfg.read(cfg_filename)
cfg_items = dict(cfg.items(cfg_section))

DB_DIR = cfg_items[cfg_fields[0]]
DB_FILES = tuple(cfg_items[s] for s in cfg_fields[1:6])
NT_FILE = cfg_items[cfg_fields[6]]
NT_OFFSET = 52  # starting id of NT books


class Root:
    def __init__(self, line):
        self.id = get_address(line[0])
        self.rt_str = line[1]
        self.sort_str = line[2]
        self.attr = int(line[3])

    def __repr__(self):
        return '<Root id {0}: {1}>'.format(self.id, self.rt_str)

    def __str__(self):
        return self.rt_str

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

    def __repr__(self):
        return '<Lexeme id {0}: {1}>'.format(self.id, self.lex_str)

    def __str__(self):
        return self.lex_str

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

    def __repr__(self):
        return '<Word id {0}: {1}>'.format(self.id, self.cons_str)

    def __str__(self):
        return self.cons_str

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

    def __repr__(self):
        return '<English id {0}: {1}>'.format(self.id, self.meaning)

    def __str__(self):
        return self.meaning

    @property
    def attributes(self):
        return split_bits(self._attr, (1,1,1,1,1,2,2,2,5), 16)


class Etymology:
    def __init__(self, line):
        self.id = get_address(line[0])    # Record address, e.g. 4:1
        self.lex_addr = get_address(line[1])    # Lexeme address (in LEXEMES.TXT), e.g. 1:1
        self.word_origin = line[2]              # Word Origin, e.g. "a\255h\256r"
        self.attr = int(line[3])

    def __repr__(self):
        return '<Etymology id {0}: {1}>'.format(self.id, self.attr_values['LANGUAGE'])

    def __str__(self):
        return self.attr_values['LANGUAGE']

    @property
    def attributes(self):
        return split_bits(self.attr, (4,1,11), 16)

    @property
    def attr_values(self):
        return get_values(c.ETYMOLOGY_ATTR, self.attributes)


class NTWord:
    def __init__(self, line):
        # self._rec_addr = line[0]  # _rec_addr is not unique, so useless
        self.location = split_loc_id(line[1])      # _loc_id
        self.word_addr = get_word_addr(line[2])   # tuple, e.g. (2,1)
        self.attr = int(line[3])

    def __repr__(self):
        return '<NTWord id {0}>'.format(self.loc_str)

    def __str__(self):
        return self.__repr__()

    @property
    def loc_str(self):
        return '{0:02}{1:02}{2:03}{3:02}'.format(*self.location)

    @property
    def book(self):
        return self.location[0]

    @property
    def book_name(self):
        return NT_BOOKS[self.location[0]-NT_OFFSET][0]

    @property
    def chapter(self):
        return self.location[1]

    @property
    def verse(self):
        return self.location[2]

    @property
    def word_num(self):
        return self.location[3]

    @property
    def attributes(self):
        return split_bits(self.attr, (16,), 16)

    @property
    def attr_bits(self):
        return '{0:016b}'.format(self.attr)

    @property
    def word(self):
        # TODO find more elegant way to refer to WORDS db
        return db[self.word_addr[0]][self.word_addr[1]]

    # def get_supertag(self):
    #     # TODO construct supertag
    #     # Get prefix from Word - TODO add prefixes to constants.py
    #     # TODO find out how to reconstruct suffix in Word from bits
    #     return self.word


def get_address(a):
    return int(a.split(':')[1]) if a != 'NULL' else None

def get_word_addr(a):
    # word_addr is a crazy encoded decimal value of two combined
    # hexadecimal values, the first of which is always '02'
    # (the number of the WORDS.TXT file). So to retrieve
    # the word_id, we must convert word_addr to a hex string
    # of eight positions, and convert the rightmost six back
    # to decimal. The leftmost two will always be '02'.
    h = '{0:08x}'.format(int(a))
    return (int(h[:2], 16), int(h[2:], 16))

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

def split_loc_id(s):
    '''Split loc_id s into elements: '250100101' -> (25, 1, 1, 1)'''
    return tuple(int(e) for e in (s[:2], s[2:4], s[4:7], s[7:]))

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

# since source file is not in order, need to sort list first
def read_nt_file():
    nt = []
    for line in read_db_file(DB_DIR, NT_FILE):
        nt.append(NTWord(line))
    return sorted(nt, key=lambda w: w.location)

db = read_db_files()
nt = read_nt_file()

# add variable names to access the separate db files:
roots_db, lexemes_db, words_db, english_db, etymology_db = db

def nt_verses():
    prev_verse = 1
    verse = []
    for word in nt:
        if word.verse != prev_verse:
            yield verse
            verse = []
            prev_verse = word.verse
        verse.append(word)
    yield verse
    # return tuple(NTWord(line) for line in read_db_file(DB_DIR, NT_FILE))

def main():
    pass

def usage():
    print(__doc__)

if __name__ == "__main__":
        main()
