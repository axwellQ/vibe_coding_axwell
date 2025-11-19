"""
Анализ датасета BoolQ (Boolean Questions).

ЗАДАНИЕ:
Загрузите датасет BoolQ, проанализируйте распределение да/нет ответов,
статистику длин текстов и выявите характеристические слова для каждого класса.

ТРЕБОВАНИЯ:
- Загрузить датасет: load_dataset()
- Провести анализ распределения true/false ответов
- Вычислить статистику длин вопросов и контекстов
- Найти характеристические слова для каждого класса
- Создать диаграмму распределения
- Сохранить результаты в boolq_results.json
"""

import json
import re
from collections import Counter
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from datasets import load_dataset
import matplotlib.pyplot as plt


# TODO: Ваш код здесь


def load_boolq_dataset():
    # TODO: Реализовать загрузку
    pass


def preprocess_text(text: str):
    # TODO: Реализовать
    pass


def analyze_answer_distribution(dataset):
    # TODO: Вернуть counts и percentages
    pass


def analyze_text_lengths(dataset):
    # TODO: Вернуть статистику вопросов и контекстов
    pass


def extract_characteristic_words(dataset, top_n: int = 15):
    # TODO: Вернуть слова отдельно для true и false
    pass


def create_visualization(dataset):
    # TODO: Создать bar chart и сохранить в "boolq_distribution.png"
    pass


def main():
    # TODO: Собрать анализ
    pass


if __name__ == "__main__":
    main()
