import re
from enum import Enum
from datetime import datetime


class Level(Enum):
    EMERG = 0
    ALERT = 1
    CRIT = 2
    ERROR = 3
    WARN = 4
    NOTICE = 5
    INFO = 6
    DEBUG = 7
    VERBOSE = 8

_letterToLevel = {
    'M': Level.EMERG,
    'A': Level.ALERT,
    'C': Level.CRIT,
    'E': Level.ERROR,
    'W': Level.WARN,
    'N': Level.NOTICE,
    'I': Level.INFO,
    'D': Level.DEBUG,
    'V': Level.VERBOSE,
}


def pars_letter(letter):
    return _letterToLevel.get(letter)


def letter_list():
    return _letterToLevel.keys()


class Log:

    def __init__(self, level, date, text):
        self._level = level
        self._date = date
        self._text = text

    def set_date(self, date):
        self._date = date

    def set_text(self, text):
        self._text = text

    def add_text(self, text):
        self._text.append(text)

    def get_level(self):
        return self._level

    def get_text(self):
        return self._text

    def __str__(self):
        return " ".join([self.get_level().name, str(self._date), self.get_text()])


def _text_decode(text_bytes, encoding_list):
    for encoding in encoding_list:
        try:
            return text_bytes.decode(encoding)
        except ValueError:
            continue
    return str(text_bytes)


class Parser:
    def __init__(self, level_monitor=Level.WARN):
        self._sep_reg = re.compile(
            '([{}]) (\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d\.\d\d\d): '.format(''.join(letter_list())).encode()
        )
        self._level_monitor = level_monitor

    def pars(self, log_bytes, date_begin=None):
        parsed_bytes = self._sep_reg.split(log_bytes)

        log_list = []
        for letter, date_bytes, text_bytes in zip(parsed_bytes[1::3], parsed_bytes[2::3], parsed_bytes[3::3]):

            try:
                level = pars_letter(letter.decode())
                if level.value > self._level_monitor.value:
                    continue
            except Exception as err:
                print('Ошибка разбора уровня логирования: ', err)
                continue

            try:
                date = datetime.strptime(date_bytes.decode(), '%Y.%m.%d %H:%M:%S.%f')
                if date_begin is not None and date < date_begin:
                    continue
            except Exception as err:
                print('Ошибка разбора даты: ', err)
                continue

            text = _text_decode(text_bytes, ['ascii', 'cp1251', 'utf-8'])

            log = Log(level, date, text)
            log_list.append(log)

        return log_list


# _levelToName = {
#     EMERG: 'EMERG',
#     ALERT: 'ALERT',
#     CRIT: 'CRIT',
#     ERROR: 'ERROR',
#     WARN: 'WARN',
#     NOTICE:'NOTICE',
#     INFO: 'INFO',
#     DEBUG: 'DEBUG',
#     VERBOSE: 'VERBOSE',
# }

# _levelToLetter = {
#     EMERG:  'M',
#     ALERT:  'A',
#     CRIT:   'C',
#     ERROR:  'E',
#     WARN:   'W',
#     NOTICE: 'N',
#     INFO:   'I',
#     DEBUG:  'D',
#     VERBOSE:'V',
# }
