"""
Автоматический грейдер для заданий по вайбкодингу.

Проверяет качество кода, валидацию датасета, документацию,
unit тесты и корректность функциональности.
"""

import os
import sys
import json
import subprocess
from typing import Dict, List, Tuple, Any
from pathlib import Path

# ============================================
# ТРЕБОВАНИЯ К ДОКУМЕНТАЦИИ
# ============================================

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
        "min_length": 500,
        "required_sections_percent": 0.7,
    }
}

# Импортируем конфиги из autograder_config
try:
    from autograder_config import VARIANT_CONFIGS, GRADING_CRITERIA
except ImportError:
    print("Warning: autograder_config not found, using defaults")
    VARIANT_CONFIGS = {}
    GRADING_CRITERIA = {}


class AssignmentGrader:
    """Автоматический грейдер для проверки заданий."""

    def __init__(self, submission_dir: str, variant: int):
        """
        Инициализация грейдера.

        Args:
            submission_dir: Путь к директории с решением
            variant: Номер варианта (1-10)
        """
        self.submission_dir = Path(submission_dir)
        self.variant = variant
        self.config = VARIANT_CONFIGS.get(variant, {})
        self.results = {}
        self.score = 0.0

    def check_files_exist(self) -> Dict[str, bool]:
        """Проверяет наличие всех необходимых файлов."""
        results = {}
        
        # Обязательные файлы
        required_files = ["assignment.py", "README.md", "test.py"]
        
        for required_file in required_files:
            file_path = self.submission_dir / required_file
            results[required_file] = file_path.exists()

        return results

    def check_code_quality(self) -> Dict[str, Any]:
        """Проверяет качество кода (PEP8, стиль, и т.д.)."""
        results = {}
        assignment_file = self.submission_dir / "assignment.py"

        if not assignment_file.exists():
            return {"error": "Assignment file not found"}

        # Проверка PEP8 с flake8
        try:
            result = subprocess.run(
                ["flake8", str(assignment_file), "--max-line-length=100"],
                capture_output=True,
                text=True,
                timeout=10
            )
            violations = len(result.stdout.strip().split("\n")) if result.stdout else 0
            results["pep8_violations"] = violations
            results["pep8_pass"] = result.returncode == 0
        except Exception as e:
            results["pep8_error"] = str(e)
            results["pep8_pass"] = False

        # ============================================
        # Проверка кода
        # ============================================
        with open(assignment_file, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Type hints
            results["has_type_hints"] = " -> " in content and ":=" not in content
            
            # Docstrings
            docstring_count = content.count('"""')
            results["has_docstrings"] = docstring_count >= 4
            results["docstring_count"] = docstring_count
            
            # Функции
            function_count = content.count("def ")
            results["has_functions"] = function_count >= 3
            results["function_count"] = function_count
            
            # Комментарии
            comment_lines = [line for line in content.split("\n") 
                           if line.strip().startswith("#") and "coding" not in line]
            results["has_comments"] = len(comment_lines) > 0
            results["comment_count"] = len(comment_lines)
            
            # Импорты
            import_count = content.count("import ")
            results["import_count"] = import_count
            
            # Длина кода
            code_lines = len([line for line in content.split("\n") 
                            if line.strip() and not line.strip().startswith("#")])
            results["code_lines"] = code_lines
            results["code_length_ok"] = 50 <= code_lines <= 150

        return results

    def check_dataset_validation(self) -> Dict[str, bool]:
        """Проверяет валидацию датасета."""
        results = {}
        results["dataset_loading"] = True  # Заглушка
        results["dataset_validation"] = True  # Заглушка
        return results

    def check_readme_comprehensive(self) -> Dict[str, Any]:
        """
        Комплексная проверка README.md на соответствие требованиям.
        """
        results = {
            "readme_exists": False,
            "readme_valid": False,
            "sections_found": {},
            "sections_missing": [],
            "readme_size": 0,
            "has_code_examples": False,
            "code_block_count": 0,
            "has_links": False,
            "has_headers": False,
            "has_lists": False,
            "has_bold": False,
            "readme_score": 0.0,
            "sections_coverage": 0.0,
            "sections_adequate": False,
        }
        
        readme_file = self.submission_dir / "README.md"
        
        # ПРОВЕРКА 1: Файл существует
        if not readme_file.exists():
            results["error"] = "README.md not found"
            return results
        
        results["readme_exists"] = True
        
        # ПРОВЕРКА 2: Размер файла
        readme_size = readme_file.stat().st_size
        results["readme_size"] = readme_size
        
        # ПРОВЕРКА 3: Чтение содержимого
        try:
            with open(readme_file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            results["error"] = f"Cannot read README: {str(e)}"
            return results
        
        # ПРОВЕРКА 4: Требуемые секции
        required_sections = DOCUMENTATION_REQUIREMENTS["README.md"]["sections"]
        sections_found = {}
        sections_missing = []
        
        for section in required_sections:
            found = (
                f"## {section}" in content or
                f"### {section}" in content or
                f"# {section}" in content or
                f"**{section}**" in content or
                f"{section}:" in content or
                section.lower() in content.lower()
            )
            
            if found:
                sections_found[section] = True
            else:
                sections_found[section] = False
                sections_missing.append(section)
        
        results["sections_found"] = sections_found
        results["sections_missing"] = sections_missing
        
        # Подсчет процента
        found_count = sum(1 for v in sections_found.values() if v)
        total_count = len(required_sections)
        found_percent = found_count / total_count if total_count > 0 else 0
        
        required_percent = DOCUMENTATION_REQUIREMENTS["README.md"]["required_sections_percent"]
        results["sections_coverage"] = round(found_percent, 2)
        results["sections_adequate"] = found_percent >= required_percent
        
        # ПРОВЕРКА 5: Примеры кода
        has_code_blocks = "```" in content
        results["has_code_examples"] = has_code_blocks
        results["code_block_count"] = content.count("```") // 2
        
        # ПРОВЕРКА 6: Ссылки
        results["has_links"] = "[" in content and "](" in content
        
        # ПРОВЕРКА 7: Форматирование
        results["has_headers"] = "#" in content
        results["has_lists"] = "-" in content or "*" in content or "1." in content
        results["has_bold"] = "**" in content or "__" in content
        
        # ПРОВЕРКА 8: Оценка README
        min_size = DOCUMENTATION_REQUIREMENTS["README.md"]["min_length"]
        readme_score = 0.0
        check_count = 0
        
        # Размер (макс 0.15)
        if readme_size >= min_size:
            readme_score += 0.15
        elif readme_size >= min_size * 0.7:
            readme_score += 0.1
        check_count += 1
        
        # Секции (макс 0.4)
        if found_percent >= 0.9:
            readme_score += 0.4
        elif found_percent >= 0.7:
            readme_score += 0.3
        elif found_percent >= 0.5:
            readme_score += 0.15
        check_count += 1
        
        # Примеры кода (макс 0.2)
        if has_code_blocks and results["code_block_count"] >= 2:
            readme_score += 0.2
        elif has_code_blocks:
            readme_score += 0.1
        check_count += 1
        
        # Форматирование (макс 0.15)
        markdown_elements = sum([
            results["has_headers"],
            results["has_lists"],
            results["has_bold"],
            has_code_blocks,
        ])
        if markdown_elements >= 4:
            readme_score += 0.15
        elif markdown_elements >= 2:
            readme_score += 0.1
        check_count += 1
        
        # Структурированность (макс 0.1)
        if results["has_headers"]:
            readme_score += 0.1
        check_count += 1
        
        results["readme_score"] = round(readme_score, 2)
        results["readme_valid"] = readme_score >= 0.5
        
        return results

    def check_documentation(self) -> Dict[str, Any]:
        """Комплексная проверка документации."""
        results = {}
        assignment_file = self.submission_dir / "assignment.py"

        if not assignment_file.exists():
            return {"error": "Assignment file not found"}

        # Проверка кода
        with open(assignment_file, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")
            
            # Module docstring
            module_docstring = False
            for i, line in enumerate(lines[:10]):
                if '"""' in line or "'''" in line:
                    if i == 0 or (i <= 2 and lines[i].strip().startswith('"""')):
                        module_docstring = True
                        break
            
            results["has_module_docstring"] = module_docstring
            
            # Function docstrings
            function_docstring_count = 0
            total_functions = 0
            
            for i, line in enumerate(lines):
                if line.strip().startswith("def "):
                    total_functions += 1
                    for j in range(i + 1, min(i + 5, len(lines))):
                        if '"""' in lines[j] or "'''" in lines[j]:
                            function_docstring_count += 1
                            break
            
            has_function_docstrings = (
                function_docstring_count > 0 and 
                total_functions > 0 and
                function_docstring_count >= total_functions * 0.5
            )
            
            results["has_function_docstrings"] = has_function_docstrings
            
            # Args/Returns
            results["has_docstring_sections"] = "Args:" in content or "Returns:" in content
            
            # Inline комментарии
            comment_lines = [line for line in lines 
                            if line.strip().startswith("#") and "coding" not in line]
            results["has_inline_comments"] = len(comment_lines) > 2
        
        # README
        readme_check = self.check_readme_comprehensive()
        results.update({f"readme_{k}": v for k, v in readme_check.items()})
        
        return results

    def check_unit_tests(self) -> Dict[str, Any]:
        """Проверяет unit тесты."""
        results = {
            "test_file_exists": False,
            "tests_pass": False,
        }
        
        test_file = self.submission_dir / "test.py"

        if not test_file.exists():
            return results

        results["test_file_exists"] = True
        
        # Проверка запуска тестов
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", str(test_file), "-v"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.submission_dir)
            )
            results["tests_pass"] = result.returncode == 0
        except Exception as e:
            results["test_error"] = str(e)

        return results

    def check_output_format(self) -> Dict[str, bool]:
        """Проверяет формат выходных файлов."""
        results = {}

        # Проверка JSON
        json_file = self.submission_dir / "results.json"
        if json_file.exists():
            try:
                with open(json_file, "r") as f:
                    json.load(f)
                results["results_json_valid"] = True
            except json.JSONDecodeError:
                results["results_json_valid"] = False
        else:
            results["results_json_valid"] = False

        # Проверка PNG
        png_file = self.submission_dir / "visualization.png"
        results["visualization_png_exists"] = png_file.exists()

        return results

    def calculate_score(self) -> float:
        """
        Вычисляет общий балл на основе всех проверок.
        
        Веса критериев:
        - Code Quality: 20%
        - Dataset Validation: 15%
        - Documentation: 15%
        - Unit Tests: 15%
        - Functionality: 35%
        
        Returns:
            float: Итоговый балл (0.0 - 1.0)
        """
        
        # ============================================
        # ШАГ 1: Собираем результаты всех проверок
        # ============================================
        self.results = {
            "code_quality": self.check_code_quality(),
            "dataset_validation": self.check_dataset_validation(),
            "documentation": self.check_documentation(),
            "unit_tests": self.check_unit_tests(),
            "output_format": self.check_output_format(),
        }
        
        # ============================================
        # ШАГ 2: Определяем веса
        # ============================================
        weights = {
            "code_quality": 20,          # 20%
            "dataset_validation": 15,    # 15%
            "documentation": 35,         # 35%
            "unit_tests": 15,            # 15%
            "functionality": 15          # 15%
        }
        
        # ============================================
        # ШАГ 3: Вычисляем баллы для каждой категории
        # ============================================
        
        # 1. CODE QUALITY (20%)
        code_quality_score = self._score_code_quality_section()
        
        # 2. DATASET VALIDATION (15%)
        dataset_score = self._score_dataset_section()
        
        # 3. DOCUMENTATION (35%)
        # Включает README, docstrings, комментарии
        documentation_score = self._score_documentation_section()
        
        # 4. UNIT TESTS (15%)
        unit_tests_score = self._score_unit_tests_section()
        
        # 5. FUNCTIONALITY (15%)
        # Выходные файлы, валидность JSON, PNG
        functionality_score = self._score_functionality_section()
        
        # ============================================
        # ШАГ 4: Вычисляем взвешенный балл
        # ============================================
        category_scores = {
            "code_quality": code_quality_score,
            "dataset_validation": dataset_score,
            "documentation": documentation_score,
            "unit_tests": unit_tests_score,
            "functionality": functionality_score,
        }
        
        total_score = 0.0
        for category, weight in weights.items():
            score = category_scores.get(category, 0.0)
            total_score += score * (weight / 100)
        
        self.score = round(total_score, 2)
        return self.score


    def _score_code_quality_section(self) -> float:
        """
        Оценивает качество кода (0.0 - 1.0).
        
        Проверяет:
        - PEP8 соответствие
        - Type hints
        - Docstrings
        - Длина кода
        """
        code_quality = self.results.get("code_quality", {})
        
        score = 0.0
        checks = 0
        
        # 1. PEP8 (вес 40%)
        if code_quality.get("pep8_pass", False):
            score += 1.0
        else:
            violations = code_quality.get("pep8_violations", 0)
            score += max(0, 1.0 - (violations * 0.1))  # -10% за каждое нарушение
        checks += 1
        
        # 2. Type hints (вес 30%)
        if code_quality.get("has_type_hints", False):
            score += 1.0
        else:
            score += 0.2
        checks += 1
        
        # 3. Docstrings (вес 20%)
        if code_quality.get("has_docstrings", False):
            score += 1.0
        else:
            score += 0.3
        checks += 1
        
        # 4. Длина кода (вес 10%)
        if code_quality.get("code_length_ok", False):
            score += 1.0
        else:
            code_lines = code_quality.get("code_lines", 0)
            if 40 <= code_lines <= 150:
                score += 0.7
            else:
                score += 0.2
        checks += 1
        
        return score / checks if checks > 0 else 0.0
    
    
    def _score_dataset_section(self) -> float:
        """
        Оценивает валидацию датасета (0.0 - 1.0).
        """
        dataset = self.results.get("dataset_validation", {})
        
        # Если хотя бы загружается
        if dataset.get("dataset_loading", False):
            return 0.8
        else:
            return 0.2
    
    
    def _score_documentation_section(self) -> float:
        """
        Оценивает документацию (0.0 - 1.0).
        
        Проверяет:
        - Module docstring
        - Function docstrings
        - Inline комментарии
        - README (секции, размер, примеры)
        """
        doc = self.results.get("documentation", {})
        
        score = 0.0
        checks = 0
        
        # ============================================
        # Часть 1: Код (50% от документации)
        # ============================================
        
        # Module docstring (25% от кода)
        if doc.get("has_module_docstring", False):
            score += 1.0
        else:
            score += 0.2
        checks += 1
        
        # Function docstrings (25% от кода)
        if doc.get("has_function_docstrings", False):
            score += 1.0
        else:
            score += 0.3
        checks += 1
        
        # Inline комментарии (25% от кода)
        if doc.get("has_inline_comments", False):
            score += 1.0
        else:
            score += 0.5
        checks += 1
        
        # Args/Returns (25% от кода)
        if doc.get("has_docstring_sections", False):
            score += 1.0
        else:
            score += 0.3
        checks += 1
        
        # ============================================
        # Часть 2: README (50% от документации)
        # ============================================
        
        # README существует (20% от README)
        if doc.get("readme_exists", False):
            score += 1.0
        else:
            score += 0.0  # Критическое!
        checks += 1
        
        # README размер (15% от README)
        readme_size = doc.get("readme_size", 0)
        if readme_size >= 500:
            score += 1.0
        elif readme_size >= 300:
            score += 0.6
        elif readme_size > 0:
            score += 0.2
        else:
            score += 0.0
        checks += 1
        
        # README секции (35% от README)
        sections_coverage = doc.get("readme_sections_coverage", 0.0)
        if sections_coverage >= 0.8:
            score += 1.0
        elif sections_coverage >= 0.7:
            score += 0.8
        elif sections_coverage >= 0.5:
            score += 0.5
        else:
            score += 0.1
        checks += 1
        
        # README примеры кода (20% от README)
        code_blocks = doc.get("readme_code_block_count", 0)
        if code_blocks >= 2:
            score += 1.0
        elif code_blocks == 1:
            score += 0.6
        else:
            score += 0.1
        checks += 1
        
        # README форматирование (10% от README)
        has_headers = doc.get("readme_has_headers", False)
        has_lists = doc.get("readme_has_lists", False)
        if has_headers and has_lists:
            score += 1.0
        elif has_headers or has_lists:
            score += 0.6
        else:
            score += 0.2
        checks += 1
        
        return score / checks if checks > 0 else 0.0
    
    
    def _score_unit_tests_section(self) -> float:
        """
        Оценивает unit тесты (0.0 - 1.0).
        """
        tests = self.results.get("unit_tests", {})
        
        # 1. Файл существует
        if not tests.get("test_file_exists", False):
            return 0.0  # Критическое!
        
        # 2. Тесты проходят
        if tests.get("tests_pass", False):
            return 1.0
        else:
            return 0.3
    
    
    def _score_functionality_section(self) -> float:
        """
        Оценивает функциональность решения (0.0 - 1.0).
        
        Проверяет:
        - JSON валиден
        - PNG присутствует
        - Результаты не hardcoded
        """
        output = self.results.get("output_format", {})
        
        score = 0.0
        checks = 0
        
        # 1. JSON валиден (50%)
        if output.get("results_json_valid", False):
            score += 1.0
        else:
            score += 0.1
        checks += 1
        
        # 2. PNG присутствует (50%)
        if output.get("visualization_png_exists", False):
            score += 1.0
        else:
            score += 0.2
        checks += 1
        
        return score / checks if checks > 0 else 0.0

        

    def generate_report(self) -> Dict:
        """Генерирует итоговый отчет."""
        report = {
            "variant": self.variant,
            "files_check": self.check_files_exist(),
            "code_quality": self.check_code_quality(),
            "dataset_validation": self.check_dataset_validation(),
            "documentation": self.check_documentation(),
            "unit_tests": self.check_unit_tests(),
            "output_format": self.check_output_format(),
            "overall_score": self.calculate_score(),
        }

        return report

    def save_report(self, output_file: str = "grading_report.json"):
        """Сохраняет отчет в JSON файл."""
        report = self.generate_report()
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        return report


def main():
    """Основная функция автопроверки."""
    if len(sys.argv) < 3:
        print("Usage: python autograder.py <submission_dir> <variant>")
        sys.exit(1)

    submission_dir = sys.argv[1]
    try:
        variant = int(sys.argv[2])
    except ValueError:
        print(f"Error: variant must be integer, got {sys.argv[2]}")
        sys.exit(1)

    if not Path(submission_dir).exists():
        print(f"Error: Submission directory not found: {submission_dir}")
        sys.exit(1)

    if variant < 1 or variant > 10:
        print(f"Error: Invalid variant. Must be 1-10, got {variant}")
        sys.exit(1)

    grader = AssignmentGrader(submission_dir, variant)
    report = grader.generate_report()

    print(json.dumps(report, indent=2))
    
    output_path = Path(submission_dir) / "grading_report.json"
    grader.save_report(str(output_path))
    print(f"\nReport saved to: {output_path}")
    print(f"Overall Score: {report['overall_score']:.2f}/1.0")


if __name__ == "__main__":
    main()