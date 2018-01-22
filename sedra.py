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
import os
from constants import SedraIII as c


ROOTS    = 'roots'
LEXEMES  = 'lexemes'
WORDS    = 'words'
ENGLISH  = 'english'
ETIMOLGY = 'etymology'
NT       = 'nt'

ATTR = 'attr'
FEAT = 'feat'

# Read database location from config file
try: # allow for different module names in python 2 and 3
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

config = ConfigParser()
config.read('linksyr.conf')
SEDRA_DIR = config.get('sedra','datadir')
SEDRA_FILES = {
    'roots':     config.get('sedra','roots'),
    'lexemes':   config.get('sedra','lexemes'),
    'words':     config.get('sedra','words'),
    'english':   config.get('sedra','english'),
    'etymology': config.get('sedra','etimolgy'),
    'nt':        config.get('sedra','nt')
}



def root_attributes(n):
    # ROOTS.TXT
    # Attributes: 16-bit intiger as follows
    if n<0: n+=65536
    b = '{0:016b}'.format(n)
    return (
        int( b[-1],    2), # 0  SEYAME FLAG:
        int( b[-3:-1], 2), # 1-2 ROOT TYPE:
        int( b[:-3],   2)  # 3-15 <RESERVED>
    )

def lexeme_attributes(n):
    # LEXEMES.TXT
    # Attributes: 16-bit intiger as follows
    if n<0: n+=65536
    b = '{0:016b}'.format(n)
    return (
        int( b[-1],    2), # 0 SEYAME FLAG:
        int( b[-2],    2), # 1 WORD TYPE:
        int( b[-6:-2], 2), # 2-5 GRAMMATICAL CATEGORY:
        int( b[:-6],   2)
    )

def lexeme_features(n):
    # LEXEMES.TXT
    # Morphological Type: 32-bit intiger as follows
    if n<0: n+=2147483648  #4294967296?
    b = '{0:032b}'.format(n)
    return (
        int( b[-4:],     2), # 0-3 First SUFFIX:
        int( b[-6:-4],   2), # 4-5 SECOND SUFFIX:
        int( b[-8:-6],   2), # 6-7 THIRD SUFFIX:
        int( b[-10:-8],  2), # 8-9 PREFIX:
        int( b[-13:-10], 2), # 10-12 FIRST VOWEL:
        int( b[-16:-13], 2), # 13-15 SECOND VOWEL: as above
        int( b[-19:-16], 2), # 16-18 THIRD VOWEL: as above
        int( b[-22:-19], 2), # 19-21 FOURTH VOWEL: as above
        int( b[-25:-22], 2), # 22-24 Total no of vowels in lexeme: 0-7
        int( b[-28:-25], 2), # 25-27 RADICAL TYPE:
        int( b[:-28],    2)  # 28-31 FORM:
    )

def word_attributes(n):
    # WORDS.TXT
    # Attributes: 16-bit intiger as follows
    if n<0: n+=65536
    b = '{0:016b}'.format(n)
    return (
        int( b[-1],    2), # 0 SEYAME FLAG:
        int( b[-5:-1], 2), # 1-4 ignore
        int( b[-6],    2), # 5 ENCLITIC FLAG:
        int( b[-7],    2), # 6 LEXEME FLAG:
        int( b[:-7],   2)  ## added HV
    )

def word_features(n):
    # WORDS.TXT
    # Morphological Features: 32-bit intiger as follows
    if n<0: n+=2147483648  #4294967296?
    b = '{0:032b}'.format(n)
    return (
        int( b[-2:],     2), # 0-1 <RESERVED>
        int( b[-4:-2],   2), # 2-3 SUFFIX GENDER:
        int( b[-6:-4],   2), # 4-5 SUFFIX PERSON:
        int( b[-7],      2), # 6 SUFFIX NUMBER:
        int( b[-9:-7],   2), # 7-8 SUFFIX/CONTRACTION:
        int( b[-15:-9],  2), # 9-14 PREFIX CODE: 0-63
        int( b[-17:-15], 2), # 15-16 GENDER:
        int( b[-19:-17], 2), # 17-18 PERSON:
        int( b[-21:-19], 2), # 19-20 NUMBER:
        int( b[-23:-21], 2), # 21-22 STATE:
        int( b[-26:-23], 2), # 23-25 TENSE:
        int( b[:-26],    2)  # 26-31 FORM:
    )

