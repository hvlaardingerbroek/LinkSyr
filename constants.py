# TODO add comments

#====================================================================
# SyrNT constants
#====================================================================
class SyrNT:
    NT_BOOKS = (
        ('Matt',   (25, 23, 17, 25, 48, 34, 29, 34, 38, 42, 30, 50, 58, 36,
                    39, 28, 27, 35, 30, 34, 46, 46, 39, 51, 46, 75, 66, 20)),
        ('Mark',   (45, 28, 35, 41, 43, 56, 37, 38, 50, 52, 33, 44, 37, 72,
                    47, 20)),
        ('Luke',   (80, 52, 38, 44, 39, 49, 50, 56, 62, 42, 54, 59, 35, 35,
                    32, 31, 37, 43, 48, 47, 38, 71, 56, 53)),
        ('John',   (51, 25, 36, 54, 47, 71, 53, 59, 41, 42, 57, 50, 38, 31,
                    27, 33, 26, 40, 42, 31, 25)),
        ('Acts',   (26, 47, 26, 37, 42, 15, 60, 40, 43, 48, 30, 25, 52, 28,
                    41, 40, 34, 28, 41, 38, 40, 30, 35, 27, 27, 32, 44, 31)),
        ('Rom',    (32, 29, 31, 25, 21, 23, 25, 39, 33, 21, 36, 21, 14, 23,
                    33, 27)),
        ('1Cor',   (31, 16, 23, 21, 13, 20, 40, 13, 27, 33, 34, 31, 13, 40,
                    58, 24)),
        ('2Cor',   (24, 17, 18, 18, 21, 18, 16, 24, 15, 18, 33, 21, 14)),
        ('Gal',    (24, 21, 29, 31, 26, 18)),
        ('Eph',    (23, 22, 21, 32, 33, 24)),
        ('Phil',   (30, 30, 21, 23)),
        ('Col',    (29, 23, 25, 18)),
        ('1Thess', (10, 20, 13, 18, 28)),
        ('2Thess', (12, 17, 18)),
        ('1Tim',   (20, 15, 16, 16, 25, 21)),
        ('2Tim',   (18, 26, 17, 22)),
        ('Titus',  (16, 15, 15)),
        ('Phlm',   (25,)),
        ('Heb',    (14, 18, 19, 16, 14, 20, 28, 13, 28, 39, 40, 29, 25)),
        ('James',  (27, 26, 18, 17, 20)),
        ('1Peter', (25, 25, 22, 19, 14)),
        ('2Peter', (21, 22, 18)),
        ('1John',  (10, 29, 24, 21, 21)),
        ('2John',  (13,)),
        ('3John',  (15,)),
        ('Jude',   (25,)),
        ('Rev',    (20, 29, 22, 11, 14, 17, 17, 13, 21, 11, 19, 17, 18, 20,
                    8, 21, 18, 24, 21, 15, 27, 20)))

    # SyroMorph Data format
    #
    # See also morph.app.SyriacDatum.java,
    # edu.byu.nlp.ccash.syriacmorphtag.gwt.SyrTagValues and the data files themselves.
    #
    # e.g., CTBA|CTBA#CTBA#CTB###0#0#0#3#1#0#2#0#0#2#0#0#2#0#0#0#0#0 ...
    #
    # On the left of the bar is the full token. On the right of the bar are the
    # annotations for that token.  All of the tokens in a verse are on the same line
    # separated by a space.
    #
    # The annotations are as follows:
    ANNOTATIONS = (             # <index> <name>
        ('stem', None),         #  0 stem
        ('lexeme', None),       #  1 lexeme (baseform)
        ('root', None),         #  2 root
        ('prefix', None),       #  3 prefix
        ('suffix', None),       #  4 suffix
        ('seyame', None),       #  5 seyame
        ('verbal_conjugation',  #  6 verb conjugation
            ('n/a',                 #  0 n/a
             'peal',                #  1 peal
             'ethpeal',             #  2 ethpeal
             'pael',                #  3 pael
             'ethpael',             #  4 ethpael
             'aphel',               #  5 aphel
             'ettaphal',            #  6 ettaphal
             'shaphel',             #  7 shaphel
             'eshtaphal',           #  8 eshtaphal
             'saphel',              #  9 saphel
             'estaphal',            # 10 estaphal
             'pauel',               # 11 pauel
             'ethpaual',            # 12 ethpaual
             'paiel',               # 13 paiel
             'ethpaial',            # 14 ethpaial
             'palpal',              # 15 palpal
             'ethpalpal',           # 16 ethpalpal
             'palpel',              # 17 palpel
             'ethpalpal2',          # 18 ethpalpal2
             'pamel',               # 19 pamel
             'ethpamel',            # 20 ethpamel
             'parel',               # 21 parel
             'ethparal',            # 22 ethparal
             'pali',                # 23 pali
             'ethpali',             # 24 ethpali
             'pahli',               # 25 pahli
             'ethpahli',            # 26 ethpahli
             'taphel',              # 27 taphel
             'ethaphal')            # 28 ethaphal
        ),
        ('aspect',              #  7 aspect
            ('n/a',                 # 0 n/a
             'perfect',             # 1 perfect
             'imperfect',           # 2 imperfect
             'imperative',          # 3 imperative
             'infinitive',          # 4 infinitive
             'participle')          # 5 participle
        ),
        ('state',               #  8 state
            ('n/a',                 # 0 n/a
             'absolute',            # 1 absolute
             'construct',           # 2 construct
             'emphatic')            # 3 emphatic
        ),
        ('number',              #  9 number
            ('n/a',                 # 0 n/a
             'singular',            # 1 singular
             'plural')              # 2 plural
        ),
        ('person',              # 10 person
            ('n/a',                 # 0 n/a
             'first',               # 1 first
             'second',              # 2 second
             'third')               # 3 third
        ),
        ('gender',              # 11 gender
            ('n/a',                 # 0 n/a
             'common',              # 1 common
             'masculine',           # 2 masculine
             'feminine')            # 3 feminine
        ),
        ('pronoun_type',        # 12 pronoun type
            ('n/a',                 # 0 n/a
             'personal',            # 1 personal
             'demonstrative',       # 2 demonstrative
             'interrogative')       # 3 interrogative
        ),
        ('demonstrative_category',
                                    # 13 demonstrative category
            ('n/a',                 # 0 n/a
             'near',                # 1 near
             'far')                 # 2 far
        ),
        ('noun_type',           # 14 noun type
            ('n/a',                 # 0 n/a
             'propper',             # 1 propper
             'common')              # 2 common
        ),
        ('numeral_type',        # 15 numeral type
            ('n/a',                 # 0 n/a
             'cardinal',            # 1 cardinal
             'ordinal',             # 2 ordinal
             'cipher')              # 3 cipher
        ),
        ('participle_type',     # 16 participle type
            ('n/a',                 # 0 n/a
             'active',              # 1 active
             'passive')             # 2 passive
        ),
        ('grammatical_category',# 17 grammatical category
            ('verb',                # 0 verb
             'participle',          # 1 participle
             'noun',                # 2 noun
             'pronoun',             # 3 pronoun
             'numeral',             # 4 numeral
             'adjective',           # 5 adjective
             'particle',            # 6 particle
             'adverb',              # 7 adverb
             'idiom')               # 8 idiom
        ),
        ('suffix_contraction',  # 18 suffix contraction
            ('n/a',                 # 0 n/a
             'suffix',              # 1 suffix
             'contraction')         # 2 contraction
        ),
        ('suffix_gender',       # 19 suffix gender
            ('common OR n/a',       # 0 common OR n/a
             'masculine',           # 1 masculine
             'feminine')            # 2 feminine
        ),
        ('suffix_person',       # 20 suffix person
            ('n/a',                 # 0 n/a
             'first',               # 1 first
             'second',              # 2 second
             'third')               # 3 third
        ),
        ('suffix_number',       # 21 suffix number
            ('singular OR n/a',     # 0 singular OR n/a
             'plural')              # 1 plural
        ),
        ('feminine he dot',     # 22 feminine he dot
            ('does not have the feminine he dot',
                                    # 0 does not have the feminine he dot
             'has the feminine he dot')
                                    # 1 has the feminine he dot
        )
    )
