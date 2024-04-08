import csv
import os

import pytest

from student import Student


class TestStudent:

    # I. Подготовка к тестированию

    @pytest.fixture
    # Создание временного файла с учебными предметами
    def subjects_file(self, request):
        file = 'data/test_student_subjects.csv'
        # Если ещё не подготовили, создадим необходимые директории
        os.makedirs(file[:file.rfind('/')], exist_ok=True)

        subjects = ['javascript', 'python', 'jinja2', 'django']
        with open(file, 'w', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(subjects)

        def delete_file():
            os.remove(file)

        request.addfinalizer(delete_file)

        return file

    # Проверка создания временного файла с учебными предметами 
    def test_subjects_file_creation(self, subjects_file):
        with open(subjects_file, 'r', newline='', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            data = []
            for line in csv_reader:
                data.extend(line)
        assert data == ['javascript', 'python', 'jinja2', 'django']

    @pytest.fixture
    # Создание корректного имени студента
    def correct_name(self, subjects_file):
        return 'Феофан Федоров'

    @pytest.fixture
    # Создание некорректного имени студента
    def incorrect_name(self, subjects_file):
        return 'янина Янковская'

    @pytest.fixture()
    # Создание студента
    def student(self, correct_name, subjects_file):
        return Student(correct_name, subjects_file)

    # II. Тестирование

    def test_student_init_with_correct_name(self, correct_name, subjects_file, capfd):
        student = Student(correct_name, subjects_file)
        assert student is not None
        assert isinstance(student, Student)

    def test_student_init_with_incorrect_name(self, incorrect_name, subjects_file, capfd):
        with pytest.raises(ValueError):
            Student(incorrect_name, subjects_file)

    def test_add_grade_to_correct_subject(self, student):
        student.add_grade('javascript', 5)
        assert student.get_average_grade() == 5.0

    def test_add_grade_with_incorrect_grade_to_correct_subject(self, student):
        with pytest.raises(ValueError):
            student.add_grade('javascript', 7)

    def test_add_test_score_to_incorrect_subject(self, student):
        with pytest.raises(ValueError):
            student.add_test_score('java', 95)

    def test_add_test_score_with_incorrect_score_to_correct_subject(self, student):
        with pytest.raises(ValueError):
            student.add_test_score('javascript', 101)
