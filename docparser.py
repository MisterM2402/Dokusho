import xml.etree.cElementTree as ET
import itertools
import sqlite3
import re
import os
from collections import defaultdict


def fromstringlist(sequence, parser=None):
    """
    Taken from Python2.7 source
    """
    if not parser:
        parser = ET.XMLParser(target=ET.TreeBuilder())
    for text in sequence:
        parser.feed(text)
    return parser.close()


def row_generator(count_dict, stops):
    for t in sorted(count_dict):
        if t not in stops:
            posting = ''
            for doc_id in sorted(count_dict[t]):
                #print (t, doc_id, count_dict[t][doc_id])
                posting += doc_id + ' ' + str(count_dict[t][doc_id]) + ' '
            yield (t, posting)


if __name__ == '__main__':
    index_conn = sqlite3.connect('index.db')
    index_conn.row_factory = sqlite3.Row
    meta_conn = sqlite3.connect('metadata.db')
    meta_conn.row_factory = sqlite3.Row
    #meta_conn.isolation_level = None

    index_conn.execute('create table if not exists inv_index'
                       '(term text, posting text)')
    meta_conn.execute('create table if not exists metadata'
                      '(doc_id text primary key, filepath text, headline text, dateline text)')

    corpus_dir = 'nyt_eng_2010/'
    stops = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
                 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
                 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them',
                 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
                 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
                 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
                 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
                 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
                 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
                 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
                 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
                 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
                 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', ''])
    did = 'NYT_ENG_20100101.0001'
    story = """A memorial service will be held Wednesday for
            Mary Edwards, a suburban Granada Hills community activist and
            environmentalist, who died Dec. 7 after a long illness. She was 79.

            Edwards was a longtime supporter and spokeswoman for the North
            Valley Coalition of Concerned Citizens, a grass-roots organization
            that opposed the expansion of nearby Sunshine Canyon Landfill.

            "Mary was worried about the health of the community. She wanted
            to make the area safer, and she wouldn't give up. She motivated us
            to fight with her," said longtime friend and fellow activist Mary
            Anna Kienholz.

            Edwards was also the founder of LASER (Landfill Alternative Save
            Environmental Resources) and was an advocate for the acquisition of
            land for the Rim of the Valley and Bee Canyon Park.

            "She was very well-known in the community but she was humble.
            Doing for others was her nature. She was truly exceptional. We will
            miss her a whole lot," Kienholz said.

            In addition, Edwards was a founding member of Granada Hills
            North Neighborhood Council, active in the Granada Hills Women's
            Club and a supporter of the anti-poverty group Meet Each Need With
            Dignity.

            "Mary was a totally giving woman. She wore her heart on her
            sleeve. She cared about the homeless, the hungry, battered women,"
            said Wayde Hunter, president of the North Valley Coalition. "She
            fought like all-get-out for the community."

            Edwards is survived by her husband, George, and seven children.

            The memorial will be held at 3 p.m. Wednesday at the Episcopal
            Church of St. Andrew and St. Charles, 16651 Rinaldi St., Granada
            Hills.

            Memorial contributions can be made to MEND, 10641 N. San
            Fernando Road, Pacoima 91331 or other charity."""
    for w in set([t.lower() for t in re.split(r'\W+', story)]) - stops:
        count = 0
        tf = 0
        for row in index_conn.execute("select posting from inv_index where term = ?", (w,)):
            r = row[0].split()
            try:
                tf = r[r.index(did)+1]
            except ValueError:
                pass
            count += len(r) / 2
            #posting = dict(zip(r[::2], r[1::2]))
            #if did in set(posting):
            #    tf = posting[did]
            #count += len(posting)
        print w, tf, count

    #meta_conn.execute('begin')
    #for filename in os.listdir('corpora/' + corpus_dir)[:2]:
    #    f = open('corpora/' + corpus_dir + filename)
    #    it = itertools.chain('<root>', f, '</root>')
    #    root = fromstringlist(it)
    #    docs = root.findall('./DOC')
    #    headlines = set([])
    #    doc_data_list = []
    #    counts = defaultdict(lambda: defaultdict(int))
    #    for d in docs:
    #        if d.attrib['type'] == 'story':
    #            doc_id = d.attrib['id']
    #            print doc_id
    #
    #            hl = d.findtext('./HEADLINE')
    #            if hl is not None:
    #                hl = hl.strip()
    #
    #            dl = d.findtext('./DATELINE')
    #            if dl is not None:
    #                dl = dl.strip()
    #
    #            text_node = d.find('./TEXT')
    #            text = ''
    #            for p in text_node.findall('./P'):
    #                text += p.text
    #            text = text.strip()
    #
    #            if hl not in headlines:
    #                doc_data_list.append((doc_id, corpus_dir + filename, hl, dl))
    #                if hl is not None:
    #                    headlines.add(hl)
    #
    #            tokens = [t.lower() for t in re.split(r'\W+', text)]
    #            for t in tokens:
    #                counts[t][doc_id] += 1
    #
    #    with meta_conn:
    #        meta_conn.executemany('insert into metadata values (?, ?, ?, ?)', doc_data_list)
    #
    #    with index_conn:
    #        index_conn.executemany('insert into inv_index values (?, ?)',
    #                               row_generator(counts, stops))

    #meta_conn.execute('commit')
    #for row in meta_conn.execute('select count(*) from metadata where dateline = "TOKYO"'):
    #    print row

    #with open('dump.sql', 'w') as f:
    #    for line in meta_conn.iterdump():
    #        f.write('%s\n' % line)

    #for row in index_conn.execute("select * from inv_index where term = 'Xinhua'"):
    #    print row
    #for dp in doc_list[:1]:
    #    print dp