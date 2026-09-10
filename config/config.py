from dotenv import load_dotenv
from pathlib import Path
import os
from urllib.parse import quote

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path, override=True)


class SUOP:
    BASE_URL = os.getenv('BASE_URL')
    BASIC_AUTH_LOGIN = os.getenv('BASIC_AUTH_LOGIN')
    BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD')

    if not BASE_URL:
        raise RuntimeError('BASE_URL is not configured')

    ENCODED_PASSWORD = quote(BASIC_AUTH_PASSWORD or '')

    if BASIC_AUTH_LOGIN and BASIC_AUTH_PASSWORD:
        if '://' in BASE_URL:
            protocol, rest = BASE_URL.split('://', 1)
            MAIN_URL = f'{protocol}://{BASIC_AUTH_LOGIN}:{ENCODED_PASSWORD}@{rest}'
        else:
            MAIN_URL = f'https://{BASIC_AUTH_LOGIN}:{ENCODED_PASSWORD}@{BASE_URL}'
    else:
        MAIN_URL = BASE_URL

    CLIENT_LOGIN = os.getenv('CLIENT_LOGIN')
    CLIENT_PASSWORD = os.getenv('CLIENT_PASSWORD')
    ORGANIZATION_CLIENT = os.getenv('ORGANIZATION_CLIENT')
    ORGANIZATION_MANAGER = os.getenv('ORGANIZATION_MANAGER')
    ORGANIZATION_ADMIN = os.getenv('ORGANIZATION_ADMIN')
