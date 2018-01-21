#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# now it works in python 2.7 and 3.x!
from __future__ import unicode_literals, print_function

# TODO: make it work in 2.6 (remove dict comprehension on line 278)
# TODO move data location to some yaml-ini-file
# TODO move constants to constants file?
# TODO upload to github

import os.path
from constants import SyrNT as c


DATADIR = '/home/gdwarf/projects/vu/LinkSyr/data/'
FILENAME = 'all-ordered.txt'

# NT_BOOKS = (
#     ('Matt',   '25 23 17 25 48 34 29 34 38 42 30 50 58 36 39 ' \
#                '28 27 35 30 34 46 46 39 51 46 75 66 20'),
#     ('Mark',   '45 28 35 41 43 56 37 38 50 52 33 44 37 72 47 20'),
#     ('Luke',   '80 52 38 44 39 49 50 56 62 42 54 59 35 35 32 ' \
#                '31 37 43 48 47 38 71 56 53'),
#     ('John',   '51 25 36 54 47 71 53 59 41 42 57 50 38 31 27 ' \
#                '33 26 40 42 31 25'),
#     ('Acts',   '26 47 26 37 42 15 60 40 43 48 30 25 52 28 41 ' \
#                '40 34 28 41 38 40 30 35 27 27 32 44 31'),
#     ('Rom',    '32 29 31 25 21 23 25 39 33 21 36 21 14 23 33 27'),
#     ('1Cor',   '31 16 23 21 13 20 40 13 27 33 34 31 13 40 58 24'),
#     ('2Cor',   '24 17 18 18 21 18 16 24 15 18 33 21 14'),
#     ('Gal',    '24 21 29 31 26 18'),
#     ('Eph',    '23 22 21 32 33 24'),
#     ('Phil',   '30 30 21 23'),
#     ('Col',    '29 23 25 18'),
#     ('1Thess', '10 20 13 18 28'),
#     ('2Thess', '12 17 18'),
#     ('1Tim',   '20 15 16 16 25 21'),
#     ('2Tim',   '18 26 17 22'),
#     ('Titus',  '16 15 15'),
#     ('Phlm',   '25'),
#     ('Heb',    '14 18 19 16 14 20 28 13 28 39 40 29 25'),
#     ('James',  '27 26 18 17 20'),
#     ('1Peter', '25 25 22 19 14'),
#     ('2Peter', '21 22 18'),
#     ('1John',  '10 29 24 21 21'),
#     ('2John',  '13'),
#     ('3John',  '15'),
#     ('Jude',   '25'),
#     ('Rev',    '20 29 22 11 14 17 17 13 21 11 19 17 18 20 8 ' \
#                '21 18 24 21 15 27 20'))
#
# # TODO check discrepancies between SEDRA and Syromorph NT.
# # It seems that
# # 521601715
# # 550104214
# # 562103016
# # 562302606
# # 580201122
# # 781901718
# # 782202101
# # 782202102
# # 782202103
# # 782202104
# # 782202105
# # 782202106
# # 782202107
# # 782202108
#
# # NT_VERSES tuple replaced by generator: get_verse_labels()
# # NT_VERSES = tuple( (book_id, book_name, chapter, verse)
# #     for book_id, (book_name, chapters) in enumerate(NT_BOOKS, 52)
# #         for chapter, versecount in enumerate(chapters.split(), 1)
# #             for verse in range(1, int(versecount) + 1) )
#
# # SyroMorph Data format
# #
# # See also morph.app.SyriacDatum.java,
# # edu.byu.nlp.ccash.syriacmorphtag.gwt.SyrTagValues and the data files themselves.
# #
# # e.g., CTBA|CTBA#CTBA#CTB###0#0#0#3#1#0#2#0#0#2#0#0#2#0#0#0#0#0 ...
# #
# # On the left of the bar is the full token. On the right of the bar are the
# # annotations for that token.  All of the tokens in a verse are on the same line
# # separated by a space.
# #
# # The annotations are as follows:
# # <index> <name>
# #  0 stem
# #  1 lexeme (baseform)
# #  2 root
# #  3 prefix
# #  4 suffix
# #  5 seyame
# #  6 verb conjugation
# #  7 aspect
# #  8 state
# #  9 number
# # 10 person
# # 11 gender
# # 12 pronoun type
# # 13 demonstrative category
# # 14 noun type
# # 15 numeral type
# # 16 participle type
# # 17 grammatical category
# # 18 suffix contraction
# # 19 suffix gender
# # 20 suffix person
# # 21 suffix number
# # 22 feminine he dot
# #
# # The tagsets for annotations 5 through 22 are described below:
# #
# ANNOTATIONS = (
#     ('stem', None),
#     ('lexeme', None),
#     ('root', None),
#     ('prefix', None),
#     ('suffix', None),
#     ('seyame', None),
#     ('verbal_conjugation',  # verbal_conjugation
#         ('n/a',             # 0 n/a
#          'peal',            # 1 peal
#          'ethpeal',         # 2 ethpeal
#          'pael',            # 3 pael
#          'ethpael',         # 4 ethpael
#          'aphel',           # 5 aphel
#          'ettaphal',        # 6 ettaphal
#          'shaphel',         # 7 shaphel
#          'eshtaphal',       # 8 eshtaphal
#          'saphel',          # 9 saphel
#          'estaphal',        # 10 estaphal
#          'pauel',           # 11 pauel
#          'ethpaual',        # 12 ethpaual
#          'paiel',           # 13 paiel
#          'ethpaial',        # 14 ethpaial
#          'palpal',          # 15 palpal
#          'ethpalpal',       # 16 ethpalpal
#          'palpel',          # 17 palpel
#          'ethpalpal2',      # 18 ethpalpal2
#          'pamel',           # 19 pamel
#          'ethpamel',        # 20 ethpamel
#          'parel',           # 21 parel
#          'ethparal',        # 22 ethparal
#          'pali',            # 23 pali
#          'ethpali',         # 24 ethpali
#          'pahli',           # 25 pahli
#          'ethpahli',        # 26 ethpahli
#          'taphel',          # 27 taphel
#          'ethaphal')        # 28 ethaphal
#     ),
#     ('aspect',              # aspect
#         ('n/a',             # 0 n/a
#          'perfect',         # 1 perfect
#          'imperfect',       # 2 imperfect
#          'imperative',      # 3 imperative
#          'infinitive',      # 4 infinitive
#          'participle')      # 5 participle
#     ),
#     ('state',               # state
#         ('n/a',             # 0 n/a
#          'absolute',        # 1 absolute
#          'construct',       # 2 construct
#          'emphatic')        # 3 emphatic
#     ),
#     ('number',              # number
#         ('n/a',             # 0 n/a
#          'singular',        # 1 singular
#          'plural')          # 2 plural
#     ),
#     ('person',              # person
#         ('n/a',             # 0 n/a
#          'first',           # 1 first
#          'second',          # 2 second
#          'third')           # 3 third
#     ),
#     ('gender',              # gender
#         ('n/a',             # 0 n/a
#          'common',          # 1 common
#          'masculine',       # 2 masculine
#          'feminine')        # 3 feminine
#     ),
#     ('pronoun_type',        # pronoun_type
#         ('n/a',             # 0 n/a
#          'personal',        # 1 personal
#          'demonstrative',   # 2 demonstrative
#          'interrogative')   # 3 interrogative
#     ),
#     ('demonstrative_category',
#                             # demonstrative_category
#         ('n/a',             # 0 n/a
#          'near',            # 1 near
#          'far')             # 2 far
#     ),
#     ('noun_type',           # noun_type
#         ('n/a',             # 0 n/a
#          'propper',         # 1 propper
#          'common')          # 2 common
#     ),
#     ('numeral_type',        # numeral_type
#         ('n/a',             # 0 n/a
#          'cardinal',        # 1 cardinal
#          'ordinal',         # 2 ordinal
#          'cipher')          # 3 cipher
#     ),
#     ('participle_type',     # participle_type
#         ('n/a',             # 0 n/a
#          'active',          # 1 active
#          'passive')         # 2 passive
#     ),
#     ('grammatical_category',# grammatical_category
#         ('verb',            # 0 verb
#          'participle',      # 1 participle
#          'noun',            # 2 noun
#          'pronoun',         # 3 pronoun
#          'numeral',         # 4 numeral
#          'adjective',       # 5 adjective
#          'particle',        # 6 particle
#          'adverb',          # 7 adverb
#          'idiom')           # 8 idiom
#     ),
#     ('suffix_contraction',  # suffix_contraction
#         ('n/a',             # 0 n/a
#          'suffix',          # 1 suffix
#          'contraction')     # 2 contraction
#     ),
#     ('suffix_gender',       # suffix_gender
#         ('common OR n/a',   # 0 common OR n/a
#          'masculine',       # 1 masculine
#          'feminine')        # 2 feminine
#     ),
#     ('suffix_person',       # suffix_person
#         ('n/a',             # 0 n/a
#          'first',           # 1 first
#          'second',          # 2 second
#          'third')           # 3 third
#     ),
#     ('suffix_number',       # suffix_number
#         ('singular OR n/a', # 0 singular OR n/a
#          'plural')          # 1 plural
#     ),
#     ('feminine he dot',     # feminine he dot
#         ('does not have the feminine he dot',
#                             # 0 does not have the feminine he dot
#          'has the feminine he dot')
#                             # 1 has the feminine he dot
#     )
# )


