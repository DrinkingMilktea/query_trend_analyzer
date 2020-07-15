from gensim.models.word2vec import Word2Vec
import pandas as pd
import multiprocessing
coreNum = multiprocessing.cpu_count()
stopword = set(open("./data/stop_word_korean.txt").read().split())

from konlpy.tag import Okt
tokenizer = Okt()
def word2noun(sentence):
    tempX = tokenizer.morphs(sentence)
    ret = [word for word in tempX if not word in stopword]
    return ret

def trainingModel(quary):
    data = pd.read_csv('./data/' + quary + 'data.csv')
    data['tokened'] = data['crawled'].apply(word2noun)

    sentencelist = data['tokened'].tolist()
    w2v_model = Word2Vec(min_count=3, window=2, size=100, workers=coreNum-1, iter=100, sg=1)
    w2v_model.build_vocab(sentencelist)
    w2v_model.train(sentencelist, epochs=w2v_model.iter, total_examples=w2v_model.corpus_count)
    w2v_model.save("./model/" + quary + "word2vec.model")
    try:
        similarWord = w2v_model.wv.most_similar(positive=quary.split(), topn=20)
    except:
        return -1
    return similarWord


if __name__ == "__main__":
    trainingModel("CJ 제일제당")