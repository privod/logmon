from enum import Enum


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

    def __str__(self):
        try:
            text = self._text.decode('utf-8')
        except:
            text = str(self._text)
        return " ".join([self._level.name, str(self._date), text])

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