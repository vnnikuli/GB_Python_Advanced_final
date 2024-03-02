from string import ascii_lowercase

from csv_reader import CSVReader


class Validate:
    """
    Класс-дескриптор, принимает валидатор
    """

    def __init__(self, validator):
        self.validator = validator

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if self.validator.validate(value):
            setattr(instance, self.name, value)


# Ниже список валидаторов


class ValidateStudentName:
    """
    Валидатор имен
    """

    @staticmethod
    def validate(value: str) -> bool:
        cyrillic_lower_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        chars = ascii_lowercase + cyrillic_lower_letters
        if [c for c in value.replace(' ', '').lower() if c not in chars] or not value.istitle():
            raise ValueError('ФИО должно состоять только из букв и начинаться с заглавной буквы')
        return True


class ValidateStudentSubjectFile:
    """
    Валидатор имен файлов
    """

    @staticmethod
    def validate(value: str) -> bool:
        if type(value) is not str or not value.endswith('.csv'):
            raise ValueError('Переданное имя файла должно быть в формате "имя_файла.csv"')
        return True


class ValidateStudentSubject:
    """
    Валидатор учебных предметов
    """

    def __init__(self):
        self._subjects_file = None
        self.subjects_list = None

    @property
    def subjects_file(self):
        return self._subjects_file

    @subjects_file.setter
    def subjects_file(self, value: str):
        self._subjects_file = value

    def validate(self, value: str) -> bool:
        self.subjects_list = CSVReader.read_file(self.subjects_file) if self.subjects_file else ['']
        if value not in self.subjects_list:
            raise ValueError(f'Предмет {value} не найден')
        return True


class ValidateGrade:
    """
    Валидатор оценок
    """

    def __init__(self):
        self.min_grade, self.max_grade = 2, 5

    def validate(self, value: int) -> bool:
        if type(value) is not int or not self.min_grade <= value <= self.max_grade:
            raise ValueError('Оценка должна быть целым числом от 2 до 5')
        return True


class ValidateTestScore:
    """
    Валидатор тестовых баллов
    """

    def __init__(self):
        self.min_test_score, self.max_test_score = 0, 100

    def validate(self, value: int) -> bool:
        if type(value) is not int or not self.min_test_score <= value <= self.max_test_score:
            raise ValueError('Результат теста должен быть целым числом от 0 до 100')
        return True
