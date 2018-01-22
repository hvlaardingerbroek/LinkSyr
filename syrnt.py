#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# now it works in python 2.7 and 3.x!
from __future__ import unicode_literals, print_function

# TODO: make it work in 2.6 (remove dict comprehension on line 278)
# TODO move data location to some yaml-ini-file

import os.path
from constants import SyrNT as c

DATADIR = '/home/gdwarf/projects/vu/LinkSyr/data/'
FILENAME = 'all-ordered.txt'

# TODO check discrepancies between SEDRA and Syromorph NT.
# It seems that
# 521601715
# 550104214
# 562103016
# 562302606
# 580201122
# 781901718
# 782202101
# 782202102
# 782202103
# 782202104
# 782202105
# 782202106
# 782202107
# 782202108

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
    # This can be done in a dict comprehension from Python 2.7 onward,
    # but 2.6 needs dict() constructor (https://stackoverflow.com/a/1747827)
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
    return c.ANNOTATIONS[17][1][a[17]]

def get_sentences(tr=towit):
    from io import open # This is for python 2.6 (TODO: why?)
    with open(os.path.join(DATADIR, FILENAME)) as f:
        for line in f:
            yield [wparse(w) for w in line.strip().translate(tr).split()]

def tag_sentences(sentences = None, tag=get_supertag):
    if sentences is None:
        sentences = get_sentences()
    for s in sentences:
        yield [(w, tag(a)) for w, a in s]

def get_verse_labels():
    for book_id, (book_name, chapters) in enumerate(c.NT_BOOKS, 52):
        for chapter, versecount in enumerate(chapters, 1):
            for verse in range(1, versecount + 1):
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


def main():
    for line in print_nt():
        print(line)

def usage():
    print(__doc__)

if __name__ == "__main__":
        main()
