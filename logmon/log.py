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

    def __str__(self):
        return self.name


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


class Log():

    def __init__(self, level, date, text):
        super().__init__()
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

    def get_date(self):
        return self._date

    def get_text(self):
        return self._text

    def __str__(self):
        return " ".join([self.get_level().name, str(self._date), self.get_text()])

    def __repr__(self):
        return str(self)


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

    def pars(self, log_bytes, date_begin=None, bar_title=None):
        parsed_bytes = self._sep_reg.split(log_bytes)
        log_list = []
        count_log = len(parsed_bytes[1::3])

        # if not bar_title:
        #     widgets = None
        # else:
        #     widgets = [
        #         bar_title, ': ',
        #         progressbar.Bar(),  ' (',
        #         progressbar.SimpleProgress(), ') ',
        #         progressbar.Percentage(),
        #     ]
        # bar = progressbar.ProgressBar(max_value=count_log, widgets=widgets).start()

        parsed_zip = zip(parsed_bytes[1::3], parsed_bytes[2::3], parsed_bytes[3::3], range(count_log))
        for letter, date_bytes, text_bytes, i in parsed_zip:

            try:
                level = pars_letter(letter.decode())
                if level.value > self._level_monitor.value:
                    continue
            except Exception as err:
                print('Ошибка разбора уровня логирования: {}'.format(err))
                continue

            try:
                date = datetime.strptime(date_bytes.decode(), '%Y.%m.%d %H:%M:%S.%f')
                if date_begin is not None and date < date_begin:
                    continue
            except Exception as err:
                print('Ошибка разбора даты: {}'.format(err))
                continue

            text = _text_decode(text_bytes, ['ascii', 'cp1251', 'utf-8'])
            text = re.sub('\s+$', '', text)

            log = Log(level, date, text)
            log_list.append(log)

            # if (i * 100) % count_log == 0:
            # bar.update(i)
        # bar.finish()
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
