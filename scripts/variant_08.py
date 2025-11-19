"""
Анализ датасета Iris для машинного обучения.

ЗАДАНИЕ:
Загрузите датасет Iris, вычислите статистику по видам растений,
постройте корреляционную матрицу и создайте scatter plots для визуализации.

ТРЕБОВАНИЯ:
- Загрузить датасет Iris из scikit-learn
- Провести анализ статистики по 3 видам (setosa, versicolor, virginica)
- Вычислить корреляционную матрицу признаков
- Найти различия между видами
- Создать scatter plots (sepal vs sepal, petal vs petal)
- Сохранить результаты в iris_results.json
"""

import json
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt


IRIS_NAMES = ["setosa", "versicolor", "virginica"]


# TODO: Ваш код здесь


def load_iris_dataset() :
    # TODO: Реализовать загрузку
    pass


def analyze_species_statistics(df):
    # TODO: Вернуть mean, std, min, max для каждого признака и вида
    pass


def calculate_correlation_matrix(df):
    # TODO: Вернуть correlation matrix и highest correlation pair
    pass


def analyze_feature_differences(df):
    # TODO: Вернуть различия для каждого признака
    pass


def create_visualization(df):
    # TODO: Создать scatter plots и сохранить в "iris_scatter_plots.png"
    pass


def main():
    # TODO: Собрать анализ
    pass


if __name__ == "__main__":
    main()
