import pytest
from unittest.mock import patch, mock_open
import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.append(os.path.dirname(__file__))

# Теперь импортируем твои функции
from main import calculate_average_rating, report_generators


class TestCalculateAverageRating:
    """Тесты для функции calculate_average_rating"""

    def test_basic_functionality(self):
        """Простой тест что функция выполняется без ошибок"""
        # Mock данные CSV
        csv_data = """name,brand,price,rating
iphone,apple,999,4.9
galaxy,samsung,1199,4.8"""

        # Заменяем open() на mock и tabulate() на mock
        with patch('builtins.open', mock_open(read_data=csv_data)):
            with patch('main.tabulate') as mock_tabulate:
                # Вызываем тестируемую функцию
                calculate_average_rating(['test.csv'])

                # Проверяем что tabulate был вызван (значит функция работает)
                assert mock_tabulate.called

    def test_calculation_correctness(self):
        """Тест что средние значения считаются правильно"""
        csv_data = """name,brand,price,rating
product1,apple,999,5.0
product2,apple,899,3.0
product3,samsung,799,4.0"""

        with patch('builtins.open', mock_open(read_data=csv_data)):
            with patch('main.tabulate') as mock_tabulate:
                calculate_average_rating(['test.csv'])

                # Получаем данные которые передали в tabulate
                call_args = mock_tabulate.call_args[0]  # аргументы функции
                table_data = call_args[0]  # первый аргумент - данные таблицы

                # Ищем рейтинг Apple в результатах
                apple_found = False
                for row in table_data:
                    if row[0] == 'apple':
                        apple_rating = float(row[1])
                        apple_found = True
                        break

                # Проверяем что Apple есть и рейтинг правильный
                assert apple_found
                assert apple_rating == 4.0  # (5.0 + 3.0) / 2 = 4.0

    def test_multiple_files(self):
        """Тест обработки нескольких файлов"""
        # Данные для первого файла
        csv_data1 = """name,brand,price,rating
iphone,apple,999,4.9"""

        # Данные для второго файла
        csv_data2 = """name,brand,price,rating
galaxy,samsung,1199,4.8"""

        # Словарь с содержимым файлов
        file_contents = {
            'file1.csv': csv_data1,
            'file2.csv': csv_data2
        }

        # Функция которая возвращает правильные данные для каждого файла
        def mock_file_open(filename, *args, **kwargs):
            return mock_open(read_data=file_contents[filename])(filename, *args, **kwargs)

        with patch('builtins.open', mock_file_open):
            with patch('main.tabulate') as mock_tabulate:
                calculate_average_rating(['file1.csv', 'file2.csv'])

                # Проверяем что tabulate вызван
                assert mock_tabulate.called


class TestReportGenerators:
    """Тесты системы отчетов"""

    def test_report_generators_exists(self):
        """Тест что словарь генераторов существует и содержит нужный отчет"""
        assert 'average-rating' in report_generators
        assert report_generators['average-rating'] == calculate_average_rating


# Простой тест без классов
def test_report_generators_structure():
    """Тест структуры системы отчетов"""
    assert isinstance(report_generators, dict)
    assert len(report_generators) >= 1