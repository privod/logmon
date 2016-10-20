import json
import os
import sys

from logmon.log import Level

_file_name = 'logmon.cfg'
_file_name_bad = _file_name + '.bad'
_default = {
    'path': 'data',
    'level': Level.WARN.value,
    'patterns': ['*.log'],
}


def singleton(cls):
    instances = {}

    def get_instance(conf_arg=None):
        if cls not in instances:
            instances[cls] = cls(conf_arg)
        return instances[cls]
    return get_instance


@singleton
class Conf(object):
    def __init__(self, conf_arg=None):

        # Значения по умолчанию, самый низкий приоритет
        self._conf = _default

        conf_load = {}
        # Значения из конфигурационного файла, более высокий приоритет
        try:
            s = open(_file_name).read()
            conf_load = json.loads(s)
        except FileNotFoundError:
            pass
        except ValueError:
            os.rename(_file_name, _file_name_bad)

        # Новые ппареметры поумочанию добавляются в конфигурационный файл
        default_keys = set(_default.keys())
        load_keys = set(conf_load.keys())
        intersect_keys = load_keys.intersection(default_keys)
        new_keys = default_keys - intersect_keys
        if new_keys:
            for key in new_keys:
                self._conf.setdefault(key, _default.get(key))
            json.dump(self._conf, open(_file_name, 'w'), indent=2, sort_keys=True)
        self._set_conf(conf_load)

        # Агрумены командной строки, более высокий приоритет
        conf_sys = {}
        try:
            conf_sys['path']= sys.argv[1]
            conf_sys['level']= sys.argv[2]
            conf_sys['patterns'] = sys.argv[3:]
        except:
            pass
        self._set_conf(conf_sys)

        # Агрумены конструктора, более высокий приоритет
        self._set_conf(conf_arg)

        self._conf['level'] = Level(self.get('level'))

    def get(self, key):
        return self._conf.get(key)

    def _set_conf(self, conf):
        if conf is not None:
            for key, val in conf.items():
                self._conf[key] = val