# def maketrans(str1, str2):
#     if hasattr(str, 'maketrans') and callable(getattr(str, 'maketrans')):
#         return str.maketrans(str1, str2)
#     else:
#         import string
#         return string.maketrans(str1, str2)
#
# above stuff does not work in python 2.
# better to make own simple maketrans function:
def maketrans(s1, s2):
    '''Make a simple translation table'''
    return dict(zip([ord(a) for a in s1], [ord(a) for a in s2]))

# translation tables:
# source is always SEDRA transcription, so only need to specify 'to'.
towit = maketrans('AOKY;CEI/XW','>WXVJK<PYQC')
tosyr = maketrans('ABGDHOZKY;CLMNSEI/XRWT','ܐܒܓܕܗܘܙܚܛܝܟܠܡܢܣܥܦܨܩܪܫܬ')
notr = maketrans('','')


def get_loc_id(book_id, chapter, verse, word_num):
    '''Combine location elements into fixed-length string'''
    return '{:02}{:02}{:03}{:02}'.format(book_id, chapter, verse, word_num)

def split_loc_id(loc_id):
    '''Split loc_id into elements: '250100101' -> (25, 1, 1, 1)'''
    loc = [loc_id[:2], loc_id[2:4], loc_id[4:7], loc_id[7:]]
    return tuple(int(a) for a in loc)

