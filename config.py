from enum import Enum

token = '683661784:AAFP9ev0XO7-uVDocIAyVnxwmjdepFPCCx8'

db_file = '/database.db'

host_ip = '185.111.219.232'


class States(Enum):

    START = "0"
    ENTER_TEXT = '1'
    TEXT_ADDED = '2'
