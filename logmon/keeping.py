import os.path
import pickle

_db_name = 'data.db'
_db_name_bad = _db_name + '.bad'


def load():

    try:
        b = open(_db_name, 'rb').read()
        data = pickle.loads(b)
    except FileNotFoundError:
        data = {}
    except ValueError:
        data = {}
        os.rename(_db_name, _db_name_bad)

    return data


def save(data):
    open(_db_name, 'wb').write(pickle.dumps(data))
