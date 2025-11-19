"""
Анализ частотности слов в датасете Wikipedia.

ЗАДАНИЕ:
Загрузите датасет Wikipedia, проведите анализ частотности слов (исключая стоп-слова),
создайте облако слов и выполните анализ распределения по разделам.

ТРЕБОВАНИЯ:
- Загрузить датасет: load_dataset()
- Провести анализ частотности слов (исключить стоп-слова)
- Найти топ-30 слов
- Создать облако слов (wordcloud)
- Проанализировать статистику статей
- Сохранить результаты в wikipedia_results.json
"""

import json
import re
from collections import Counter
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from datasets import load_dataset
import matplotlib.pyplot as plt
from wordcloud import WordCloud


STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "will", "would", "could", "should", "may",
    "might", "must", "can", "this", "that", "these", "those", "i", "you",
    "he", "she", "it", "we", "they", "what", "which", "who", "when", "where",
    "why", "how", "all", "each", "every", "both", "few", "more", "most",
    "some", "any", "such", "as", "if", "so", "up", "out", "no", "not", "only"
}


# TODO: Ваш код здесь


def load_wikipedia_dataset():
    # TODO: Реализовать загрузку
    pass


def preprocess_text(text: str):
    # TODO: Реализовать, исключив STOPWORDS
    pass


def analyze_dataset_statistics(dataset):
    # TODO: Вернуть total_articles, avg_text_length, etc.
    pass


def extract_top_words(dataset, top_n: int = 30):
    # TODO: Реализовать
    pass


def create_wordcloud(dataset) :
    # TODO: Создать wordcloud и сохранить в "wikipedia_wordcloud.png"
    pass


def main():
    # TODO: Собрать анализ
    pass


if __name__ == "__main__":
    main()
