from enum import Enum

token = '683661784:AAFP9ev0XO7-uVDocIAyVnxwmjdepFPCCx8'

db_file = '/home/user/databases/users.db'

host_ip = '185.111.219.232'

ssl_cert = '/home/user/scripts/webhook_cert.pem'
ssl_priv = '/home/user/scripts/webhook_pkey.pem'

client_secret_calendar = '/home/user/scripts/main/client_secret.json'

calendar_id = 'gfcarwash.bot@gmail.com'


class States(Enum):

    S_START = "1"
