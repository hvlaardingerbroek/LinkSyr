#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# now it works in python 2.6 and 3.x!
from __future__ import unicode_literals, print_function

import os.path
from constants import NT_BOOKS, SyrNT as c

# Read database location from config file
try: # allow for different module names in python 2 and 3
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

config = ConfigParser()
config.read('linksyr.conf')
datadir = config.get('syrnt','datadir')
filename = config.get('syrnt','filename')
dbpath = os.path.join(datadir, filename)
NT_OFFSET = 52  # starting id of NT books

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


class NTWord:
    def __init__(self, w_str, location):
        self.location = location
        self.cons_str, a_str = w_str.split('|')
        self.annotation = tuple( int(v) if v.isdigit() else v
                                        for v in a_str.split('#') )

    def __repr__(self):
        return '<NTWord {0}: {1}>'.format(self.loc_str, self.cons_str)

    def __str__(self):
        return self.cons_str

    @property
    def book_id(self):
        return self.location[0]

    @property
    def book_name(self):
        return NT_BOOKS[self.book_id - NT_OFFSET][0]

    @property
    def chapter(self):
        return self.location[1]

    @property
    def verse(self):
        return self.location[2]

    @property
    def w_num(self):
        return self.location[3]

    @property
    def loc_str(self):
        '''Combine location elements into fixed-length string'''
        return '{0:02}{1:02}{2:03}{3:02}'.format(*self.location)
        # return get_loc_id(self.book_id, self.chapter, self.verse, self.w_num)

    @property
    def stem(self):
        return self.annotation[0]

    @property
    def lexeme(self):
        return self.annotation[1]

    @property
    def root(self):
        return self.annotation[2]

    @property
    def prefix(self):
        return self.annotation[3]

    @property
    def suffix(self):
        return self.annotation[4]

    @property
    def seyame(self):
        return self.annotation[5]

    @property
    def ann_values(self):
        '''Return dictionary with descriptive key:value annotations'''
        # This can be done in a dict comprehension from Python 2.7 onward,
        # but 2.6 needs dict() constructor (https://stackoverflow.com/a/1747827)
        return dict( (l[0], (l[1][n]) if l[1] else n)
                    for l, n in zip(c.ANNOTATIONS, self.annotation) )

    @property
    def postag(self):
        # Part of Speech, or grammatical category, is annotation field 17
        return c.ANNOTATIONS[17][1][self.annotation[17]]


def get_verse_labels():
    for book_id, (book_name, chapters) in enumerate(NT_BOOKS, NT_OFFSET):
        for chapter, versecount in enumerate(chapters, 1):
            for verse in range(1, versecount + 1):
                yield (book_name, book_id, chapter, verse)

def nt_verses():
    from io import open # This is for python 2.6 (TODO: why?)
    with open(dbpath) as f:
        for verse_label, line in zip(get_verse_labels(), f):
            yield (verse_label,
                   [ NTWord(w_str, verse_label[1:] + (w_num,))
                     for w_num, w_str in enumerate(line.strip().split(), 1) ])

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

def get_supertag(w):
    return '+'.join([e for e in (w.prefix, w.postag, w.suffix) if e])

def tag_sentences(tr=towit, tag=get_supertag):
    for l, s in nt_verses():
        yield [(w.cons_str.translate(tr), tag(w)) for w in s]

def main():
    for line in print_nt():
        print(line)

def usage():
    print(__doc__)

if __name__ == "__main__":
        main()
