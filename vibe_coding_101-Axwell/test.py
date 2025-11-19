import unittest
from assignment import analyze_category_distribution, analyze_text_lengths_by_category, extract_top_words_by_category, preprocess_text, CATEGORY_LABELS

# Тестовый датасет с разными характеристиками
# Используем константу CATEGORY_LABELS для проверки соответствия
TEST_DATASET = [
    {"label": 0, "text": "Global peace talks continue in Geneva."}, # World
    {"label": 1, "text": "The home team won a thrilling match in front of a packed stadium."}, # Sports
    {"label": 2, "text": "Fed official says weak data caused by weather, should not delay tapering."}, # Business
    {"label": 3, "text": "Google Maps Launches New Feature to Help You Find Parking Spots."}, # Tech
    {"label": 0, "text": "Economic recovery shows signs of strengthening, experts say."}, # World
    {"label": 1, "text": "The championship final was decided in a penalty shootout."}, # Sports
    {"label": 2, "text": "New corporate earnings reports exceed market expectations."}, # Business
    {"label": 3, "text": "Scientists develop a new algorithm for faster data processing."}, # Tech
    {"label": 0, "text": "More world news on international relations."}, # World (3 шт.)
    {"label": 1, "text": "Sports news about a tennis tournament."}, # Sports (3 шт.)
    {"label": 2, "text": "Business news about quarterly earnings."}, # Business (3 шт.)
    {"label": 3, "text": "Tech news about artificial intelligence."} # Tech (3 шт.)
]

# Тестовый датасет для граничных случаев
EDGE_CASE_DATASET = [
    {"label": 0, "text": ""}, # Пустой текст
    {"label": 1, "text": "   "}, # Текст только из пробелов
    {"label": 2, "text": "A"}, # Один символ
    {"label": 3, "text": "123 456 !@#"}, # Только числа и символы
    {"label": 0, "text": "Normal text with numbers 123 and symbols !@#."}, # Смешанный
    # Датасет с отсутствующими ключами (для проверки гибкости, хотя в assignment.py это обрабатывается)
    # {"text": "No label here."}, # Не включаем, т.к. assignment.py ожидает 'label'
]

