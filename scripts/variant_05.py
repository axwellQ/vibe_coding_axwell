"""
Анализ датасета SQuAD (Stanford Question Answering Dataset).

ЗАДАНИЕ:
Загрузите датасет SQuAD, проанализируйте статистику вопросов и ответов,
вычислите характеристики длин текстов и выполните типологизацию вопросов.

ТРЕБОВАНИЯ:
- Загрузить датасет: load_dataset()
- Провести анализ QA статистики (avg/median lengths)
- Классифицировать вопросы по типам (What, Who, Where, etc.)
- Провести анализ контекстных текстов
- Создать диаграмму распределения длин
- Сохранить результаты в squad_results.json
"""

import json
import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from datasets import load_dataset
import matplotlib.pyplot as plt


# TODO: Ваш код здесь


def load_squad_dataset():
    # TODO: Реализовать загрузку
    pass


def analyze_qa_statistics(dataset):
    # TODO: Вернуть avg/median lengths для вопросов и ответов
    pass


def classify_questions(dataset):
    # TODO: Вернуть распределение: What, Who, When, etc.
    pass


def analyze_context_lengths(dataset):
    # TODO: Вернуть статистику контекстов
    pass


def create_distribution_chart(dataset):
    # TODO: Создать гистограммы и сохранить в "squad_distribution.png"
    pass


def main():
    # TODO: Собрать анализ
    pass


if __name__ == "__main__":
    main()
