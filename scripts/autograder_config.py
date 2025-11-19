"""
Конфигурация автопроверки для заданий по вайбкодингу.

Определяет требования и критерии для каждого варианта задания.
"""

VARIANT_CONFIGS = {
    1: {
        "name": "IMDb Movie Reviews Sentiment Analysis",
        "dataset": "imdb",
        "split": "train[:1000]",
        "expected_files": [
            "assignment.py",
            "test.py",
            "imdb_results.json",
            "imdb_top_words.csv",
            "imdb_analysis.png"
        ],
        "code_requirements": {
            "min_lines": 50,
            "max_lines": 100,
            "required_functions": [
                "load_imdb_dataset",
                "analyze_sentiment_distribution",
                "analyze_text_lengths",
                "extract_top_words",
                "create_visualization"
            ]
        },
        "json_schema": {
            "sentiment_distribution": ["positive", "negative", "positive_percent", "negative_percent"],
            "text_statistics": ["mean_length", "median_length", "min_length", "max_length"],
            "top_words": "dict"
        }
    },
    2: {
        "name": "AG News Topic Classification",
        "dataset": "ag_news",
        "split": "train[:2000]",
        "expected_files": [
            "assignment.py",
            "test.py",
            "ag_news_results.json",
            "visualization.png"
        ],
        "code_requirements": {
            "min_lines": 50,
            "max_lines": 100,
            "required_functions": [
                "load_ag_news_dataset",
                "analyze_category_distribution",
                "extract_top_words_by_category",
                "create_pie_chart"
            ]
        }
    },
    3: {
        "name": "Wikipedia Word Frequency Analysis",
        "dataset": "wikipedia",
        "split": "train[:500]",
        "expected_files": [
            "assignment.py",
            "test.py",
            "wikipedia_results.json",
            "wikipedia_wordcloud.png"
        ]
    },
    4: {
        "name": "MNIST Digit Recognition Analysis",
        "dataset": "ylecun/mnist",
        "split": "train[:5000]",
        "expected_files": [
            "assignment.py",
            "test.py",
            "mnist_results.json",
            "mnist_examples.png"
        ]
    },
    5: {
        "name": "SQuAD Question Answering Dataset",
        "dataset": "rajpurkar/squad",
        "split": "train[:2000]",
        "expected_files": [
            "assignment.py",
            "test.py",
            "squad_results.json",
            "squad_distribution.png"
        ]
    },
    6: {
        "name": "BoolQ Yes/No Questions",
        "dataset": "google/boolq",
        "split": "train[:2000]",
        "expected_files": [
            "assignment.py",
            "test.py",
            "boolq_results.json",
            "boolq_distribution.png"
        ]
    },
    7: {
        "name": "Multi-NLI Textual Entailment",
        "dataset": "nyu-mll/multi_nli",
        "split": "train[:2000]",
        "expected_files": [
            "assignment.py",
            "test.py",
            "multinli_results.json",
            "multinli_distribution.png"
        ]
    },
    8: {
        "name": "Iris Flower Classification",
        "dataset": "iris",
        "source": "sklearn",
        "expected_files": [
            "assignment.py",
            "test.py",
            "iris_results.json",
            "iris_scatter_plots.png"
        ]
    },
    9: {
        "name": "GLUE MRPC Semantic Similarity",
        "dataset": "nyu-mll/glue",
        "config": "mrpc",
        "split": "train[:2000]",
        "expected_files": [
            "assignment.py",
            "test.py",
            "mrpc_results.json",
            "mrpc_distribution.png"
        ]
    },
    10: {
        "name": "DBpedia Category Classification",
        "dataset": "dbpedia_14",
        "split": "train[:3000]",
        "expected_files": [
            "assignment.py",
            "test.py",
            "dbpedia_results.json",
            "dbpedia_distribution.png"
        ]
    }
}


# Критерии оценки
GRADING_CRITERIA = {
    "code_quality": {
        "weight": 20,
        "checks": [
            "pep8_compliance",
            "function_naming",
            "type_hints",
            "line_length",
            "no_code_duplication"
        ]
    },
    "dataset_validation": {
        "weight": 15,
        "checks": [
            "correct_dataset_loaded",
            "expected_fields_present",
            "data_integrity",
            "error_handling",
            "logging"
        ]
    },
    "documentation": {
        "weight": 15,
        "checks": [
            "module_docstring",
            "function_docstrings",
            "inline_comments",
            "readme",
            "doctest_examples"
        ]
    },
    "unit_tests": {
        "weight": 15,
        "checks": [
            "test_file_exists",
            "min_5_functions_tested",
            "all_tests_pass",
            "coverage_above_50",
            "edge_cases_covered"
        ]
    },
    "functionality": {
        "weight": 35,
        "checks": [
            "correct_output_format",
            "calculations_are_correct",
            "no_placeholder_solutions",
            "visualization_informative",
            "statistics_meaningful"
        ]
    }
}


# Требования к документации
DOCUMENTATION_REQUIREMENTS = {
    "README.md": {
        "sections": [
            "Описание задачи",
            "Информация о датасете",
            "Требования",
            "Установка",
            "Использование",
            "Выходные файлы",
            "Пример вывода"
        ],
        "min_length": 500,  # Минимум 500 символов
        "required_sections_percent": 0.7,  # Минимум 70% секций должны быть
    }
}


# Требования к выводам
OUTPUT_REQUIREMENTS = {
    "json_format": {
        "indent": 2,
        "must_include": ["dataset", "statistics", "results"]
    },
    "csv_format": {
        "header": True,
        "encoding": "utf-8"
    },
    "png_format": {
        "dpi": 100,
        "bbox_inches": "tight"
    }
}
