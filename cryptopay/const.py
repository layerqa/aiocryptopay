from enum import Enum


class HTTPMethods(str, Enum):
    '''Available HTTP methods.'''

    POST = 'POST'
    GET = 'GET'

class Networks(str, Enum):
    '''Cryptobot networks'''

    MAIN_NET = 'https://pay.crypt.bot'
    TEST_NET = 'https://testnet-pay.crypt.bot'