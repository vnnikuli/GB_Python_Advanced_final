import argparse
import logging
import os
from collections import namedtuple
from typing import Callable

import pytest


def log_to_file(data: str, file: str = 'task2.log') -> None:
    logging.basicConfig(filename=file, encoding='UTF-8', level=logging.NOTSET)
    logger = logging.getLogger(__name__)
    logger.info(data)


def wrap_query(func) -> Callable:
    def wrapper(*args, **kwargs):
        log_to_file(f'{'-' * 15} NEW QUERY START {'-' * 15}')
        res = func(*args, **kwargs)
        log_to_file(f'{'-' * 18} QUERY END {'-' * 18}')
        return res

    return wrapper


@wrap_query
def get_dir_contents(dir_path: str = None) -> list[namedtuple]:
    res = []
    DirItem = namedtuple('DirItem', 'name ext is_dir parent')
    if not dir_path:
        dir_path = os.getcwd()
    for item in os.listdir(dir_path):
        abs_path_w_item = os.path.join(dir_path + '\\' + item)

        name = item if os.path.isdir(abs_path_w_item) else os.path.splitext(item)[0]
        ext = None if os.path.isdir(abs_path_w_item) else os.path.splitext(item)[1]

        new = DirItem(name=name, ext=ext, is_dir=os.path.isdir(abs_path_w_item), parent=f'{dir_path}')
        log_to_file(str(new))
        res.append(new)

    return res


def cl_parser() -> str:
    parser = argparse.ArgumentParser(description='Передайте путь для получения содержимого')
    parser.add_argument('-p', '--path', default=f'{os.getcwd()}')
    args = parser.parse_args()

    return f'{args.path}'


if __name__ == '__main__':
    path = rf'{cl_parser()}'
    # tuples хранит список объектов 'DirItem' (см. *.log файл)
    tuples = get_dir_contents(path)

    pytest.main(['-v'])
