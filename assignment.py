"""
Классификация новостей AG News по тематическим категориям.

ЗАДАНИЕ:
Загрузите датасет AG News (4 категории: World, Sports, Business, Tech),
проанализируйте распределение новостей по категориям, вычислите статистику
длины текстов и выявите характеристические слова для каждой категории.

ТРЕБОВАНИЯ:
- Загрузить датасет: load_dataset() <- Попытка, с резервным вариантом
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
# from datasets import load_dataset # Импорт закомментирован, так как может не работать
import matplotlib.pyplot as plt

CATEGORY_LABELS = {0: "World", 1: "Sports", 2: "Business", 3: "Tech"}

#  Имя файла для локального датасета
LOCAL_DATASET_FILE = "ag_news_sample.json"

#  Обратный словарь для проверки в тестах
LABEL_TO_CATEGORY = {v: k for k, v in CATEGORY_LABELS.items()}


def load_ag_news_dataset():
    """
    Загружает датасет AG News.
    Сначала пытается загрузить с Hugging Face Hub.
    Если загрузка зависает или вызывает ошибку, использует локальный файл 'ag_news_sample.json'.
    """
    try:
        print("DEBUG: Попытка загрузки датасета из Hugging Face Hub...")
        from datasets import load_dataset
        dataset = load_dataset("ag_news", split="train")
        print("DEBUG: Датасет успешно загружен из Hugging Face Hub.")
        return dataset
    except ImportError:
        print("DEBUG: Библиотека 'datasets' не установлена. Использую локальный файл.")
    except KeyboardInterrupt:
        print("DEBUG: Прервано пользователем (Ctrl+C). Использую локальный файл.")
    except Exception as e:
        print(f"DEBUG: Ошибка при загрузке из Hugging Face Hub: {e}. Использую локальный файл.")
    # Если Hugging Face не сработал, загружаем из локального файла
    try:
        print(f"DEBUG: Загружаю датасет из локального файла '{LOCAL_DATASET_FILE}'...")
        with open(LOCAL_DATASET_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("DEBUG: Локальный датасет успешно загружен.")
        return data
    except FileNotFoundError:
        print(f"ERROR: Файл '{LOCAL_DATASET_FILE}' не найден. Невозможно загрузить датасет.")
        raise FileNotFoundError(f"Файл '{LOCAL_DATASET_FILE}' отсутствует.")
    except json.JSONDecodeError as e:
        print(f"ERROR: Ошибка чтения JSON из '{LOCAL_DATASET_FILE}': {e}")
        raise e


def preprocess_text(text: str) -> str:
    """
    Предобрабатывает текст: приведение к нижнему регистру, удаление знаков препинания и чисел.

    Args:
        text (str): Входной текст.

    Returns:
        str: Предобработанный текст.
    """
    # Приведение к нижнему регистру
    text = text.lower()
    # Удаление чисел и знаков препинания, оставляя только буквы и пробелы
    text = re.sub(r'[^a-z\s]', ' ', text)
    # Удаление лишних пробелов
    text = ' '.join(text.split())
    return text


def analyze_category_distribution(dataset) -> Dict[str, int]:
    """
    Анализирует распределение новостей по категориям.

    Args:
        dataset: Загруженный датасет (список словарей с ключами 'text' и 'label').

    Returns:
        Dict[str, int]: Словарь с количеством новостей по каждой категории.
    """
    distribution = Counter()
    for item in dataset:
        label = item.get('label')
        if label is not None:
            category_name = CATEGORY_LABELS.get(label)
            if category_name:
                distribution[category_name] += 1
    # Гарантируем, что все категории присутствуют в результате
    result = {name: distribution.get(name, 0) for name in CATEGORY_LABELS.values()}
    return result


def analyze_text_lengths_by_category(dataset) -> Dict[str, Dict[str, float]]:
    """
    Вычисляет статистику длины текстов по категориям.

    Args:
        dataset: Загруженный датасет.

    Returns:
        Dict[str, Dict[str, float]]:
        Словарь со статистикой (средняя, медиана, std) по каждой категории.
    """
    lengths_by_category = defaultdict(list)
    for item in dataset:
        text = item.get('text', '')
        label = item.get('label')
        category_name = CATEGORY_LABELS.get(label)
        if category_name:
            lengths_by_category[category_name].append(len(text.split()))

    stats = {}
    # Проходим по всем возможным категориям, чтобы гарантировать их наличие
    for label, category_name in CATEGORY_LABELS.items():
        lengths = lengths_by_category[category_name]
        if lengths:
            arr_lengths = np.array(lengths)
            stats[category_name] = {
                "mean_length": round(np.mean(arr_lengths), 2),
                "median_length": float(np.median(arr_lengths)),
                "std_length": round(np.std(arr_lengths), 2),
                "min_length": int(np.min(arr_lengths)),
                "max_length": int(np.max(arr_lengths))
            }
        else:
            stats[category_name] = {"mean_length": 0, "median_length": 0,
                                    "std_length": 0, "min_length": 0, "max_length": 0}
    return stats


def extract_top_words_by_category(dataset, top_n: int = 15) -> Dict[str, List[Tuple[str, int]]]:
    """
    Извлекает топ-N слов для каждой категории.

    Args:
        dataset: Загруженный датасет.
        top_n (int): Количество топ слов для извлечения. По умолчанию 15.

    Returns:
        Dict[str, List[Tuple[str, int]]]: Словарь, где ключ - категория, значение - список топ слов.
    """
    words_by_category = defaultdict(Counter)
    for item in dataset:
        text = item.get('text', '')
        label = item.get('label')
        category_name = CATEGORY_LABELS.get(label)
        if category_name:
            processed_text = preprocess_text(text)
            words = processed_text.split()
            # Обновляем счётчик слов для текущей категории
            words_by_category[category_name].update(words)

    top_words = {}
    # Проходим по всем возможным категориям, чтобы гарантировать их наличие
    for label, category_name in CATEGORY_LABELS.items():
        counter = words_by_category[category_name]
        # Получаем топ-N слов
        top_words[category_name] = counter.most_common(top_n)
    return top_words


def create_pie_chart(category_counts: Dict[str, int]):
    """
    Создаёт и сохраняет круговую диаграмму распределения категорий.

    Args:
        category_counts (Dict[str, int]): Словарь с количеством новостей по категориям.
    """
    labels = category_counts.keys()
    sizes = category_counts.values()

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of News Categories in AG News Dataset')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(
        "visualization.png"
    )
    plt.close()


def main():
    """
    Основная функция для выполнения анализа.
    """
    print("Loading AG News dataset...")
    dataset = load_ag_news_dataset()
    print("Dataset loaded successfully.")

    print("Analyzing category distribution...")
    category_dist = analyze_category_distribution(dataset)
    print("Category distribution:", category_dist)

    print("Analyzing text lengths...")
    length_stats = analyze_text_lengths_by_category(dataset)
    print("Length statistics by category:", length_stats)

    print("Extracting top words...")
    top_words = extract_top_words_by_category(dataset, top_n=15)
    print("Top words extracted.")

    print("Creating pie chart...")
    create_pie_chart(category_dist)
    print("Pie chart saved as 'visualization.png'.")

    # Сбор результатов в один словарь
    results = {
        "dataset": "ag_news",
        "category_distribution": category_dist,
        "text_length_statistics": length_stats,
        "top_words_per_category": top_words
    }

    print("Saving results to 'ag_news_results.json'...")
    with open("ag_news_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("Results saved successfully.")


if __name__ == "__main__":
    main()
