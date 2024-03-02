import logging
import os


class Logger:

    def __init__(self, file_to_save: str = 'log/log.txt', level=logging.NOTSET):

        # Если ещё не подготовили, создадим необходимые директории
        os.makedirs(file_to_save[:file_to_save.rfind('/')], exist_ok=True)

        self.file_to_save = file_to_save
        self.level = level
        logging.basicConfig(format='{levelname} {asctime} {msg}',
                            filename=self.file_to_save, encoding='UTF-8', level=self.level, style='{')
        self.logger = logging.getLogger(__name__)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try:
                func_return = func(*args, **kwargs)
                self.logger.info(f'"{func.__name__}" {args=} {func_return=}')
            except (AttributeError, ValueError, FileNotFoundError) as e:
                self.logger.error(f'{type(e).__name__}: {e}')
                raise type(e)(f'{e}')
            return func_return

        return wrapper