def get_ann_values(a):
    '''Return dictionary with descriptive key:value annotations'''
    # a: annotation; l: ?; n: ?
    # return { l[0]:(l[1][n] if l[1] else n) for l, n in zip(ANNOTATIONS, a) }
    return dict( (l[0], (l[1][n]) if l[1] else n)
                    for l, n in zip(c.ANNOTATIONS, a) )

def aparse(a_str):
    '''Split annotation string into fields and return as tuple'''
    # a_str: annotation string; v: value
    return tuple( int(v) if v.isdigit() else v for v in a_str.split('#') )

def wparse(w):
    '''Split word field into word string and annotation, return tuple'''
    cons_str, a_str = w.split('|')
    return (cons_str, aparse(a_str))

def get_supertag(a):
    # a: annotation
    # prefix is annotation field 3, suffix is annotation field 4
    PoS = get_postag(a)
    prefix = a[3]+'+' if a[3] else ''
    suffix = '+'+a[4] if a[4] else ''
    return prefix+PoS+suffix

def get_postag(a):
    # Part of Speech, or grammatical category, is annotation field 17
    return ANNOTATIONS[17][1][a[17]]

def get_sentences(tr=towit):
    # sentences = []
    from io import open
    with open(os.path.join(DATADIR, FILENAME)) as f:
        for line in f:
            yield [wparse(w) for w in line.strip().translate(tr).split()]
            # sentence = []
            # # print(type(line))
            # for w in line.strip().split():
            #     # print(w)
            #     wtr=w.translate(tr)
            #     wp=wparse(wtr)
            #     sentence.append(wp)
            #     # sentence.append(wparse(w.translate(tr)))
            # yield sentence
            # sentences.append(sentence)
    # return sentences


def tag_sentences(sentences = None, tag=get_supertag):
    if sentences is None:
        sentences = get_sentences()
    for s in sentences:
        yield [(w, tag(a)) for w, a in s]
    # [(yield [(w,get_supertag(a)) for w, a in s]) for s in sentences] # werkt niet?
    # return [[(w,get_supertag(a)) for w, a in s] for s in sentences]
    # return [[(w,get_postag(a)) for w, a in s] for s in sentences]

