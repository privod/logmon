import re
from datetime import datetime
from log import Log, Level, pars_letter, letter_list

file_name = "test.log"


class LogParser:
    def __init__(self, level_monitor = Level.WARN):
        self._sep_reg = re.compile('([{}]) (\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d\.\d\d\d): '.format(''.join(letter_list())).encode())
        self._level_monitor = level_monitor

    def _text_decode(self, text_bytes, encoding_list):
        for encoding in encoding_list:
            try:
                return text_bytes.decode(encoding)
            except:
                continue
        return str(text_bytes)

    def pars(self, log_bytes):
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
            except Exception as err:
                print('Ошибка разбора даты: ', err)
                continue

            text = self._text_decode(text_bytes, ['ascii', 'cp1251', 'utf-8'])

            log = Log(level, date, text)
            log_list.append(log)

        return log_list


with open(file_name, 'rb') as file:

    log_list = LogParser().pars(file.read())

    for log in log_list:
        print(log)
