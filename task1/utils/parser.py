# Модуль для запуска из командной строки

import argparse


class Parser:

    @staticmethod
    def cl_parser() -> str:
        parser = argparse.ArgumentParser(description='Работа с классом Student из командной строки')
        parser.add_argument('-n', '--name', default='По Умолчанию')
        parser.add_argument('-f', '--file', default='data/subjects.csv')
        args = parser.parse_args()

        return f'{args.name},{args.file}'
