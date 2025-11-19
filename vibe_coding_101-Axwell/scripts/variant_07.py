"""
Анализ датасета Multi-NLI (Natural Language Inference).

ЗАДАНИЕ:
Загрузите датасет Multi-NLI, анализируйте распределение классов (entailment,
contradiction, neutral), выполните анализ длин текстов и выявите
характеристические слова для каждого класса.

ТРЕБОВАНИЯ:
- Загрузить датасет: load_dataset()
- Провести анализ распределения по 3 классам
- Вычислить статистику длин premise и hypothesis
- Найти характеристические слова для каждого класса
- Создать bar chart распределения
- Сохранить результаты в multinli_results.json
"""

import json
import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from datasets import load_dataset
import matplotlib.pyplot as plt


CLASS_LABELS = {0: "entailment", 1: "neutral", 2: "contradiction"}


# TODO: Ваш код здесь


def load_multinli_dataset():
    # TODO: Реализовать загрузку
    pass


def preprocess_text(text: str):
    # TODO: Реализовать
    pass


def analyze_class_distribution(dataset):
    # TODO: Вернуть распределение 3 классов
    pass


def analyze_text_lengths(dataset):
    # TODO: Вернуть статистику premise и hypothesis
    pass


def extract_characteristic_words(dataset, top_n: int = 15):
    # TODO: Вернуть слова для каждого класса
    pass


def create_visualization(dataset):
    # TODO: Создать bar chart и сохранить в "multinli_distribution.png"
    pass


def main():
    # TODO: Собрать анализ
    pass


if __name__ == "__main__":
    main()
