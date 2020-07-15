from newcollactor import newcollactor
from PNclassifier import PNclassifier
from word2vec_train import trainingModel
import numpy as np

def QTA():
    quary = str(input("원하는 검색어를 입력하시오 : "))
    print("news 수집중입니다.......")
    newcollactor(quary)
    print("news 수집이 완료되었습니다.")
    print("news 내용에서 검색어(" + quary + ")와 가장 가까운 단어를 찾고 있습니다.")
    similarWord = trainingModel(quary)
    if similarWord == -1:
        from gensim.models.word2vec import Word2Vec
        w2vModel = Word2Vec.load("./model/" + quary + "word2vec.model")
        while True:
            try:
                newquary = input("비슷한 단어를 찾기 위해 다른 단어를 입력해주세요 : ")
                similarWord = w2vModel.wv.most_similar(positive=newquary.split(), topn=20)
                break
            except:
                continue
    print(similarWord)
    print("위 단어들의 긍부정 정도를 탐색합니다.\n\n")
    print("부정은 -1, 긍정은 1에 가까워집니다.")
    print(quary, "와 관련된 단어들의 긍부정 분포를 나열합니다.")
    for word, probability in similarWord:
        sentiment_result = list()
        print(word)
        print("news 수집중입니다.......")
        rawdata = newcollactor(word)
        print("news 수집이 완료되었습니다.")
        for sentence in rawdata['crawled']:
            sentiment_result.append(PNclassifier(sentence))
        sentiment_mean = np.array(sentiment_result).mean()
        print(word, "의 감정분포는 ", sentiment_mean, "입니다.")

if __name__ == "__main__":
    QTA()