def eng_attributes(n):
    # ENGLISH.TXT
    # Attributes: 15-bit intiger as follows:
    if n<0: n+=65536
    b = '{0:016b}'.format(n)
    return (
        int( b[-1],      2), # 0 <RESERVED>
        int( b[-2],      2), # 1 COMMENT POSITION:
        int( b[-3],      2), # 2 COMMENT FONT:
        int( b[-4],      2), # 3 STRING BEFORE FONT: as above
        int( b[-5],      2), # 4 STRING AFTER FONT: as above
        int( b[-7:-5],   2), # 5-6 VERB TYPE:
        int( b[-9:-7],   2), # 7-8 NUMBER: as above
        int( b[-11:-9],  2), # 9-10 GENDER: as above
        int( b[:-11],    2)
        # int( b[-15:-11], 2), # 11-15 FORM: as above
        ## TODO: 5bit (b[-16:-11])? this is strange.
        ## Maybe it should be 4bit (b[-15:-11])?
        # int( b[-16],     2)  # Ignore last field
    )

def etym_attributes(n):
    # ETIMOLGY.TXT
    # Attributes: 16-bit intigier as follows:
    b = '{0:016b}'.format(n)
    return (
        int( b[-4:], 2),    # 0-3 LANGUAGE:
        int( b[-5],  2),    # 4 TYPE:
        int( b[:-5], 2)     ## added /HV
    )

def nt_attributes(n):
    if n<0: n+=65536
    return '{0:016b}'.format(n)

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

# read files
db = {}

# Read ROOTS.TXT to a dictionary.
db[ROOTS] = {}
with open(os.path.join(SEDRA_DIR, SEDRA_FILES[ROOTS])) as f:
    for line in f:
        # rt_addr, rt_str, sort_str, attr = line.strip().split(',')
        # rt_file, rt_id = [int(a) for a in rt_addr.split(':')]

        # first comma separated field (only the id after the colon)
        rt_id = int(line.split(',')[0].split(':')[1])
        # middle two string fields, surrounded by double quotes
        # and separated by commas
        rt_str, sort_str = line.split('"')[1:-1:2]
        # last comma separated field
        attr = int(line.split(',')[-1])

        attributes = root_attributes(int(attr))
        attr_values = get_values(c.ROOTS_ATTR, attributes)

        db[ROOTS][rt_id] = {
            'id':           rt_id,
            'rt_str':       rt_str,
            'sort_str':     sort_str,
            'attributes':   attributes,
            'attr_values':  attr_values
        }


# Read LEXEMES.TXT to a dictionary.
# REMARK: in the documentation SEDRA3.DOC, the order of the last
# two fields seems to be reversed.
db[LEXEMES] = {}
with open(os.path.join(SEDRA_DIR, SEDRA_FILES[LEXEMES])) as f:
    for line in f:
        # lex_addr, rt_addr, lex_str, feat, attr = line.strip().split(',')
        # lex_file, lex_id = [int(a) for a in lex_addr.split(':')]
        # rt_id = None if rt_addr == 'NULL' else int(rt_addr.split(':')[-1])

        # first two comma separated fields (only the id after the colon)
        lex_id, rt_id = [ int(a.split(':')[1])
                            if a != 'NULL' else None
                            for a in line.split(',')[:2] ]
        # middle string field, surrounded by double quotes
        lex_str = line.split('"')[1]
        # # last comma separated field
        # attr = int(line.split(',')[-1])
        # last two comma separated fields
        feat, attr = [ int(a) for a in line.split(',')[-2:] ]

        attributes = lexeme_attributes(attr)
        attr_values = get_values(c.LEXEMES_ATTR, attributes)
        features = lexeme_features(feat)
        feat_values = get_values(c.LEXEMES_FEAT, features)

        db[LEXEMES][lex_id] = {
            'id':           lex_id,
            'rt_id':        rt_id,
            'root':         db[ROOTS][rt_id] if rt_id else None,
            'lex_str':      lex_str,
            'attributes':   attributes,
            'attr_values':  attr_values,
            'features':     features,
            'feat_values':  feat_values
        }


