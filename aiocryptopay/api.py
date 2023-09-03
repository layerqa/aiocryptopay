from .base import BaseClient
from .const import HTTPMethods, Networks, Assets, PaidButtons, InvoiceStatus

from .models.profile import Profile
from .models.balance import Balance
from .models.rates import ExchangeRate
from .models.currencies import Currency
from .models.invoice import Invoice
from .models.transfer import Transfer
from .models.update import Update

from .utils.exchange import get_rate, get_rate_summ

from hmac import HMAC
from hashlib import sha256
from typing import Optional, Union, List, Callable

from aiohttp.web import Response
from aiohttp.web_request import Request


class AioCryptoPay(BaseClient):
    """
    CryptoPay API client.
        Consists of API methods only.
        All other methods are hidden in the BaseClient.
    """

    API_DOCS = "https://help.crypt.bot/crypto-pay-api"

    def __init__(
        self, token: str, network: Union[str, Networks] = Networks.MAIN_NET
    ) -> None:
        super().__init__()
        """
        Init CryptoPay API client
            :param token: Your API token from @CryptoBot
            :param network: Network address https://help.crypt.bot/crypto-pay-api#HYA3
        """
        self.__token = token
        self.network = network
        self.__headers = {"Crypto-Pay-API-Token": token}
        self._handlers = []

    async def get_me(self) -> Profile:
        """
        Use this method to test your app's authentication token. Requires no parameters. On success, returns basic information about an app.
        https://help.crypt.bot/crypto-pay-api#getMe

        Returns:
            Profile: App profile
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/getMe"

        response = await self._make_request(
            method=method, url=url, headers=self.__headers
        )
        return Profile(**response["result"])

    async def get_balance(self) -> List[Balance]:
        """
        Use this method to get a balance of your app. Returns array of assets.
        https://help.crypt.bot/crypto-pay-api#getBalance

        Returns:
            List[Balance]: Balances in list
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/getBalance"

        response = await self._make_request(
            method=method, url=url, headers=self.__headers
        )
        return [Balance(**balance) for balance in response["result"]]

    async def get_exchange_rates(self) -> List[ExchangeRate]:
        """
        Use this method to get exchange rates of supported currencies. Returns array of currencies.
        https://help.crypt.bot/crypto-pay-api#getExchangeRates

        Returns:
            List[ExchangeRates]: ExchangeRates in list
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/getExchangeRates"

        response = await self._make_request(
            method=method, url=url, headers=self.__headers
        )
        return [ExchangeRate(**rate) for rate in response["result"]]

    async def get_currencies(self) -> List[Currency]:
        """
        Use this method to get a list of supported currencies. Returns array of currencies.
        https://help.crypt.bot/crypto-pay-api#getCurrencies

        Returns:
            List[Currencies]: Currencies in list
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/getCurrencies"

        response = await self._make_request(
            method=method, url=url, headers=self.__headers
        )
        return [Currency(**currency) for currency in response["result"]]

    async def create_invoice(
        self,
        asset: Union[Assets, str],
        amount: Union[int, float],
        description: Optional[str] = None,
        hidden_message: Optional[str] = None,
        paid_btn_name: Optional[Union[PaidButtons, str]] = None,
        paid_btn_url: Optional[str] = None,
        payload: Optional[str] = None,
        allow_comments: Optional[bool] = None,
        allow_anonymous: Optional[bool] = None,
        expires_in: Optional[int] = None,
    ) -> Invoice:
        """
        Use this method to create a new invoice. On success, returns an object of the created invoice.
        https://help.crypt.bot/crypto-pay-api#createInvoice

        Args:
            asset (Union[Assets, str]): Currency code. Supported assets: “BTC”, “TON”, “ETH”, “USDT”, “USDC” and “BUSD”.
            amount (Union[int, float]): Amount of the invoice in float or int. For example: 125.50
            description (Optional[str], optional): Description for the invoice. User will see this description when they pay the invoice. Up to 1024 characters.
            hidden_message (Optional[str], optional): Text of the message that will be shown to a user after the invoice is paid. Up to 2o48 characters.
            paid_btn_name (Optional[Union[PaidButtons, str]], optional): Name of the button that will be shown to a user after the invoice is paid.
            paid_btn_url (Optional[str], optional): Required if paid_btn_name is used.URL to be opened when the button is pressed. You can set any success link (for example, a link to your bot). Starts with https or http.
            payload (Optional[str], optional): Any data you want to attach to the invoice (for example, user ID, payment ID, ect). Up to 4kb.
            allow_comments (Optional[bool], optional): Allow a user to add a comment to the payment. Default is true.
            allow_anonymous (Optional[bool], optional): Allow a user to pay the invoice anonymously. Default is true.
            expires_in (Optional[int], optional): You can set a payment time limit for the invoice in seconds. Values between 1-2678400 are accepted.

        Returns:
            Invoice: Invoice object
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/createInvoice"

        params = {
            "asset": asset,
            "amount": amount,
            "description": description,
            "hidden_message": hidden_message,
            "paid_btn_name": paid_btn_name,
            "paid_btn_url": paid_btn_url,
            "payload": payload,
            "allow_comments": allow_comments,
            "allow_anonymous": allow_anonymous,
            "expires_in": expires_in,
        }

        for key, value in params.copy().items():
            if isinstance(value, bool):
                params[key] = str(value).lower()
            if value is None:
                del params[key]

        response = await self._make_request(
            method=method, url=url, params=params, headers=self.__headers
        )
        return Invoice(**response["result"])

    async def get_invoices(
        self,
        asset: Optional[Union[Assets, str]] = None,
        invoice_ids: Optional[Union[List[int], int]] = None,
        status: Optional[Union[InvoiceStatus, str]] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Optional[Union[Invoice, List[Invoice]]]:
        """
        Use this method to get invoices of your app. On success, returns array of invoices.
        https://help.crypt.bot/crypto-pay-api#getInvoices

        Args:
            asset (Optional[Union[Assets, str]], optional): Currency codes separated by comma. Supported assets: “BTC”, “TON”, “ETH”, “USDT”, “USDC” and “BUSD”. Defaults to all assets.
            invoice_ids (Optional[Union[List[int], int]], optional): Invoice IDs separated by comma (list in python).
            status (Optional[Union[InvoiceStatus, str]], optional): Status of invoices to be returned. Available statuses: “active” and “paid”. Defaults to all statuses.
            offset (Optional[int], optional): Offset needed to return a specific subset of invoices. Default is 0.
            count (Optional[int], optional): Number of invoices to be returned. Values between 1-1000 are accepted. Default is 100.

        Returns:
            Optional[Union[Invoice, List[Invoice]]]: Invoice object or list of Invoices
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/getInvoices"

        if invoice_ids and type(invoice_ids) == list:
            invoice_ids = ",".join(map(str, invoice_ids))

        params = {
            "asset": asset,
            "invoice_ids": invoice_ids,
            "status": status,
            "offset": offset,
            "count": count,
        }

        for key, value in params.copy().items():
            if value is None:
                del params[key]

        response = await self._make_request(
            method=method, url=url, params=params, headers=self.__headers
        )
        if len(response["result"]["items"]) > 0:
            if invoice_ids and isinstance(invoice_ids, int):
                return Invoice(**response["result"]["items"][0])
            return [Invoice(**invoice) for invoice in response["result"]["items"]]

    async def transfer(
        self,
        user_id: int,
        asset: Union[Assets, str],
        amount: Union[int, float],
        spend_id: Union[str, int],
        comment: Optional[str] = None,
        disable_send_notification: Optional[bool] = None,
    ) -> Transfer:
        """
        Use this method to send coins from your app's balance to a user. On success, returns object of completed transfer.
        https://help.crypt.bot/crypto-pay-api#transfer

        Args:
            user_id (int): Telegram user ID. User must have previously used @CryptoBot (@CryptoTestnetBot for testnet).
            asset (Union[Assets, str]): Currency code. Supported assets: “BTC”, “TON”, “ETH”, “USDT”, “USDC” and “BUSD”.
            amount (Union[int, float]): Amount of the transfer in float.
            spend_id (Union[str, int]): Unique ID to make your request idempotent and ensure that only one of the transfers with the same spend_id is accepted from your app.
            comment (Optional[str], optional): Comment for the transfer. Users will see this comment when they receive a notification about the transfer.
            disable_send_notification (Optional[bool], optional): Pass true if the user should not receive a notification about the transfer. Default is false.

        Returns:
            Transfer: Transfer object
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/transfer"

        params = {
            "user_id": user_id,
            "asset": asset,
            "amount": amount,
            "spend_id": spend_id,
            "comment": comment,
            "disable_send_notification": disable_send_notification,
        }

        for key, value in params.copy().items():
            if isinstance(value, bool):
                params[key] = str(value).lower()
            if value is None:
                del params[key]

        response = await self._make_request(
            method=method, url=url, params=params, headers=self.__headers
        )
        return Transfer(**response["result"])

    def check_signature(self, body_text: str, crypto_pay_signature: str) -> bool:
        """
        https://help.crypt.bot/crypto-pay-api#verifying-webhook-updates

        Args:
            body_text (str): webhook update body
            crypto_pay_signature (str): Crypto-Pay-Api-Signature header

        Returns:
            bool: is cryptopay api signature
        """
        token = sha256(string=self.__token.encode("UTF-8")).digest()
        signature = HMAC(
            key=token, msg=body_text.encode("UTF-8"), digestmod=sha256
        ).hexdigest()
        return signature == crypto_pay_signature

    async def get_updates(self, request: Request) -> Response:
        """
        WebHook updates route

        Args:
            request (Request): WebHook request

        Returns:
            Response: 200 status code for cryptopay api
        """
        body = await request.json()
        body_text = await request.text()
        crypto_pay_signature = request.headers.get(
            "Crypto-Pay-Api-Signature", "No value"
        )
        signature = self.check_signature(
            body_text=body_text, crypto_pay_signature=crypto_pay_signature
        )
        if signature:
            for handler in self._handlers:
                await handler(Update(**body), request.app)
            return Response(text="Status OK!")

    async def get_amount_by_fiat(
        self, summ: Union[int, float], asset: Union[Assets, str], target: str
    ) -> Union[int, float]:
        """Get amount in crypto by fiat summ

        Args:
            summ (Union[int, float]): Summ in fiat.
            asset (Union[Assets, str]): Crypto currency code.
            target (str): Fiat currency code.

        Returns:
            Union[int, float]: Amount in crypto
        """
        rates = await self.get_exchange_rates()
        rate = get_rate(source=asset, target=target, rates=rates)
        fiat_summ = get_rate_summ(summ=summ, rate=rate)
        return fiat_summ

    def register_pay_handler(self, func: Callable) -> None:
        """
        Register handler when invoice paid.

        Args:
            func (Callable): Handler function
        """
        self._handlers.append(func)

    def pay_handler(self, func: Callable = None):
        def decorator(handler):
            self._handlers.append(handler)
            return handler

        return decorator
