import re
#from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import gutenberg


class ReadabilityText():

    def __init__(self, text):
        self.words = re.split(r'\W+', text)  # word_tokenize(text)
        self.stemmed_words = [SnowballStemmer('english').stem(w) for w in self.words]
        self.poly_syl_words = [w for w in self.words if syl_count(w) > 2]
        self.sents = re.split(r'[.!?]+\W+', text)  # sent_tokenize(text)
        self.len = len(self.words)
        self.avg_sent_len = calc_avg_sent_len(self.sents)
        self.avg_syl = calc_avg_syl(self.words)


def flesch_kincaid(r_text):
    return 0.39 * r_text.avg_sent_len + 11.8 * r_text.avg_syl - 15.59


def dale_chall(r_text, easy_words):
    words = r_text.stemmed_words
    easy_words = set(easy_words) & set([w.lower() for w in words])
    #print set([w.lower() for w in words]) - easy_words
    dw_count = 0
    for w in words:
        if w.lower() not in easy_words:
            dw_count += 1
    dw_percentage = dw_count * 100.0 / r_text.len
    adjust = 0
    if dw_percentage > 5:
        adjust = 3.6365
    return 0.1579 * dw_percentage + 0.0496 * r_text.avg_sent_len + adjust


def gunning_fog(r_text):
    return 0.4 * (r_text.avg_sent_len + 100 * len(r_text.poly_syl_words) / len(r_text.words))


def calc_avg_sent_len(sents):
    sent_lens = []
    for s in sents:
        sent_lens.append(len(re.split(r'\W+', s)))
    return sum(sent_lens) / len(sents)


def syl_count(word):
    vowels = 'aeiouy'
    w = word.lower()
    prev_l = 'x'
    count = 0
    for l in w:
        if prev_l not in vowels and l in vowels:
            count += 1
        prev_l = l
    if len(w) > 2 and w[-2] not in vowels and w[-1] == 'e':
        count -= 1
    return count


def syl_count_all(words):
    count = 0
    for w in words:
        count += syl_count(w)
    return count


def calc_avg_syl(words):
    return 1.0 * syl_count_all(words) / len(words)


if __name__ == '__main__':
    text1 = """CHAPTER I. Down the Rabbit-Hole

Alice was beginning to get very tired of sitting by her sister on the
bank, and of having nothing to do: once or twice she had peeped into the
book her sister was reading, but it had no pictures or conversations in
it, 'and what is the use of a book,' thought Alice 'without pictures or
conversation?'

So she was considering in her own mind (as well as she could, for the
hot day made her feel very sleepy and stupid), whether the pleasure
of making a daisy-chain would be worth the trouble of getting up and
picking the daisies, when suddenly a White Rabbit with pink eyes ran
close by her.

There was nothing so VERY remarkable in that; nor did Alice think it so
VERY much out of the way to hear the Rabbit say to itself, 'Oh dear!
Oh dear! I shall be late!' (when she thought it over afterwards, it
occurred to her that she ought to have wondered at this, but at the time
it all seemed quite natural); but when the Rabbit actually TOOK A WATCH
OUT OF ITS WAISTCOAT-POCKET, and looked at it, and then hurried on,
Alice started to her feet, for it flashed across her mind that she had
never before seen a rabbit with either a waistcoat-pocket, or a watch
to take out of it, and burning with curiosity, she ran across the field
after it, and fortunately was just in time to see it pop down a large
rabbit-hole under the hedge.

In another moment down went Alice after it, never once considering how
in the world she was to get out again.

The rabbit-hole went straight on like a tunnel for some way, and then
dipped suddenly down, so suddenly that Alice had not a moment to think
about stopping herself before she found herself falling down a very deep
well."""

    with open('DaleChallStemmed.txt', 'r') as dcewl_file:
        easy_words = [w.strip() for w in dcewl_file.readlines()]

    r_text1 = ReadabilityText(text1)
    print 'Alice extract', syl_count_all(r_text1.words), calc_avg_syl(r_text1.words),\
        flesch_kincaid(r_text1), dale_chall(r_text1, easy_words), gunning_fog(r_text1)

    #for fid in gutenberg.fileids():
    fid = 'carroll-alice.txt'
    r_text = ReadabilityText(gutenberg.raw(fid))
        #if fid == 'carroll-alice.txt':
    print fid, flesch_kincaid(r_text), dale_chall(r_text, easy_words), gunning_fog(r_text)
        #print fid, len(text.split()), syl_count(text), calc_avg_syl(text)
        #print fid, calc_avg_sent_len(text), alt_avg_sent_len(text)