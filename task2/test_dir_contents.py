import os

import pytest
from collections import namedtuple
from main import get_dir_contents


class TestDirContents:

    @pytest.fixture
    # Создадим заготовку для проверки на соответствие типов
    def dir_item_for_type_check(self):
        DirItem = namedtuple('DirItem', 'name ext is_dir parent')
        return DirItem

    @pytest.fixture
    # Создадим временную тестируемую папку '/test/' с подпапками и файлами
    def dir_item_test_folder(self, request):
        os.makedirs('test/dir1', exist_ok=True)
        os.makedirs('test/dir2', exist_ok=True)
        with (open('test/file1.f1', 'w'), open('test/file2.f2', 'w')):
            pass

        def delete_file():
            os.remove('test/file1.f1')
            os.remove('test/file2.f2')
            os.rmdir(os.path.abspath('test/dir1'))
            os.rmdir(os.path.abspath('test/dir2'))
            os.rmdir(os.path.abspath('test'))

        request.addfinalizer(delete_file)

    @pytest.fixture
    # Зафиксируем кортеж имен временной тестируемой папки '/test/'
    def dir_item_test_folder_item_names(self):
        return 'dir1', 'dir2', 'file1', 'file2'

    @pytest.fixture
    # Зафиксируем кортеж расширений временной тестируемой папки '/test/'
    def dir_item_test_folder_item_extensions(self):
        return None, None, '.f1', '.f2'

    # Проверка на соответствие типов
    def test_dir_contents_instance(self, dir_item_for_type_check):
        tuples = get_dir_contents(os.getcwd())
        for tup in tuples:
            assert isinstance(type(tup), type(dir_item_for_type_check))

    # Проверка на количество содержимого тестовой папки
    def test_number_of_dir_contents(self, dir_item_test_folder):
        path = os.path.abspath('test/')
        tuples = get_dir_contents(path)
        assert len(tuples) == 4

    # Проверка имен содержимого тестовой папки
    def test_names_in_test_folder(self, dir_item_test_folder, dir_item_test_folder_item_names):
        path = os.path.abspath('test/')
        tuples = get_dir_contents(path)
        for i in range(len(tuples)):
            assert tuples[i].name == dir_item_test_folder_item_names[i]

    # Проверка расширений содержимого тестовой папки
    def test_extensions_in_test_folder(self, dir_item_test_folder, dir_item_test_folder_item_extensions):
        path = os.path.abspath('test/')
        tuples = get_dir_contents(path)
        for i in range(len(tuples)):
            assert tuples[i].ext == dir_item_test_folder_item_extensions[i]
