from datetime import datetime
from time import time, sleep
import os.path
from glob import glob

from progressbar import Bar
from progressbar import Percentage
from progressbar import ProgressBar
from progressbar import SimpleProgress
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from logmon.log import Parser
from logmon.conf import Conf
import logmon.keeping as keep


class Handler(PatternMatchingEventHandler):

    def __init__(self,patterns=None, ignore_patterns=None,
                 ignore_directories=False, case_sensitive=False, mon_pool_file_name=None):
        super().__init__(patterns, ignore_patterns, ignore_directories, case_sensitive)
        self._mon_pool_file_name = mon_pool_file_name

    def on_modified(self, event):
        # print(event)
        # print('Новый файл лога: ', event.src_path)
        self._mon_pool_file_name.add(event.src_path)


def files_parse(file_name_pool, data=None, level=Conf().get('level'), bar_widgets=None):

    file_count = len(file_name_pool)
    bar = ProgressBar(max_value=file_count, widgets=bar_widgets).start()
    while len(file_name_pool) > 0:
        file_name = os.path.normpath(file_name_pool.pop())
        file_done = file_count - len(file_name_pool)
        # print('Обработка лога {}:'.format(file_name))
        pos_beg = data.get(file_name, {'pos': 0}).get('pos')

        file_bytes = open(file_name, 'rb').read()
        parse_bytes = file_bytes[pos_beg:]
        if not parse_bytes:
            bar.update(file_done)
            # print('\tБез изменений')
            continue

        log_list = Parser(level).pars(parse_bytes, bar_title=file_name)

        data.setdefault(file_name, {'pos': 0, 'log_list': []})
        data[file_name]['log_list'].extend(log_list)
        data[file_name]['pos'] = pos_beg + len(file_bytes)
        bar.update(file_done)

    bar.finish()


# def _set_argv(argv, default=None):
#     if argv is None:
#         argv = sys.argv[1:]
#     if len(argv) == 0:
#         argv = default
#     return argv


# def print_data(data):
#     for key, val in data.items():
#         print(key)
#         for log in val['log_list']:
#             print('\t', log)


def logmon_start(conf_arg=None):
    # path, *patterns = _set_argv(argv, ['.', '*.log'])
    conf = Conf(conf_arg)

    file_name_pool = set()
    observer = Observer()
    handler = Handler(patterns=conf.get('patterns'), ignore_directories=True, mon_pool_file_name=file_name_pool)
    observer.schedule(handler, path=conf.get('path'), recursive=True)
    observer.start()

    print('Мониторинг логов на низменения')
    print('Путь: {}'.format(conf.get('path')))
    print('Шаблоны поиска: {}'.format(conf.get('patterns')))
    try:
        # data = {}
        beg_time = time()
        while True:

            sleep(1)

            # Таймер 10 минут
            if time() - beg_time > 600:
                data = keep.load()
                files_parse(file_name_pool, data, bar_widgets = [
                    datetime.now().strftime('%Y.%m.%d %H:%M:%S'), ' ',
                    SimpleProgress(format='Изменено %(max_value)d, обработано %(value)d'), ' ',
                    Bar(), ' ',
                    Percentage(),
                ])
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

    print('Обработка логов в каталоге')
    print('Путь: {}'.format(conf.get('path')))
    print('Шаблоны поиска: {}'.format(conf.get('patterns')))
    sleep(0.1)
    for pattern in conf.get('patterns'):
        file_name_pool = glob(os.path.join(conf.get('path'), pattern))
        data = keep.load()
        files_parse(file_name_pool, data)
        keep.save(data)

    sleep(0.1)
    print('Выполнено')

if __name__ == "__main__":
    logmon_path()