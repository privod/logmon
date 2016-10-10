from unittest import TestCase
from datetime import datetime
from logmon.log import Parser, Level


class LogTestCase(TestCase):
    def test_parser(self):

        log_bytes = """I 2016.06.24 12:06:29.504: xml.mread_blob...........end
I 2016.06.24 12:06:38.159: i = 160	yuid.uid = 8748	yuid.type_letter = 0
I 2016.06.24 12:06:38.284: AD230095@ncr.com
I 2016.06.24 12:06:38.299: NCR Reports...""".encode()

        log_list = Parser(Level.INFO).pars(log_bytes, datetime(2016, 6, 24, 12, 6, 30))
        self.assertEqual(log_list[0].get_text(), 'i = 160	yuid.uid = 8748	yuid.type_letter = 0')

        # log_list = Parser(Level.INFO).pars(log_bytes, datetime(2016, 6, 24, 12, 59, 59))
        # for log in log_list:
        #     print(log)
