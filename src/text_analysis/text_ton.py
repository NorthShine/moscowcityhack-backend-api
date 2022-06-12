from typing import List

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

# выполнить в терминале перед запуском, после установки requirements.txt
# !python -m dostoevsky download fasttext-social-network-model

tokenizer = RegexTokenizer()

model = FastTextSocialNetworkModel(tokenizer=tokenizer)

messages = ['барак обама ужасно поет',
            'лучшее продолжение ковида это обезьянья оспа']


def get_text_tone(messages: List, model=model):  # firs orig news second checking news, please
    results = model.predict(messages, k=3)
    res = []
    for message, sentiment in zip(messages, results):
        res.append(sentiment)
    return res  # список из словарей каждый из которых обязательно содержит ключи 'negative' и 'positive'


if __name__ == '__main__':
    print(get_text_tone(messages))
