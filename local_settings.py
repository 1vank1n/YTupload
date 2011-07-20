# -*- coding: utf-8 -*-
import os
def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

# encode
ENCODE_DIR_FROM = rel('encode_from')
ENCODE_DIR_TO = rel('encode_to')
YT_LOGIN = ''
YT_PASSWORD = ''