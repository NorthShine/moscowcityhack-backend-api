from typing import List

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

# выполнить в терминале перед запуском, после установки requirements.txt
# !python -m dostoevsky download fasttext-social-network-model
from src.text_analysis.summarizator import get_summary

tokenizer = RegexTokenizer()

model = FastTextSocialNetworkModel(tokenizer=tokenizer)

messages = ['барак обама ужасно поет',
            'лучшее продолжение ковида это обезьянья оспа']


def get_text_tone(messages: List, model=model):  # firs orig news second checking news, please
    results = model.predict(messages, k=5)
    res = []
    for message, sentiment in zip(messages, results):
        res.append(sentiment)
    return res  # список из словарей каждый из которых обязательно содержит ключи 'negative' и 'positive'


def compare_tone(source, data):
    source_sum = get_summary(source)
    data_sum = get_summary(data)
    source_tone, data_tone = get_text_tone([source_sum,data_sum])
    pos_diff = source_tone['positive'] - data_tone['positive']
    neg_diff = source_tone['negative'] - data_tone['negative']
    if (abs(neg_diff) > abs(pos_diff)) and neg_diff < 0:
        return f'Введенная новость на {round(abs(neg_diff)*100)}% более негативна.'
    elif (abs(neg_diff) < abs(pos_diff)) and pos_diff > 0:
        return f'Введенная новость на {round(abs(pos_diff)*100)}% более негативна.'
    else:
        return f'Тональности новостей совпадают.'


if __name__ == '__main__':
    print(compare_tone(messages[0], messages[1]))
