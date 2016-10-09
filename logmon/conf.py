import json
import os.path
import sys


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance


@singleton
class Conf:
    _file_name = 'logmon.cfg'
    _default = {
        'path': 'data',
        'patterns': ['*.log'],
    }

    def __init__(self, conf_arg=None):

        # Значения по умолчанию, самый низкий приоритет
        self._conf = Conf._default

        # Значения из конфигурационного файла, более высокий приоритет
        if os.path.isfile(Conf._file_name):
            conf_load = json.load(open(Conf._file_name))
            self._set_conf(conf_load)
        # Новые ппареметры поумочанию добавляются в конфигурационный файл
        default_keys = set(self._default.keys())
        conf_keys = set(self._conf.keys())
        intersect_keys = conf_keys.intersection(default_keys)
        new_keys = default_keys - intersect_keys
        if new_keys:
            for key in new_keys:
                self._conf.setdefault(key, self._default.get(key))
            json.dump(self._conf, open(Conf._file_name))

        # Агрумены командной строки, более высокий приоритет
        self._set_conf(sys.argv[1:])

        # Агрумены конструктора, более высокий приоритет
        self._set_conf(conf_arg)

    def _set_conf(self, conf):
        for key, val in conf:
            self._conf.setdefault(key, val)
