from .base import BaseClient
from .const import HTTPMethods, Networks

from .models.profile import Profile
from .models.balance import Balance
from .models.rates import ExchangeRates
from .models.currencies import Currencies

from typing import Union, List


class AioCryptoPay(BaseClient):
    '''
    CryptoPay API client.
        Consists of API methods only.
        All other methods are hidden in the BaseClient.
    '''

    API_DOCS = 'https://help.crypt.bot/crypto-pay-api'

    def __init__(
        self,
        token: str,
        network: Union[str, Networks] = Networks.MAIN_NET
    ) -> None:
        super().__init__()
        '''
        Init CryptoPay API client
            :param token: Your API token from @CryptoBot
            :param network: Network address https://help.crypt.bot/crypto-pay-api#HYA3
        '''
        self.__token = token
        self.network = network
        self.__headers = {'Crypto-Pay-API-Token': token}
    
    async def get_me(self) -> Profile:
        """
        Use this method to test your app's authentication token. Requires no parameters. On success, returns basic information about an app.
        https://help.crypt.bot/crypto-pay-api#getMe

        Returns:
            Profile: App profile
        """
        method = HTTPMethods.GET
        url = f'{self.network}/api/getMe'

        response = await self._make_request(
            method=method,
            url=url,
            headers=self.__headers
        )
        return Profile(**response['result'])
    
    async def get_balance(self) -> List[Balance]:
        """
        Use this method to get a balance of your app. Returns array of assets.
        https://help.crypt.bot/crypto-pay-api#getBalance

        Returns:
            List[Balance]: Balances in list
        """
        method = HTTPMethods.GET
        url = f'{self.network}/api/getBalance'

        response = await self._make_request(
            method=method,
            url=url,
            headers=self.__headers
        )
        return [Balance(**balance) for balance in response['result']]
    
    async def get_exchange_rates(self) -> List[ExchangeRates]:
        """
        Use this method to get exchange rates of supported currencies. Returns array of currencies.
        https://help.crypt.bot/crypto-pay-api#getExchangeRates

        Returns:
            List[ExchangeRates]: ExchangeRates in list
        """
        method = HTTPMethods.GET
        url = f'{self.network}/api/getExchangeRates'

        response = await self._make_request(
            method=method,
            url=url,
            headers=self.__headers
        )
        return [ExchangeRates(**rate) for rate in response['result']]
    
    async def get_currencies(self) -> List[Currencies]:
        """
        Use this method to get a list of supported currencies. Returns array of currencies.
        https://help.crypt.bot/crypto-pay-api#getCurrencies

        Returns:
            List[Currencies]: Currencies in list
        """
        method = HTTPMethods.GET
        url = f'{self.network}/api/getCurrencies'

        response = await self._make_request(
            method=method,
            url=url,
            headers=self.__headers
        )
        return [Currencies(**currency) for currency in response['result']]