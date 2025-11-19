"""
Unit тесты для варианта 3 - Wikipedia Word Frequency Analysis.
"""

import unittest
from collections import Counter


class TestWikipediaAnalysis(unittest.TestCase):
    """Тесты для анализа Wikipedia датасета."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.stopwords = {"the", "a", "and", "or", "but"}

    def test_stopwords_are_excluded(self):
        """Тест: стоп-слова должны быть исключены."""


    def test_top_words_count(self):
        """Тест: должно быть 30 топ слов."""


    def test_wordcloud_generation(self):
        """Тест: облако слов должно быть создано."""


    def test_word_frequency_is_positive(self):
        """Тест: частота слов должна быть положительной."""


    def test_article_statistics(self):
        """Тест: статистика статей должна быть корректна."""



if __name__ == "__main__":
    unittest.main()
