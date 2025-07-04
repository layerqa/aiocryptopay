from .base import BaseClient
from .const import (
    HTTPMethods,
    Networks,
    Assets,
    PaidButtons,
    InvoiceStatus,
    CurrencyType,
    CheckStatus,
)

from .models.profile import Profile
from .models.balance import Balance
from .models.rates import ExchangeRate
from .models.currencies import Currency
from .models.invoice import Invoice
from .models.transfer import Transfer
from .models.update import Update
from .models.check import Check
from .models.app_stats import AppStats

from .utils.exchange import get_rate, get_rate_summ

from datetime import datetime
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

    async def get_stats(
        self,
        start_at: Optional[Union[datetime, str]] = None,
        end_at: Optional[Union[datetime, str]] = None,
    ) -> AppStats:
        """
        Use this method to get app statistics.
        http://help.crypt.bot/crypto-pay-api#jvP3

        Args:
            start_at: (Optional[Union[datetime, str]]): Date from which start calculating statistics in ISO 8601 format. Defaults is current date minus 24 hours.
            end_at: (Optional[Union[datetime, str]]): The date on which to finish calculating statistics in ISO 8601 format. Defaults is current date.

        Returns:
            AppStats: AppStats object
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/getStats"

        params = {
            "start_at": start_at,
            "end_at": end_at,
        }

        for key, value in params.copy().items():
            if isinstance(value, datetime):
                params[key] = str(value)
            if value is None:
                del params[key]

        response = await self._make_request(
            method=method, url=url, params=params, headers=self.__headers
        )
        return AppStats(**response["result"])

    async def get_balance(self) -> List[Balance]:
        """
        Use this method to get a balance of your app.
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
        amount: Union[int, float],
        asset: Optional[Union[Assets, str]] = None,
        description: Optional[str] = None,
        hidden_message: Optional[str] = None,
        paid_btn_name: Optional[Union[PaidButtons, str]] = None,
        paid_btn_url: Optional[str] = None,
        payload: Optional[str] = None,
        allow_comments: Optional[bool] = None,
        allow_anonymous: Optional[bool] = None,
        expires_in: Optional[int] = None,
        fiat: Optional[str] = None,
        currency_type: Optional[Union[CurrencyType, str]] = None,
        accepted_assets: Optional[Union[List[Union[Assets, str]], str]] = None,
        swap_to: Optional[Union[Assets, str]] = None,
    ) -> Invoice:
        """
        Use this method to create a new invoice.
        https://help.crypt.bot/crypto-pay-api#createInvoice

        Args:
            asset (Optional[Union[Assets, str]]): Currency code if the field currency_type has crypto as a value. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC”.
            amount (Union[int, float]): Amount of the invoice in float or int. For example: 125.50
            description (Optional[str], optional): Description for the invoice. User will see this description when they pay the invoice. Up to 1024 characters.
            hidden_message (Optional[str], optional): Text of the message that will be shown to a user after the invoice is paid. Up to 2o48 characters.
            paid_btn_name (Optional[Union[PaidButtons, str]], optional): Name of the button that will be shown to a user after the invoice is paid.
            paid_btn_url (Optional[str], optional): Required if paid_btn_name is used.URL to be opened when the button is pressed. You can set any success link (for example, a link to your bot). Starts with https or http.
            payload (Optional[str], optional): Any data you want to attach to the invoice (for example, user ID, payment ID, ect). Up to 4kb.
            allow_comments (Optional[bool], optional): Allow a user to add a comment to the payment. Default is true.
            allow_anonymous (Optional[bool], optional): Allow a user to pay the invoice anonymously. Default is true.
            expires_in (Optional[int], optional): You can set a payment time limit for the invoice in seconds. Values between 1-2678400 are accepted.
            fiat (Optional[str], optional): Fiat currency code if the field currency_type has fiat as a value. Supported fiat currencies: All fiats in CryptoBot
            currency_type (Optional[Union[CurrencyType, str]], optional): Type of the price, can be “crypto” or “fiat”. Default is crypto.
            accepted_assets (Optional[Union[List[Union[Assets, str]], str]], optional): Assets which can be used to pay the invoice if the field fiat has a value. Supported assets: “USDT”, “TON”, “BTC” (and “JET” for testnet). Defaults to all currencies.
            swap_to (Optional[Union[Assets, str]], optional): Asset to swap to after payment. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” и “USDC”.

        Returns:
            Invoice: Invoice object
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/createInvoice"

        if accepted_assets and type(accepted_assets) == list:
            accepted_assets = ",".join(map(str, accepted_assets))

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
            "fiat": fiat,
            "currency_type": currency_type,
            "accepted_assets": accepted_assets,
            "swap_to": swap_to,
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
        Use this method to get invoices of your app.
        https://help.crypt.bot/crypto-pay-api#getInvoices

        Args:
            asset (Optional[Union[Assets, str]], optional): Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet). Defaults to all currencies.
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

    async def delete_invoice(self, invoice_id: int) -> bool:
        """
        Use this method to delete invoices created by your app.
        http://help.crypt.bot/crypto-pay-api#34Hd

        Args:
            invoice_id (int): Invoice ID to be deleted.

        Returns:
            bool: Returns True on success.
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/deleteInvoice"

        params = {"invoice_id": invoice_id}

        response = await self._make_request(
            method=method, url=url, params=params, headers=self.__headers
        )
        return response["result"]

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
        Use this method to send coins from your app's balance to a user.
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

    async def get_transfers(
        self,
        asset: Optional[Union[Assets, str]] = None,
        transfer_ids: Optional[Union[List[int], int]] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Optional[Union[Transfer, List[Transfer]]]:
        """
        Use this method to get transfers created by your app.
        http://help.crypt.bot/crypto-pay-api#RjDU

        Args:
            asset (Optional[Union[Assets, str]], optional): Currency codes separated by comma. Supported assets: “BTC”, “TON”, “ETH”, “USDT”, “USDC” and “BUSD”. Defaults to all assets.
            transfer_ids (Optional[Union[List[int], int]], optional): List of transfer IDs separated by comma (list in python).
            offset (Optional[int], optional): Offset needed to return a specific subset of invoices. Default is 0.
            count (Optional[int], optional): Number of invoices to be returned. Values between 1-1000 are accepted. Default is 100.

        Returns:
            Optional[Union[Transfer, List[Transfer]]]: Transfer object or list of Transfers
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/getTransfers"

        if transfer_ids and type(transfer_ids) == list:
            transfer_ids = ",".join(map(str, transfer_ids))

        params = {
            "asset": asset,
            "transfer_ids": transfer_ids,
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
            if transfer_ids and isinstance(transfer_ids, int):
                return Transfer(**response["result"]["items"][0])
            return [Transfer(**transfer) for transfer in response["result"]["items"]]

    async def create_check(
        self,
        asset: Union[Assets, str],
        amount: Union[int, float],
        pin_to_user_id: Optional[int] = None,
        pin_to_username: Optional[str] = None,
    ) -> Check:
        """
        Use this method to create a new check.
        http://help.crypt.bot/crypto-pay-api#ZU9K

        Args:
            asset (Union[Assets, str]): Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet).
            amount (Union[int, float]): Amount of the invoice in float. For example: 125.50
            pin_to_user_id (Optional[int], optional) ID of the user who will be able to activate the check.
            pin_to_username (Optional[str], optional) A user with the specified username will be able to activate the check.
        Returns:
            Check: Check object
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/createCheck"

        params = {
            "asset": asset,
            "amount": amount,
            "pin_to_user_id": pin_to_user_id,
            "pin_to_username": pin_to_username,
        }

        for key, value in params.copy().items():
            if value is None:
                del params[key]

        response = await self._make_request(
            method=method, url=url, params=params, headers=self.__headers
        )
        return Check(**response["result"])

    async def get_checks(
        self,
        asset: Optional[Union[Assets, str]] = None,
        check_ids: Optional[Union[List[int], int]] = None,
        status: Optional[Union[CheckStatus, str]] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Check:
        """
        Use this method to get checks created by your app.
        http://help.crypt.bot/crypto-pay-api#nIwG

        Args:
            asset (Optional[Union[Assets, str]], optional): _description_. Defaults to None.
            check_ids (Optional[Union[List[int], int]], optional): _description_. Defaults to None.
            status (Optional[Union[CheckStatus, str]], optional): _description_. Defaults to None.
            offset (Optional[int], optional): _description_. Defaults to None.
            count (Optional[int], optional): _description_. Defaults to None.

        Returns:
            Check: Check object or list of Checks
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/getChecks"

        if check_ids and type(check_ids) == list:
            check_ids = ",".join(map(str, check_ids))

        params = {
            "asset": asset,
            "check_ids": check_ids,
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
            if check_ids and isinstance(check_ids, int):
                return Check(**response["result"]["items"][0])
            return [Check(**check) for check in response["result"]["items"]]

    async def delete_check(self, check_id: int) -> bool:
        """
        Use this method to delete checks created by your app.
        http://help.crypt.bot/crypto-pay-api#nd2L

        Args:
            check_id (int): Check ID to be deleted.

        Returns:
            bool: Returns True on success.
        """
        method = HTTPMethods.GET
        url = f"{self.network}/api/deleteCheck"

        params = {"check_id": check_id}

        response = await self._make_request(
            method=method, url=url, params=params, headers=self.__headers
        )
        return response["result"]

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

    async def __aenter__(self) -> None:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()
