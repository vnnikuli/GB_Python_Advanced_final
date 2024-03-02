from utils.csv_reader import CSVReader
from utils.logger import Logger
from utils.validator import (Validate, ValidateStudentName, ValidateStudentSubject,
                             ValidateStudentSubjectFile, ValidateGrade, ValidateTestScore)


class LoggerFile:
    file_to_save = 'log/student.log'


class Student:
    name: str = Validate(ValidateStudentName())
    subjects_file: str = Validate(ValidateStudentSubjectFile())
    subject_to_validate: str = Validate(ValidateStudentSubject())
    grade_to_validate: int = Validate(ValidateGrade())
    test_score_to_validate: int = Validate(ValidateTestScore())

    @Logger(file_to_save=LoggerFile.file_to_save)
    def __init__(self, name, subjects_file):
        self.name = name
        self.subjects_file = subjects_file
        ValidateStudentSubject.subjects_file = self.subjects_file
        self.subjects = dict()
        self.load_subjects(subjects_file)

    @Logger(file_to_save=LoggerFile.file_to_save)
    def load_subjects(self, subjects_file):
        [self.subjects.setdefault(k, {}) for k in CSVReader.read_file(subjects_file)]

    def __str__(self):
        subjects = ', '.join([k for k, v in self.subjects.items() if v])
        return f'Студент: {self.name}\nПредметы: {subjects}'

    def __repr__(self):
        subjects = ', '.join([k for k, v in self.subjects.items() if v])
        return f'Student.repr: " {self.name=}:{subjects=} "'

    @Logger(file_to_save=LoggerFile.file_to_save)
    def add_grade(self, subject, grade):
        self.subject_to_validate, self.grade_to_validate = subject, grade
        self.subjects[subject].setdefault('grades', [])
        self.subjects[subject]['grades'].append(grade)

    @Logger(file_to_save=LoggerFile.file_to_save)
    def add_test_score(self, subject, test_score):
        self.subject_to_validate, self.test_score_to_validate = subject, test_score
        self.subjects[subject].setdefault('test_scores', [])
        self.subjects[subject]['test_scores'].append(test_score)

    @Logger(file_to_save=LoggerFile.file_to_save)
    def get_average_grade(self) -> float:
        all_grades = []
        for subject in self.subjects:
            if self.subjects[subject].get('grades'):
                all_grades.extend(self.subjects[subject].get('grades'))
        return sum(all_grades) / len(all_grades) if len(all_grades) > 0 else 0

    @Logger(file_to_save=LoggerFile.file_to_save)
    def get_average_test_score(self, subject):
        self.subject_to_validate = subject
        all_test_scores = []
        if self.subjects[subject].get('test_scores'):
            all_test_scores.extend(self.subjects[subject].get('test_scores'))
        return sum(all_test_scores) / len(all_test_scores) if len(all_test_scores) > 0 else 0
