# -*- coding: utf-8 -*-
import sqlite3
import random
import numpy as np
import MeCab

class Sql:
    dbname = '../word2vec.db'
    conn = sqlite3.connect(dbname)
    conn.text_factory = str
    c = conn.cursor()

    def select(self, get_words_n):
        wi_a = np.random.randint(0,100000,get_words_n)
        result = []
        for wi in wi_a:
                for row in self.c.execute('select word from wiki_plus_articles_vocab_control where word_index == {0}'.format(wi)):
                        result.append(row[0])

        return result

if __name__ == '__main__':
	sql = Sql()
	results = sql.select(40)
	for w in results:
		print(w)

test_sentence = '犬山dtm'

    


def test04(s):
    tagger = MeCab.Tagger('-Oyomi')
    result = tagger.parse(s)
    print result
    
test04(test_sentence)

