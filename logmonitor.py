import re
from datetime import datetime
from log import Log, Level, pars_letter, letter_list

file_name = "test.log"
level_monitor = Level.WARN

reg = re.compile('([{}]) (\d\d\d\d\.\d\d.\d\d \d\d:\d\d:\d\d\.\d\d\d): '.format(''.join(letter_list())).encode())
pos = 0


def text_decode(text_bytes, encoding_list):
    for encoding in encoding_list:
        try:
            return text_bytes.decode(encoding)
        except :
            continue
    return str(text_bytes)

log_list = []
with open(file_name, 'rb') as file:

    file_bytes = file.read()
    result = reg.split(file_bytes)
    # print(result)

    for letter, date_bytes, text_bytes in zip(result[1::3], result[2::3], result[3::3]):

        try:
            level = pars_letter(letter.decode())
        except Exception as err:
            print('Ошибка разбора уровня логирования: ', err)
            continue

        try:
            date = datetime.strptime(date_bytes.decode(), '%Y.%m.%d %H:%M:%S.%f')
        except Exception as err:
            print('Ошибка разбора даты: ', err)
            continue

        text = text_decode(text_bytes, ['ascii', 'cp1251', 'utf-8'])

        log = Log(level, date, text)
        log_list.append(log)

    for log in filter(lambda log: log.get_level().value <= level_monitor.value, log_list):
        print(log)

    # for line in file.readlines():
    #
    #     res = reg.match(line)
    #     if res is not None:
    #
    #         if log_item is not None:
    #             log_list.append(log_item)
    #
    #         if log_item.get_level() > level_monitor:
    #             continue
    #
    #         log_item = log.Log(res.group(1))
    #         log_item.set_date(datetime.strptime(res.group(2), '%Y.%m.%d %H:%M:%S.%f'))
    #         log_item.set_text(res.group(3))
    #
    #     elif log_item is not None:
    #         log_item.add_text(line)

    # log_byte_list = file.read()
    # pos_prev = 0
    # log_prev = None
    # for pos in range(len(log_byte_list)):
    #
    #     try:
    #         level = pars_letter(log_byte_list[pos:pos + 1].decode())
    #         date_str = log_byte_list[pos + 2:pos + 25].decode()
    #         date = datetime.strptime(date_str, '%Y.%m.%d %H:%M:%S.%f')
    #     except:
    #         continue
    #
    #     log = Log(level, date)
    #
    #     if log_prev is not None:
    #         log_prev.set_text(log_byte_list[pos_prev:pos - 1])
    #         log_list.append(log_prev)
    #         print(log_prev)
    #
    #     log_prev = log
    #     pos_prev = pos + 26
    #
    # log_prev.set_text(log_byte_list[pos_prev:])
    # log_list.append(log_prev)
    #
    # print(pos)
