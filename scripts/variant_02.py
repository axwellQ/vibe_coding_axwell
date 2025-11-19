"""
Классификация новостей AG News по тематическим категориям.

ЗАДАНИЕ:
Загрузите датасет AG News (4 категории: World, Sports, Business, Tech),
проанализируйте распределение новостей по категориям, вычислите статистику
длины текстов и выявите характеристические слова для каждой категории.

ТРЕБОВАНИЯ:
- Загрузить датасет: load_dataset()
- Вычислить распределение по 4 категориям
- Провести анализ длины текстов по категориям
- Найти топ-15 слов для каждой категории
- Создать круговую диаграмму (pie chart)
- Сохранить результаты в ag_news_results.json
"""

import json
import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from datasets import load_dataset
import matplotlib.pyplot as plt


CATEGORY_LABELS = {0: "World", 1: "Sports", 2: "Business", 3: "Tech"}


# TODO: Ваш код здесь


def load_ag_news_dataset():

    # TODO: Реализовать загрузку датасета
    pass


def preprocess_text(tex):

    # TODO: Реализовать предобработку
    pass


def analyze_category_distribution(dataset):

    # TODO: Реализовать анализ
    pass


def analyze_text_lengths_by_category(dataset):

    # TODO: Реализовать анализ длин по категориям
    pass


def extract_top_words_by_category(dataset, top_n) :

    # TODO: Реализовать извлечение слов по категориям
    pass


def create_pie_chart(dataset):

    # TODO: Создать pie chart
    # Сохранить в "visualization.png"
    pass


def main():
    # TODO: Собрать анализ в функцию main()
    pass


if __name__ == "__main__":
    main()
