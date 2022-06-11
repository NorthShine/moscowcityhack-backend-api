import re
from string import punctuation

from gensim.models.doc2vec import Doc2Vec
from nltk.corpus import stopwords
import nltk
from pymystem3 import Mystem
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')

MODEL_PATH = '/second_4tb/kuchuganova/other/fake_news/d2v.model'
vec_size = 40
alpha = 0.025

mystem = Mystem()
russian_stopwords = stopwords.words("russian")

model = Doc2Vec(vector_size=vec_size,
                alpha=alpha,
                min_alpha=0.00025,
                min_count=4,
                dm=1,
                workers=4)

model = Doc2Vec.load(MODEL_PATH)


def preprocess_text(text, russian_stopwords=russian_stopwords):
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.lower().split(' ')
    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation]

    text = " ".join(tokens)

    return text


def comp_cosine_similarity(text1, text2, model=model):
    text1 = preprocess_text(text1)
    text2 = preprocess_text(text2)
    data = [text1, text2]
    vectors = [model.infer_vector([word for word in sent]).reshape(1, -1) for sent in data]
    return cosine_similarity(vectors[0], vectors[1])[0][0]


if __name__ == '__main__':
    tx1 = 'Mосква заняла первое место среди европейских городов в рейтинге инноваций, помогающих в борьбе с COVID-19'
    tx2 = 'Москва стала лидером в Европе в рейтинге инноваций, помогающих в борьбе с COVID-19'
    ccs = comp_cosine_similarity(tx1, tx2)
    print(ccs)
