from typing import List

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

# выполнить в терминале перед запуском, после установки requirements.txt
# !python -m dostoevsky download fasttext-social-network-model
from text_analysis.summarizator import get_summary

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


def compare_tone(source, entry_article):
    """
        Entry article to source tone comparison
        negative entry_tone_difference stands for
            entry text is X percents more negative
        positive entry_tone_difference stands for
            entry text is X percents more positive"""

    source_tone, data_tone = get_text_tone([source, entry_article])
    pos_diff = source_tone['positive'] - data_tone['positive']
    neg_diff = source_tone['negative'] - data_tone['negative']
    if (abs(neg_diff) > abs(pos_diff)) and neg_diff < 0:
        return {"entry_tone_difference": round(abs(neg_diff)*100)}
    elif (abs(neg_diff) < abs(pos_diff)) and pos_diff > 0:
        return {"entry_tone_difference": -round(abs(pos_diff)*100)}
    else:
        return {"entry_tone_difference": 0}


if __name__ == '__main__':
    print(compare_tone(messages[0], messages[1]))
