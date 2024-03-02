import os
import sys

# Для корректной отработки структуры в случае запуска из командной строки
# командой, напр.: "python main.py -n 'Яна Янина' -f 'data/subjects.csv'",
# добавим путь к папке '\utils' в коллекцию 'sys.path'.
sys.path.append(rf'{os.path.abspath('utils/')}')

from student import Student
from test_student import pytest
from utils.parser import Parser

if __name__ == '__main__':
    # Выбор входящих данных для формирования студента
    if Parser.cl_parser().split(',')[0] != 'По Умолчанию':
        # Данные из командной строки
        student = Student(*Parser.cl_parser().split(','))
    else:
        student = Student('Иван Иванов', 'data/subjects.csv')

    # Пример команд, не вызывающих исключений
    student.add_grade('python', 4)
    student.add_test_score('python', 85)
    student.add_grade('django', 5)
    student.add_test_score('django', 92)
    average_grade = student.get_average_grade()
    subj1 = 'python'
    average_test_score = student.get_average_test_score(subj1)
    student2 = Student('Сидоров Сидор', 'data/subjects2.csv')
    student2.add_grade('mongodb', 4)

    # Пример команд, вызывающих исключения
    # average_subject_score = student.get_average_test_score('jinja2')
    # student1 = Student('Сидоров Сидор', 'subjects.cs')
    # average_score = student.get_average_test_score('fastapi')

    # Прохождение тестов также логируется в log/student_log.txt
    pytest.main(['-v'])