# Read WORDS.TXT to a dictionary.
# REMARK: in the documentation SEDRA3.DOC, the order of the last
# two fields seems to be reversed.
db[WORDS] = {}
with open(os.path.join(SEDRA_DIR, SEDRA_FILES[WORDS])) as f:
    for line in f:
        # first two comma separated fields (only the id after the colon)
        word_id, lex_id = [ int(a.split(':')[1])
                            if a != 'NULL' else None
                            for a in line.split(',')[:2] ]
        # middle two string fields, surrounded by double quotes
        # and separated by commas, but also containing commas, so
        # cannot just split by commas. Instead, split string by
        # double quotes, and then select only the even elements
        # (ignoring first, last, and comma elements)
        cons_str, voc_str = line.split('"')[1:-1:2]
        # last two comma separated fields
        feat, attr = [ int(a) for a in line.split(',')[-2:] ]

        attributes = word_attributes(attr)
        attr_values = get_values(c.WORDS_ATTR, attributes)
        features = word_features(feat)
        feat_values = get_values(c.WORDS_FEAT, features)

        db[WORDS][word_id] = {
            'id':           word_id,
            'lex_id':       lex_id,
            'lexeme':       db[LEXEMES][lex_id] if lex_id else None,
            'rt_id':        db[LEXEMES][lex_id]['rt_id'] if lex_id else None,
            'root':         db[LEXEMES][lex_id]['root'] if lex_id else None,
            'cons_str':     cons_str,
            'voc_str':      voc_str,
            'attributes':   attributes,
            'attr_values':  attr_values,
            'features':     features,
            'feat_values':  feat_values
        }


# Read ENGLISH.TXT to a dictionary.
#
# ENGLISH.TXT
# ===========
#    English meaning records, e.g.
#       3:165,1:97,"cause","without","","",0,0
#
#    Fields:
#       Record address, e.g. 3:165
#       Lexeme address (in LEXEMES.TXT), e.g. 1:97
#       Meaning, e.g. "cause"
#       String before meaning, e.g. "without" (i.e. without cause)
#       String after meaning, e.g. ""
#       Comment, e.g. ""
#       Attributes: 15-bit intiger
#       Ignore last field
#
# REMARK: in the documentation SEDRA3.DOC, the bit count for
# the FORM field seems to be wrong
db[ENGLISH] = {}
with open(os.path.join(SEDRA_DIR, SEDRA_FILES[ENGLISH])) as f:
    for line in f:
        # first two comma separated fields (only the id after the colon)
        eng_id, lex_id = [ int(a.split(':')[1])
                            if a != 'NULL' else None
                            for a in line.split(',')[:2] ]
        # middle four string fields, surrounded by double quotes
        # and separated by commas, but also containing commas, so
        # cannot just split by commas. Instead, split string by
        # double quotes, and then select only the even elements
        # (ignoring first, last, and comma elements)
        meaning, before, after, comment = line.split('"')[1:-1:2]
        # last two comma separated fields
        attr, ignore = [ int(a) for a in line.split(',')[-2:] ]

        attributes = eng_attributes(attr)
        attr_values = get_values(c.ENGLISH_ATTR, attributes)

        db[ENGLISH][eng_id] = {
            'id':           eng_id,         # int
            'lex_id':       lex_id,         # int
            'meaning':      meaning,        # string
            'before':       before,         # string
            'after':        after,          # string
            'comment':      comment,        # string
            'attributes':   attributes,     # tuple of integers
            'attr_values':  attr_values,    # dict of strings
            'ignore':       ignore          # 0 or (sometimes) 1
        }