class TestAnalysis(unittest.TestCase):

    # --- Тесты для preprocess_text ---
    def test_preprocess_text_basic(self):
        """Тест: базовая предобработка текста."""
        input_text = "Hello, World! This is a TEST 123."
        expected_output = "hello world this is a test"
        processed = preprocess_text(input_text)
        self.assertEqual(processed, expected_output)

    def test_preprocess_text_edge_cases(self):
        """Тест: предобработка текста - граничные случаи."""
        # Пустой текст
        self.assertEqual(preprocess_text(""), "")
        # Только пробелы
        self.assertEqual(preprocess_text("   "), "")
        # Только числа и символы
        self.assertEqual(preprocess_text("123!@#"), "")
        # Смешанный
        self.assertEqual(preprocess_text("A 1 B!"), "a b")


    # --- Тесты для analyze_category_distribution ---
    def test_analyze_category_distribution_basic(self):
        """Тест: распределение по категориям."""
        result = analyze_category_distribution(TEST_DATASET)
        # Проверим, что все категории присутствуют
        expected_categories = set(CATEGORY_LABELS.values())
        self.assertEqual(set(result.keys()), expected_categories)
        # Проверим количество для каждой категории
        expected = {CATEGORY_LABELS[0]: 3, CATEGORY_LABELS[1]: 3, CATEGORY_LABELS[2]: 3, CATEGORY_LABELS[3]: 3}
        self.assertEqual(result, expected)

    def test_analyze_category_distribution_empty(self):
        """Тест: распределение по категориям для пустого датасета."""
        result = analyze_category_distribution([])
        # Ожидаем, что все категории будут, но с 0
        expected = {name: 0 for name in CATEGORY_LABELS.values()}
        self.assertEqual(result, expected)


    # --- Тесты для analyze_text_lengths_by_category ---
    def test_analyze_text_lengths_by_category_basic(self):
        """Тест: статистика длины текстов по категориям."""
        result = analyze_text_lengths_by_category(TEST_DATASET)
        # Проверим, что все ожидаемые категории присутствуют
        expected_categories = set(CATEGORY_LABELS.values())
        self.assertEqual(set(result.keys()), expected_categories)

        # Проверим структуру возвращаемых данных для одной категории
        for stats in result.values():
            self.assertIn("mean_length", stats)
            self.assertIn("median_length", stats)
            self.assertIn("std_length", stats)
            self.assertIn("min_length", stats)
            self.assertIn("max_length", stats)
            self.assertIsInstance(stats["mean_length"], float)
            self.assertIsInstance(stats["median_length"], float)
            self.assertIsInstance(stats["std_length"], float)
            self.assertIsInstance(stats["min_length"], int)
            self.assertIsInstance(stats["max_length"], int)

        # Пример проверки конкретных значений для одной категории (World)
        # Тексты: "Global peace talks continue in Geneva." (6), "Economic recovery shows signs of strengthening, experts say." (8), "More world news on international relations." (6)
        # Длины: [6, 8, 6] -> mean=6.67, median=6.0, std=0.94 (std генеральной совокупности), min=6, max=8
        world_stats = result.get(CATEGORY_LABELS[0])
        self.assertIsNotNone(world_stats)
        self.assertAlmostEqual(world_stats["mean_length"], 6.67, places=1)
        self.assertEqual(world_stats["median_length"], 6.0)
        # Исправлено: было 1.05, теперь 0.94 (std для [6, 8, 6] как генеральная совокупность)
        self.assertAlmostEqual(world_stats["std_length"], 0.94, places=1)
        self.assertEqual(world_stats["min_length"], 6)
        self.assertEqual(world_stats["max_length"], 8)

    def test_analyze_text_lengths_by_category_empty_category(self):
        """Тест: статистика длины текстов для категории без данных."""
        # Создаём датасет только с одной категорией
        single_cat_dataset = [{"label": 0, "text": "A B C"}]
        result = analyze_text_lengths_by_category(single_cat_dataset)
        # Теперь все категории гарантированно присутствуют
        for cat_name in CATEGORY_LABELS.values():
            stats = result[cat_name]
            if cat_name == CATEGORY_LABELS[0]: # World
                self.assertEqual(stats["mean_length"], 3.0)
                self.assertEqual(stats["median_length"], 3.0)
                self.assertEqual(stats["std_length"], 0.0)
                self.assertEqual(stats["min_length"], 3)
                self.assertEqual(stats["max_length"], 3)
            else: # Остальные категории (Sports, Business, Tech)
                # Проверяем, что возвращаются нулевые значения для пустых категорий
                self.assertEqual(stats["mean_length"], 0)
                self.assertEqual(stats["median_length"], 0)
                self.assertEqual(stats["std_length"], 0)
                self.assertEqual(stats["min_length"], 0)
                self.assertEqual(stats["max_length"], 0)


    # --- Тесты для extract_top_words_by_category ---
    def test_extract_top_words_by_category_basic(self):
        """Тест: извлечение топ слов по категориям."""
        result = extract_top_words_by_category(TEST_DATASET, top_n=2)
        # Проверим, что все ожидаемые категории присутствуют
        expected_categories = set(CATEGORY_LABELS.values())
        self.assertEqual(set(result.keys()), expected_categories)

        # Проверим структуру возвращаемых данных для одной категории
        for category_words in result.values():
            self.assertIsInstance(category_words, list)
            self.assertTrue(all(isinstance(item, tuple) and len(item) == 2 for item in category_words))
            # Проверим, что кортежи содержат строку и число
            for word, count in category_words:
                self.assertIsInstance(word, str)
                self.assertIsInstance(count, int)
                self.assertGreaterEqual(count, 0)

        # Пример проверки для категории "World" (label 0)
        # Тексты: "Global peace talks continue in Geneva.", "Economic recovery shows signs of strengthening, experts say.", "More world news on international relations."
        # Предобработанные и разделённые: ['global', 'peace', 'talks', 'continue', 'in', 'geneva'], ['economic', 'recovery', 'shows', 'signs', 'of', 'strengthening', 'experts', 'say'], ['more', 'world', 'news', 'on', 'international', 'relations']
        # Подсчёт: Все слова встречаются 1 раз. Counter сохраняет порядок. most_common(2) вернёт первые два слова.
        # Это будут ('global', 1), ('peace', 1)
        world_top = result.get(CATEGORY_LABELS[0], [])
        world_top_words = {word: count for word, count in world_top}
        # Исправлено: ожидаемые топ-2 слова теперь те, которые фактически возвращаются первыми
        expected_top_words = {'global', 'peace'} # Эти слова идут первыми в обработке
        actual_top_words_set = set(list(world_top_words.keys())[:2])
        # Проверим, что ожидаемые топ-2 слова совпадают с фактическими первыми двумя
        self.assertEqual(actual_top_words_set, expected_top_words, f"Ожидаемые топ-2 слова {expected_top_words} не совпадают с фактическими {actual_top_words_set} для World. Полный топ: {world_top}")


    def test_extract_top_words_by_category_empty(self):
        """Тест: извлечение топ слов для пустого датасета."""
        result = extract_top_words_by_category([], top_n=5)
        # Теперь все категории гарантированно присутствуют с пустыми списками
        expected = {cat: [] for cat in CATEGORY_LABELS.values()}
        self.assertEqual(result, expected)

    def test_extract_top_words_by_category_few_words(self):
        """Тест: извлечение топ слов, когда уникальных слов меньше, чем top_n."""
        small_dataset = [
            {"label": 0, "text": "cat dog"},
            {"label": 0, "text": "cat"}
        ]
        result = extract_top_words_by_category(small_dataset, top_n=5)
        world_top = result.get(CATEGORY_LABELS[0], [])
        # Ожидаем ('cat', 2), ('dog', 1) в каком-то порядке
        expected_set = {('cat', 2), ('dog', 1)}
        result_set = set(world_top)
        self.assertEqual(result_set, expected_set)


if __name__ == '__main__':
    unittest.main()
