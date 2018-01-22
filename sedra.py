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

ROOTS    = 'roots'
LEXEMES  = 'lexemes'
WORDS    = 'words'
ENGLISH  = 'english'
ETIMOLGY = 'etymology'
NT       = 'nt'

ATTR = 'attr'
FEAT = 'feat'

SEDRA_DIR = '../data/sedra'
SEDRA_FILES = {
    ROOTS:    "ROOTS.TXT",
    LEXEMES:  "LEXEMES.TXT",
    WORDS:    "WORDS.TXT",
    ENGLISH:  "ENGLISH.TXT",
    ETIMOLGY: "ETIMOLGY.TXT",
    NT:       "BFBS.TXT"
}
BOOK_NAMES = {
    52 : 'Matt',
    53 : 'Mark',
    54 : 'Luke',
    55 : 'John',
    56 : 'Acts',
    57 : 'Rom',
    58 : '1Cor',
    59 : '2Cor',
    60 : 'Gal',
    61 : 'Eph',
    62 : 'Phil',
    63 : 'Col',
    64 : '1Thess',
    65 : '2Thess',
    66 : '1Tim',
    67 : '2Tim',
    68 : 'Titus',
    69 : 'Phlm',
    70 : 'Heb',
    71 : 'James',
    72 : '1Peter',
    73 : '2Peter',
    74 : '1John',
    75 : '2John',
    76 : '3John',
    77 : 'Jude',
    78 : 'Rev'
}

