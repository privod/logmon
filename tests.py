from unittest import TestCase

from datetime import datetime
from logmonitor.log import Parser, Level


class LogTestCase(TestCase):
    def test_parser(self):
        with open('logmonitor/testdata/test.log', 'rb') as file:
            log_bytes = file.read()

            log_list = Parser(Level.INFO).pars(log_bytes, datetime(2016, 6, 24, 12, 30))
            self.assertEqual(log_list[0].get_text(), 'i = 160	yuid.uid = 8748	yuid.type_letter = 0\r\n')

            # log_list = Parser(Level.INFO).pars(log_bytes, datetime(2016, 6, 24, 12, 59, 59))
            # for log in log_list:
            #     print(log)