db[ETIMOLGY] = {}
# etym_attributes()

db[NT] = {}
with open(os.path.join(SEDRA_DIR, SEDRA_FILES[NT])) as f:
    for line in f:
        # Split comma separated fields:
        rec_addr, loc_id, word_addr, attr = line.strip().split(',')

        # Retrieve encoded data from fields:
        # file_id and rec_num are pretty useless info,
        # since file_id is 0, just as ROOTS, and rec_num is not unique
        # so we can disregard them
        #file_id, rec_num = [int(a) for a in rec_id.split(':')]
        # word_addr is a crazy encoded decimal value of two combined
        # hexadecimal values, the first of which is always '02'
        # (the number of the WORDS.TXT file). So to retrieve
        # the word_id, we must convert word_addr to a hex string
        # of eight positions, and convert the rightmost six back
        # to decimal. The leftmost two will always be '02'.
        #word_file_id = int('{:08x}'.format(int(word_addr))[:2], 16)
        # word_file_id is always '02'
        word_id = int('{:08x}'.format(int(word_addr))[2:], 16)
        # split the loc_id into book, chapter, verse, and word_num
        book_id = int(loc_id[:2])
        chapter = int(loc_id[2:4])
        verse = int(loc_id[4:7])
        word_num = int(loc_id[7:])
        # relevance of attributes is not so clear
        attributes = nt_attributes(int(attr)) # TODO there is no key for NT attributes?

        db[NT][int(loc_id)] = {
            'id':         loc_id,                       # string (e.g. '520100101')
            'book_id':    book_id,                      # integer
            'book_name':  c.BOOK_NAMES[book_id],        # string (e.g. 'Matt')
            'chapter':    chapter,                      # integer
            'verse':      verse,                        # integer
            'word_num':   word_num,                     # integer
            'word_id':    word_id,                      # integer
            'word':       db[WORDS][word_id],           # dict
            'lex_id':     db[WORDS][word_id]['lex_id'], # dict
            'lexeme':     db[WORDS][word_id]['lexeme'], # dict or None
            'rt_id':      db[WORDS][word_id]['rt_id'],  # dict
            'root':       db[WORDS][word_id]['root'],   # dict or None
            'attributes': attr#,                        # binary string
            #'attr_values': get_values(c.NT_ATTR, attributes) # TODO
        }


absedra = 'A  B G D H O Z K Y ; C L M N S E I / X R W T a e i o u * , \' _ -'
abpil =   '\' b g d h w z H T y k l m n s ` p S q r $ t a e i A u " # ^ #_ -'
sedratopil = dict(zip(absedra.split(), abpil.split()))

# ignore vowels
for c in 'aeiou':
    sedratopil[c] = ''

def tr(s):
    return ''.join([sedratopil[c] for c in s])

def main():
    prev_verse = 1
    prev_chapter = 1
    for w_id in sorted(db['nt']):
        e = db['nt'][w_id]

        # print newlines between chapters and verses
        if e['chapter'] != prev_chapter:
            print('\n\n{} {}'.format(e['book_name'], e['chapter']), end='')
            prev_chapter = e['chapter']
        if e['verse'] != prev_verse:
            print('\n{} {} {} '.format(e['book_name'], e['chapter'], e['verse']), end='')
            prev_verse = e['verse']
        else:
            print(' ', end='')

        print(tr(e['word']['voc_str']), end = '')

    print('') # print newline after last verse


# def main():
#     for w_id, e in db['words'].items():
#         print('{0:06b}'.format(e['features'][5]), e['cons_str'])

# def main():
#     for w_id, e in db['nt'].items():
#         if e['word_id'] == 625:
#             print(w_id, e['book_name'], e['chapter'], e['verse'], e['word_num'])

def usage():
    print(__doc__)

if __name__ == "__main__":
        main()
