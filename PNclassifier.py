from tensorflow.keras.models import load_model
import numpy as np

PNmodel = load_model("./model/best_model.h5")

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def PNclassifier(sentence):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(sentence)
    X_train = tokenizer.texts_to_sequences(sentence)
    train_X = pad_sequences(X_train, maxlen=80)

    sentiment = np.array(PNmodel.predict(train_X)).mean()
    if sentiment < 0.5:
        return -1
    elif sentiment == 0.5:
        return 0
    else:
        return 1

if __name__ == "__main__":
    print(PNclassifier("정말 짜증나네요"))