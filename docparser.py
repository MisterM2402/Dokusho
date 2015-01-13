import xml.etree.cElementTree as ET
import itertools


def fromstringlist(sequence, parser=None):
    """
    Taken from Python2.7 source
    """
    if not parser:
        parser = ET.XMLParser(target=ET.TreeBuilder())
    for text in sequence:
        parser.feed(text)
    return parser.close()

if __name__ == '__main__':
    f = open('../corpora/nyt_eng_2010/nyt_eng_201001')
    it = itertools.chain('<root>', f, '</root>')
    root = fromstringlist(it)
    docs = root.findall('./DOC')
    doc_list = []
    for d in docs:
        doc_info = {}
        if d.attrib['type'] == 'story':
            doc_info['id'] = d.attrib['id']
            doc_info['headline'] = d.findtext('./HEADLINE').strip()
            doc_list.append(doc_info)

    for di in doc_list[:5]:
        print di
