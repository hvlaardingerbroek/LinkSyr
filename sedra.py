#!/usr/bin/python3
# -*- coding: utf-8 -*-
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
# Add values for prefix-attribute in constants.py, and
# find a way to reconstruct suffixes, and add relevant
# attributes/methods to Word class.
# TODO
# With the prefixes and suffixes, make a supertag-method
# for the NTWord-class.
# TODO
# Add documentation to classes/methods.

# now it works in python 2.6 and 3.x!
from __future__ import unicode_literals, print_function
import os
from collections import namedtuple
from constants import NT_BOOKS, SedraIII as c

CFG_FILENAME = 'linksyr.conf'
CFG_SECTION = 'sedra'
CFG_FIELDS = ('datadir',
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
cfg.read(CFG_FILENAME)
cfg_items = dict(cfg.items(CFG_SECTION))

DB_DIR = cfg_items[CFG_FIELDS[0]]
DB_FILES = tuple(cfg_items[s] for s in CFG_FIELDS[1:6])
NT_FILE = cfg_items[CFG_FIELDS[6]]
NT_OFFSET = 52  # starting id of NT books


class Root:
    # example input line: 0:1,"AAR","aat          |0",0

    Attributes = namedtuple('Attributes',
                    [f[0].strip('<>').replace(' ','_') for f in c.ROOTS_ATTR])

    def __init__(self, line):
        self.id = int(line[0].split(':')[1])
        self.rt_str = line[1]
        self.sort_str = line[2]
        self.attr = int(line[3])
        attr_values = get_values(self.attr, c.ROOTS_ATTR)
        self.attributes = Root.Attributes(*attr_values)

    def __repr__(self):
        return get_identifier(self)

    def __str__(self):
        return self.rt_str


class Lexeme:
    # example input line: 1:2,0:2,"ABA",41960448,16

    Attributes = namedtuple('Attributes',
                    [f[0].strip('<>').replace(' ','_') for f in c.LEXEMES_ATTR])
    Features = namedtuple('Features',
                    [f[0].strip('<>').replace(' ','_') for f in c.LEXEMES_FEAT])

    def __init__(self, line):
        self.id = int(line[0].split(':')[1])
        self.root_addr = get_address(line[1])
        self.lex_str = line[2]
        self.feat = int(line[3])
        feat_values = get_values(self.feat, c.LEXEMES_FEAT)
        self.features = Lexeme.Features(*feat_values)
        self.attr = int(line[4])
        attr_values = get_values(self.attr, c.LEXEMES_ATTR)
        self.attributes = Lexeme.Attributes(*attr_values)


    def __repr__(self):
        return get_identifier(self)

    def __str__(self):
        return self.lex_str

    @property
    def root(self):
        return db_lookup(self.root_addr) if self.root_addr else None

    @property
    def english(self):
        return [e for k,e in db[3].items()
                  if e.lex_id is not None and  e.lex_id[1] == self.id]


class Word:
    # example input line: 2:3,1:1,"DAAR","D'oAAaR",558080,128

    Attributes = namedtuple('Attributes',
                    [f[0].strip('<>').replace(' ','_') for f in c.WORDS_ATTR])
    Features = namedtuple('Features',
                    [f[0].strip('<>').replace(' ','_').replace('/','_') for f in c.WORDS_FEAT])

    def __init__(self, line):
        self.id = int(line[0].split(':')[1])
        self.lex_addr = get_address(line[1])
        self.cons_str = line[2]
        self.voc_str = line[3]
        self.feat = int(line[4])
        feat_values = get_values(self.feat, c.WORDS_FEAT)
        self.features = Word.Features(*feat_values)
        self.attr = int(line[5])
        attr_values = get_values(self.attr, c.WORDS_ATTR)
        self.attributes = Word.Attributes(*attr_values)

    def __repr__(self):
        return get_identifier(self)

    def __str__(self):
        return self.cons_str

    @property
    def lexeme(self):
        return db_lookup(self.lex_addr) if self.lex_addr else None

    @property
    def root(self):
        return self.lexeme.root if self.lexeme else None


class English:
    # example input line: 3:36,1:22,"land","parcel of","","",0,0

    Attributes = namedtuple('Attributes',
                    [f[0].strip('<>').replace(' ','_') for f in c.ENGLISH_ATTR])

    def __init__(self, line):
        self.id = int(line[0].split(':')[1])
        self.lex_id = get_address(line[1])
        self.meaning = line[2]
        self.before = line[3]
        self.after = line[4]
        self.comment = line[5]
        self.attr = int(line[6])
        attr_values = get_values(self.attr, c.ENGLISH_ATTR)
        self.attributes = English.Attributes(*attr_values)
        self.ignore = int(line[7])

    def __repr__(self):
        return get_identifier(self)

    def __str__(self):
        return self.meaning


class Etymology:
    # example input line: 4:5,1:46,"eu\255jaristi\256a",5

    Attributes = namedtuple('Attributes',
                    [f[0].strip('<>').replace(' ','_') for f in c.ETYMOLOGY_ATTR])

    def __init__(self, line):
        self.id = int(line[0].split(':')[1])    # Record address, e.g. 4:1
        self.lex_addr = get_address(line[1])    # Lexeme address (in LEXEMES.TXT), e.g. 1:1
        self.word_origin = line[2]              # Word Origin, e.g. "a\255h\256r"
        self.attr = int(line[3])
        attr_values = get_values(self.attr, c.ETYMOLOGY_ATTR)
        self.attributes = Etymology.Attributes(*attr_values)

    def __repr__(self):
        return get_identifier(self)

    def __str__(self):
        return self.attr_values.LANGUAGE # ['LANGUAGE']


class NTWord:
    # example input line: 0:6,520100106,33558659,24

    Location = namedtuple('Location',
                    ['book_name', 'book_id', 'chapter', 'verse', 'w_num'])

    def __init__(self, line):
        # self.rec_addr = line[0]  # rec_addr is not unique, so useless as id
        self.id = int(line[1]) # use location id as identifier instead
        self.location = NTWord.Location(*get_location(line[1]))
        self.word_addr = self._get_word_addr(line[2]) # tuple, e.g. (2,1)
        self.attr = int(line[3])
        self.attributes = self.attr # TODO find attribute description
        self.attr_bits = '{0:016b}'.format(self.attr) # for easier inspection

    def __repr__(self):
        return get_identifier(self)

    def __str__(self):
        return self.word.__str__()

    def _get_word_addr(self, a):
        # word_addr is a crazy encoded decimal value of two combined
        # hexadecimal values, the first of which is always '02'
        # (the number of the WORDS.TXT file). So to retrieve
        # the word_id, we must convert word_addr to a hex string
        # of eight positions, and convert the rightmost six back
        # to decimal. The leftmost two will always be '02'.
        h = '{0:08x}'.format(int(a))
        return (int(h[:2], 16), int(h[2:], 16))

    @property
    def word(self):
        return db_lookup(self.word_addr)

    @property
    def lexeme(self):
        return self.word.lexeme

    @property
    def root(self):
        return self.word.root

    @property
    def cons_str(self):
        return self.word.cons_str


def get_identifier(o):
    return '<{0}.{1} {2}: {3}>'.format(o.__module__,
                                       o.__class__.__name__,
                                       o.id,
                                       o.__str__())

def get_address(a):
    return tuple(int(e) for e in a.split(':')) if a != 'NULL' else None

def get_values(n, fields):
    # TODO calculating bit groups for every record may be inefficient,
    # maybe it could be done once in a class variable?
    bit_groups = [f_bits for (f_name, f_bits, f_values) in fields]
    bits = 32 if sum(bit_groups) > 16 else 16
    values = split_bits(n, bit_groups, bits)
    return [(l[2][n] if l[2] else n) for l, n in zip(fields, values)]

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

def get_location(s):
    loc_id = tuple(int(e) for e in (s[:2], s[2:4], s[4:7], s[7:]))
    book_name = NT_BOOKS[loc_id[0]-NT_OFFSET][0]
    return (book_name,) + loc_id

def db_lookup(addr):
    return db[addr[0]][addr[1]]

def read_db_file(db_dir, filename):
    from csv import reader
    with open(os.path.join(db_dir, filename), 'r') as f:
        for line in reader(f):
            try:        # csv.reader in python 2 does not support Unicode
                line = [e.decode('utf-8') for e in line]
            except AttributeError:
                pass    # for Python 3, no decoding is possible/necessary
            yield line

def read_db_files():
    db = []
    for f, c in zip(DB_FILES, (Root, Lexeme, Word, English, Etymology)):
        d = {}
        for line in read_db_file(DB_DIR, f):
            e = c(line)
            d[e.id] = e
        db.append(d)
    return tuple(db)

# since source file is not sorted properly, need to sort list first
def read_nt_file():
    nt = []
    for line in read_db_file(DB_DIR, NT_FILE):
        nt.append(NTWord(line))
    return sorted(nt, key=lambda w: w.id)

db = read_db_files()
nt = read_nt_file()

# add variable names to access the separate db files:
roots_db, lexemes_db, words_db, english_db, etymology_db = db

def nt_verses():
    verse = []
    verse_label = nt[0].location[:4]
    for word in nt:
        if word.location[:4] != verse_label:
            yield (verse_label, verse)
            verse = []
            verse_label = word.location[:4]
        verse.append(word)
    yield (verse_label, verse)

def nt_words():
    for w in nt:
        yield w

def maketrans(s1, s2):
    '''Make a simple translation table'''
    # There are more sophisticated maketrans-functions (str.maketrans()
    # in python 3 and string.maketrans() in python 2, but they are not
    # compatible. The dictionary works in all versions from at least 2.6)
    return dict(zip([ord(a) for a in s1], [ord(a) for a in s2]))

# translation tables:
# source is always SEDRA transcription, so only need to specify 'to'.
towit = maketrans('AOKY;CEI/XW','>WXVJK<PYQC')
tosyr = maketrans('ABGDHOZKY;CLMNSEI/XRWT','ܐܒܓܕܗܘܙܚܛܝܟܠܡܢܣܥܦܨܩܪܫܬ')
notr = maketrans('','')

def print_nt(tr=towit):
    pl = None # pl: previous label
    for l, v in nt_verses():
        if pl is None or pl[1] != l[1] or pl[2] != l[2]:
            if pl is not None:  # no newline before first chapter
                yield ''
                # nt.append('')   # add newline before chapter label
            yield '{0} chapter {1}'.format(l[0], l[2])
        pl = l
        yield '{0:2} {1}'.format(l[3],
                ' '.join([w.cons_str.translate(tr) for w in v]))


def main():
    for line in print_nt():
        print(line)

def usage():
    print(__doc__)

if __name__ == "__main__":
        main()