def get_verse_labels():
    for book_id, (book_name, chapters) in enumerate(c.NT_BOOKS, 52):
        for chapter, versecount in enumerate(chapters.split(), 1):
            for verse in range(1, int(versecount) + 1):
                yield (book_id, book_name, chapter, verse)

def outputverses(tr=tosyr):
    for l,s in zip(get_verse_labels(), get_sentences(tr=notr)):
        ' '.join([w[0] for w in s]).translate(tr)
        yield (l, ' '.join([w[0] for w in s]).translate(tr))

def print_nt():
    # nt = []
    pl = None # pl: previous label
    for l,v in outputverses():
        if pl is None or pl[1] != l[1] or pl[2] != l[2]:
            if pl is not None:  # no newline before first chapter
                yield ''
                # nt.append('')   # add newline before chapter label
            yield '{} chapter {}'.format(l[1], l[2])
            # nt.append('{} chapter {}'.format(l[1], l[2])) # add chapter label
        pl = l
        yield '{:2} {}'.format(l[3], v)
        # nt.append('{:2} {}'.format(l[3], v))
    # return '\n'.join(nt)


# NLTK POS tagger results:
#
# from nltk.tag import UnigramTagger # etc...
# cpath=os.path.expanduser('~/nltk_data/corpora/syrnt')
# c=syrnt.tag_sentences()
# t='\n'.join([' '.join(['/'.join(w) for w in s]) for s in c])
# with open(os.path.join(cpath,'syrnt.pos'), 'w') as f:
#     f.write(t)
## output: 1417742
# reader = TaggedCorpusReader(cpath, r'.*\.pos')
# train_sents=reader.tagged_sents()[:5967]
# test_sents=reader.tagged_sents()[5967:]
# tagger2 = UnigramTagger(train_sents, backoff=tagger1)
# tagger2.evaluate(test_sents)
##output: 0.8217430693966298


# loc_pattern = '{:02}{:02}{:03}{:02}'

# db = {}
# with open(os.path.join(DATADIR, FILENAME)) as f:
#     for line, v in zip(f, NT_VERSES):
#         book_id, book_name, chapter, verse = v
#         for word_num, w in enumerate(line.strip().split(), 1):
#             # loc_id = loc_pattern.format(book_id, chapter, verse, word_num)
#             loc_id = get_loc_id(book_id, chapter, verse, word_num)
#             cons_str, a_string = w.split('|')
#             # annotation = tuple( int(val) if val.isdigit() else val
#             #                     for val in a_string.split('#') )
#             annotation = get_annotation(a_string)
#             # ann_values = { l[0]:(l[1][n] if l[1] else n)
#             #                 for l, n in zip(ANNOTATIONS, annotation) }
#             ann_values = get_ann_values(annotation)
#             db[int(loc_id)] = {
#                 'id':           loc_id,         # string (e.g. '520100101')
#                 'book_id':      book_id,        # integer ([52..78])
#                 'book_name':    book_name,      # string (e.g. 'Matt')
#                 'chapter':      chapter,        # integer
#                 'verse':        verse,          # integer
#                 'word_num':     word_num,       # integer
#                 'cons_str':     cons_str,       # string
#                 'annotation':   annotation,     # tuple
#                 'ann_values':   ann_values      # dict with string values
#             }
# nt = tuple(db[loc] for loc in sorted(db))

# def main():
#     for w_id in sorted(db):
#         e = db[w_id]
#         print(
#             e['book_name'],
#             e['chapter'],
#             e['verse'],
#             e['word_num'],
#             e['cons_str']
#         )

# def main():
#     prev_verse = 1
#     prev_chapter = 1
#     for w_id in sorted(db):
#         e = db[w_id]
#
#         # print newlines between chapters and verses
#         if e['chapter'] != prev_chapter:
#             print('\n\n{} {}'.format(e['book_name'], e['chapter']), end='')
#             prev_chapter = e['chapter']
#         if e['verse'] != prev_verse:
#             print('\n{} {} {} '.format(e['book_name'], e['chapter'], e['verse']), end='')
#             prev_verse = e['verse']
#         else:
#             print(' ', end='')
#
#         print(e['cons_str'], end = '')
#
#     print('') # print newlina after last verse

def main():
    for line in print_nt():
        print(line)

def usage():
    print(__doc__)

if __name__ == "__main__":
        main()