# ANNOTATIONS[ROOTS][ATTR]['SEYAME FLAG'][root['attr'][FIELDS]]
ANNOTATIONS = {
    ROOTS: {                        # ROOTS.TXT
        ATTR: ((                     # Attributes: 16-bit intiger as follows
            'SEYAME FLAG', (        # 0  SEYAME FLAG:
                'NO SEYAME',        #     0 NO SEYAME
                'SEYAME'            #     1 SEYAME
            )), (
            'ROOT TYPE', (          # 1-2 ROOT TYPE:
                'NORMAL',           #     00 NORMAL
                'PARETHESIED',      #     01 PARETHESIED
                'BRACKETED',        #     10 BRACKETED
                'HIGH FREQUENCY ROOT, e.g. propositons'
                                    #     11 HIGH FREQUENCY ROOT, e.g. propositons
            )), (
            '<RESERVED>', None      # 3-15 <RESERVED>
        ))
    },
    LEXEMES: {                      # LEXEMES.TXT
        ATTR: ((                    # Attributes: 16-bit intiger as follows
            'SEYAME FLAG', (        # 0 SEYAME FLAG:
                'NO SEYAME',        #     0 NO SEYAME
                'SEYAME'            #     1 SEYAME
            )), (
            'WORD TYPE', (          # 1 WORD TYPE:
                'NORMAL',           #     0 NORMAL
                'PARENTHESISED'     #     1 PARENTHESISED
            )), (
            'GRAMMATICAL CATEGORY', (
                                    # 2-5 GRAMMATICAL CATEGORY:
                'VERB',             #     0000 VERB
                'PARTICIPLE ADJECTIVE',
                                    #     0001 PARTICIPLE ADJECTIVE
                'DENOMINATIVE',     #     0010 DENOMINATIVE
                'SUBSTANTIVE',      #     0011 SUBSTANTIVE
                'NOUN',             #     0100 NOUN
                'PRONOUN',          #     0101 PRONOUN
                'PROPER_NOUN',      #     0110 PROPER_NOUN
                'NUMERAL',          #     0111 NUMERAL
                'ADJECTIVE',        #     1000 ADJECTIVE
                'PARTICLE',         #     1001 PARTICLE
                'IDIOM',            #     1010 IDIOM
                'ADVERB (ending with AiYT)',
                                    #     1011 ADVERB (ending with AiYT)
                'ADJECTIVE OF PLACE',
                                    #     1100 ADJECTIVE OF PLACE
                'ADVERB'            #     1101 ADVERB
            ))
        ),
        FEAT: ((                    # Morphological Type: 32-bit intiger as follows
            'First SUFFIX', (       # 0-3 First SUFFIX:
                '<NONE>',           #     0000 <NONE>
                'ToA',              #     0001 ToA
                'YoA',              #     0010 YoA
                'NoA',              #     0011 NoA
                'oNoA',             #     0100 oNoA
                'iYNoA',            #     0101 iYNoA
                'uONoA',            #     0110 uONoA
                'ToNoA',            #     0111 ToNoA
                'TuONoA',           #     1000 TuONoA
                'uOSoA',            #     1001 uOSoA
                'oRoA',             #     1010 oRoA
                'QoNoA',            #     1011 QoNoA
                'i;N'               #     1100 i;N
            )), (
            'SECOND SUFFIX', (      # 4-5 SECOND SUFFIX:
                '<NONE>',           #     00 <NONE>
                'oYoA',             #     01 oYoA
                'iYToA'             #     10 iYToA
            )), (
            'THIRD SUFFIX', (       # 6-7 THIRD SUFFIX:
                '<NONE>',           #     00 <NONE>
                'uOToA',            #     01 uOToA
                'oAiYT'             #     10 oAiYT
            )), (
            'PREFIX', (             # 8-9 PREFIX:
                '<NONE>',           #     00 <NONE>
                'M',                #     01 M
                'T',                #     10 T
                '?????????',         ##              /add -HV
            )), (
            'FIRST VOWEL', (        # 10-12 FIRST VOWEL:
                '<NONE>',           #     000 <NONE>
                'a',                #     001 a
                'o',                #     010 o
                'e',                #     011 e
                'i',                #     100 i
                'u'                 #     101 u
            )), (
            'SECOND VOWEL', (       # 13-15 SECOND VOWEL: as above
                '<NONE>',           ##    000 <NONE>
                'a',                ##    001 a
                'o',                ##    010 o
                'e',                ##    011 e
                'i',                ##    100 i
                'u'                 ##    101 u
            )), (
            'THIRD VOWEL', (        # 16-18 THIRD VOWEL: as above
                '<NONE>',           ##    000 <NONE>
                'a',                ##    001 a
                'o',                ##    010 o
                'e',                ##    011 e
                'i',                ##    100 i
                'u'                 ##    101 u
            )), (
            'FOURTH VOWEL', (        # 19-21 FOURTH VOWEL: as above
                '<NONE>',           ##    000 <NONE>
                'a',                ##    001 a
                'o',                ##    010 o
                'e',                ##    011 e
                'i',                ##    100 i
                'u'                 ##    101 u
            )), (
            'NUM_VOWELS', None
            ), (
                                    # 22-24 Total no of vowels in lexeme: 0-7
            'RADICAL TYPE', (       # 25-27 RADICAL TYPE:
                '<NONE>',           #     000 <NONE>
                'BI',               #     001 BI
                'TRI',              #     010 TRI
                'FOUR_RADICAL',     #     011 FOUR_RADICAL
                'FIVE_RADICAL',     #     100 FIVE_RADICAL
                'SIX_RADICAL',      #     101 SIX_RADICAL
                'COMPOUND'          #     110 COMPOUND
            )), (
            'FORM', (               # 28-31 FORM:
                '<NONE>',           #     0000 <NONE>
                'PEAL',             #     0001 PEAL
                'ETHPEAL',          #     0010 ETHPEAL
                'PAEL',             #     0011 PAEL
                'ETHPAEL',          #     0100 ETHPAEL
                'APHEL',            #     0101 APHEL
                'ETTAPHAL',         #     0110 ETTAPHAL
                'SHAPHEL',          #     0111 SHAPHEL
                'ESHTAPHAL',        #     1000 ESHTAPHAL
                'SAPHEL',           #     1001 SAPHEL
                'ESTAPHAL',         #     1010 ESTAPHAL
                'P',                #     1011 P
                'ETHP',             #     1100 ETHP
                'PALPEL',           #     1101 PALPEL
                'ETHPALPAL'         #     1110 ETHPALPAL
            ))
        )
    },
    WORDS: {                        # WORDS
        ATTR: ((                     # Attributes: 16-bit intiger as follows
            'SEYAME FLAG', (        # 0 SEYAME FLAG:
                'NO SEYAME',        #     0 NO SEYAME
                'SEYAME'            #     1 SEYAME
            )), (
            'ignore', None          # 1-4 ignore
            ), (
            'ENCLITIC FLAG', (      # 5 ENCLITIC FLAG:
                'NOT ENCLITIC',     #     0 NOT ENCLITIC
                'ENCLITIC'          #     1 ENCLITIC
            )), (
            'LEXEME FLAG', (        # 6 LEXEME FLAG:
                'NO',               #     0 NO
                'YES, i.e. = word represents lexeme'
                                    #     1 YES, i.e. = word represents lexeme
            ))
        ),
        FEAT: ((                    # Morphological Features: 32-bit intiger as follows
            '<RESERVED>', None      # 0-1 <RESERVED>
            ), (
            'SUFFIX GENDER', (      # 2-3 SUFFIX GENDER:
                'COMMON or <NONE>', #     00 COMMON or <NONE>
                'MASCULINE',        #     01 MASCULINE
                'SUFFEMININE'       #     10 SUFFEMININE
            )), (
            'SUFFIX PERSON', (      # 4-5 SUFFIX PERSON:
                '<NONE>',           #     00 <NONE>
                'THIRD',            #     01 THIRD
                'SECOND',           #     10 SECOND
                'FIRST'             #     11 FIRST
            )), (
            'SUFFIX NUMBER', (      # 6 SUFFIX NUMBER:
                'SINGULAR or <NONE>',
                                    #     0 SINGULAR or <NONE>
                'PLURAL'            #     1 PLURAL
            )), (
            'SUFFIX/CONTRACTION', ( # 7-8 SUFFIX/CONTRACTION:
                '<NONE>',           #     00 <NONE>
                'SUFFIX',           #     01 SUFFIX
                'CONTRACTION'       #     10 CONTRACTION
            )), (
            'PREFIX CODE', None     # 9-14 PREFIX CODE: 0-63
            ), (
            'GENDER', (             # 15-16 GENDER:
                '<NONE>',           #     00 <NONE>
                'COMMON',           #     01 COMMON
                'MASCULINE',        #     10 MASCULINE
                'FEMININE'          #     11 FEMININE
            )), (
            'PERSON', (             # 17-18 PERSON:
                '<NONE>',           #     00 <NONE>
                'THIRD',            #     01 THIRD
                'SECOND',           #     10 SECOND
                'FIRST'             #     11 FIRST
            )), (
            'NUMBER', (             # 19-20 NUMBER:
                '<NONE>',           #     00 <NONE>
                'SINGULAR',         #     01 SINGULAR
                'PLURAL'            #     10 PLURAL
            )), (
            'STATE', (              # 21-22 STATE:
                '<NONE>',           #     00 <NONE>
                'ABSOLUTE',         #     01 ABSOLUTE
                'CONSTRUCT',        #     10 CONSTRUCT
                'EMPHATIC'          #     11 EMPHATIC
            )), (
            'TENSE', (              # 23-25 TENSE:
                '<NONE>',           #     000 <NONE>
                'PERFECT',          #     001 PERFECT
                'IMPERFECT',        #     010 IMPERFECT
                'IMPERATIVE',       #     011 IMPERATIVE
                'INFINITIVE',       #     100 INFINITIVE
                'ACTIVE_PARTICIPLE',#     101 ACTIVE_PARTICIPLE
                'PASSIVE_PARTICIPLE',
                                    #     110 PASSIVE_PARTICIPLE
                'PARTICIPLES'       #     111 PARTICIPLES
            )), (
            'FORM', (               # 26-31 FORM:
                '<NONE>',           #     000000 <NONE>
                'PEAL',             #     000001 PEAL
                'ETHPEAL',          #     000010 ETHPEAL
                'PAEL',             #     000011 PAEL
                'ETHPAEL',          #     000100 ETHPAEL
                'APHEL',            #     000101 APHEL
                'ETTAPHAL',         #     000110 ETTAPHAL
                'SHAPHEL',          #     000111 SHAPHEL
                'ESHTAPHAL',        #     001000 ESHTAPHAL
                'SAPHEL',           #     001001 SAPHEL
                'ESTAPHAL',         #     001010 ESTAPHAL
                'PAUEL',            #     001011 PAUEL
                'ETHPAUAL',         #     001100 ETHPAUAL
                'PAIEL',            #     001101 PAIEL
                'ETHPAIAL',         #     001110 ETHPAIAL
                'PALPAL',           #     001111 PALPAL
                'ETHPALPAL',        #     010000 ETHPALPAL
                'PALPEL',           #     010001 PALPEL
                'ETHPALPAL',        #     010010 ETHPALPAL
                'PAMEL',            #     010011 PAMEL
                'ETHPAMAL',         #     010100 ETHPAMAL
                'PAREL',            #     010101 PAREL
                'ETHPARAL',         #     010110 ETHPARAL
                'PALI',             #     010111 PALI
                'ETHPALI',          #     011000 ETHPALI
                'PAHLI',            #     011001 PAHLI
                'ETHPAHLI',         #     011010 ETHPAHLI
                'TAPHEL',           #     011011 TAPHEL
                'ETHAPHAL'          #     011100 ETHAPHAL
            ))
        )
    },
    ENGLISH: {                      # ENGLISH
        ATTR: ((                     # Attributes: 15-bit intiger as follows:
            '<RESERVED>', None      # 0 <RESERVED>
            ), (
            'COMMENT POSITION', (   # 1 COMMENT POSITION:
                'COMMENT BEFORE MEANING',
                                    #     0 COMMENT BEFORE MEANING
                'COMMENT AFTER MEANING'
                                    #     1 COMMENT AFTER MEANING
            )), (
            'COMMENT FONT', (       # 2 COMMENT FONT:
                'NORMAL',           #     0 NORMAL
                'ITALIC'            #     1 ITALIC
            )), (
            'STRING BEFORE FONT', ( # 3 STRING BEFORE FONT: as above
                'NORMAL',           ##    0 NORMAL
                'ITALIC'            ##    1 ITALIC
            )), (
            'STRING AFTER FONT', (  # 4 STRING AFTER FONT: as above
                'NORMAL',           ##    0 NORMAL
                'ITALIC'            ##    1 ITALIC
            )), (
            'VERB TYPE', (          # 5-6 VERB TYPE:
                '<NONE>',           #     00 <NONE>
                'TRANSITIVE',       #     01 TRANSITIVE
                'INTRANSITIVE'      #     10 INTRANSITIVE
            )), (
            'NUMBER', (             # 7-8 NUMBER: as above
                '<NONE>',           ##    00 <NONE>
                'SINGULAR',         ##    01 SINGULAR
                'PLURAL'            ##    10 PLURAL
            )), (
            'GENDER', (             # 9-10 GENDER: as above
                '<NONE>',           ##    00 <NONE>
                'COMMON',           ##    01 COMMON
                'MASCULINE',        ##    10 MASCULINE
                'FEMININE'          ##    11 FEMININE
            )), (
            'FORM', None               # 11-15 FORM: as above
                # TODO: what forms are these?
                # Below the attested values:
                # (5 bits; the sixth bit is always 0)
                # 000001 1
                # 000010 2
                # 000011 3
                # 000100 4
                # 000101 5
                # 000110 6
                # 000111 7
                # 001000 8
                # 001001 9
                # 001101 13
                # 001110 14
                # 010000 16
                # 010010 18
                # 010110 22
            )
        )
    },
    ETIMOLGY: {                     # ETIMOLGY.TXT
        ATTR: ((                     # Attributes: 16-bit intigier as follows:
            'LANGUAGE', (           # 0-3 LANGUAGE:
                'SYRIAC',           #     0000  SYRIAC
                'AKKADIAN',         #     0001  AKKADIAN
                'ARAMAIC',          #     0010  ARAMAIC
                'ARABIC',           #     0011  ARABIC
                'ARMENIAN',         #     0100  ARMENIAN
                'GREEK',            #     0101  GREEK
                'HEBREW',           #     0110  HEBREW
                'LATIN',            #     0111  LATIN
                'PERSIAN',          #     1000  PERSIAN
                'SANSKRIT'          #     1001  SANSKRIT
            )), (
            'TYPE', (               # 4 TYPE:
                'NORMAL',           #     0 NORMAL
                'PARENTHESIED'      #     1 PARENTHESIED
            )), (
            'REST', None
            )
        )
    }
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
        attr_values = get_values(ANNOTATIONS[ROOTS][ATTR], attributes)

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
        attr_values = get_values(ANNOTATIONS[LEXEMES][ATTR], attributes)
        features = lexeme_features(feat)
        feat_values = get_values(ANNOTATIONS[LEXEMES][FEAT], features)

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
        attr_values = get_values(ANNOTATIONS[WORDS][ATTR], attributes)
        features = word_features(feat)
        feat_values = get_values(ANNOTATIONS[WORDS][FEAT], features)

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
        attr_values = get_values(ANNOTATIONS[ENGLISH][ATTR], attributes)

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
            'book_name':  BOOK_NAMES[book_id],          # string (e.g. 'Matt')
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
            #'attr_values': get_values(ANNOTATIONS[NT][ATTR], attributes) # TODO
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


def main2():
    for w_id, e in db['words'].items():
        print('{0:06b}'.format(e['features'][5]), e['cons_str'])

def main3():
    for w_id, e in db['nt'].items():
        if e['word_id'] == 625:
            print(w_id, e['book_name'], e['chapter'], e['verse'], e['word_num'])

def usage():
    print(__doc__)

if __name__ == "__main__":
        main3()
