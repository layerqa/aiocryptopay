from enum import Enum


class HTTPMethods(str, Enum):
    '''Available HTTP methods.'''

    POST = 'POST'
    GET = 'GET'

class Networks(str, Enum):
    '''Cryptobot networks'''

    MAIN_NET = 'https://pay.crypt.bot'
    TEST_NET = 'https://testnet-pay.crypt.bot'

class Assets(str, Enum):
    '''Cryptobot assets'''

    BTC = 'BTC'
    TON = 'TON'
    ETH = 'ETH'
    USDT = 'USDT'
    USDC = 'USDC'
    BUSD = 'BUSD'

class PaidButtons(str, Enum):
    '''Cryptobot paid button names'''

    VIEW_ITEM = 'viewItem'
    OPEN_CHANNEL = 'openChannel'
    OPEN_BOT = 'openBot'
    CALLBACK = 'callback'

class InvoiceStatus(str, Enum):
    '''Invoice status'''

    ACTIVE = 'active'
    PAID = 'paid'
    EXPIRED = 'expired'