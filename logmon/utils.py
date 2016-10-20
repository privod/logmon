import sys


def print_enc(str):
    print(str_enc(str))


def str_enc(str):
    return str.encode().decode(sys.stdout.encoding)