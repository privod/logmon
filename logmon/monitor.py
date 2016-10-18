from time import time, sleep
import sys
import os.path
from glob import glob

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from logmon.log import Parser, Level
from logmon.conf import Conf
import logmon.keeping as keep

# path = os.path.join('.', 'testdata')           # TODO Переопределить
# print(os.getcwd())

# class FileParcer(Parser):
#
#     def __init__(self, file_name = None, level_monitor=Level.WARN):
#         super().__init__(level_monitor)
#         self.file_name = file_name
#
#     def pars(self, date_begin=None):
#         with open(self.file_name, 'rb') as file:
#             return super().pars(file.read(), date_begin)


class Handler(PatternMatchingEventHandler):

    def __init__(self,patterns=None, ignore_patterns=None,
                 ignore_directories=False, case_sensitive=False, mon_pool_file_name=None):
        super().__init__(patterns, ignore_patterns, ignore_directories, case_sensitive)
        self._mon_pool_file_name = mon_pool_file_name

    def on_modified(self, event):
        # print(event)
        # print('Новый файл лога: ', event.src_path)
        self._mon_pool_file_name.add(event.src_path)


def files_parse(file_name_pool, data=None, level=Level.WARN):
    while len(file_name_pool) > 0:
        file_name = os.path.normpath(file_name_pool.pop())
        # print('Обработка лога {}:'.format(file_name))
        pos_beg = data.get(file_name, {'pos': 0}).get('pos')

        file_bytes = open(file_name, 'rb').read()
        parse_bytes = file_bytes[pos_beg:]
        if not parse_bytes:
            # print('\tБез изменений')
            continue

        log_list = Parser(level).pars(parse_bytes, bar_title=file_name)

        data.setdefault(file_name, {'pos': 0, 'log_list': []})
        data[file_name]['log_list'].extend(log_list)
        data[file_name]['pos'] = pos_beg + len(file_bytes)


# def _set_argv(argv, default=None):
#     if argv is None:
#         argv = sys.argv[1:]
#     if len(argv) == 0:
#         argv = default
#     return argv


def print_data(data):
    for key, val in data.items():
        print(key)
        for log in val['log_list']:
            print('\t', log)


def logmon_start(conf_arg=None):
    # path, *patterns = _set_argv(argv, ['.', '*.log'])
    conf = Conf(conf_arg)

    file_name_pool = set()
    observer = Observer()
    handler = Handler(patterns=conf.get('patterns'), ignore_directories=True, mon_pool_file_name=file_name_pool)
    observer.schedule(handler, path=conf.get('path'), recursive=True)
    observer.start()

    try:
        # data = {}
        beg_time = time()
        while True:

            sleep(1)

            # Таймер 10 минут
            if time() - beg_time > 600:
                data = keep.load()
                files_parse(file_name_pool, data)
                keep.save(data)

                beg_time = time()

    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    # print_data(keep.load())


def logmon_path(conf_arg=None):
    # path, *patterns = _set_argv(argv, ['.', '*.log'])
    conf = Conf(conf_arg)

    # data = {}

    for pattern in conf.get('patterns'):
        file_name_pool = glob(os.path.join(conf.get('path'), pattern))
        data = keep.load()
        files_parse(file_name_pool, data)
        keep.save(data)

    # print_data(conf)

if __name__ == "__main__":
    logmon_path()