import asyncio
import ssl
from typing import Optional

import certifi
from aiohttp import ClientSession, TCPConnector
from aiohttp.typedefs import StrOrURL

from .exceptions import CryptoPayAPIError


class BaseClient:
    """Base aiohttp client"""

    def __init__(self) -> None:
        """
        Set defaults on object init.
            By default `self._session` is None.
            It will be created on a first API request.
            The second request will use the same `self._session`.
        """
        self._loop = asyncio.get_event_loop()
        self._session: Optional[ClientSession] = None

    def get_session(self, **kwargs):
        """Get cached session. One session per instance."""
        if isinstance(self._session, ClientSession) and not self._session.closed:
            return self._session

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = TCPConnector(ssl=ssl_context)

        self._session = ClientSession(connector=connector, **kwargs)
        return self._session

    async def _make_request(self, method: str, url: StrOrURL, **kwargs) -> dict:
        """
        Make a request.
            :param method: HTTP Method
            :param url: endpoint link
            :param kwargs: data, params, json and other...
            :return: status and result or exception
        """
        session = self.get_session(**kwargs)

        async with session.request(method, url, **kwargs) as response:
            response = await response.json(content_type="application/json")
        return self._validate_response(response)

    def _validate_response(self, response: dict) -> dict:
        """Validate response"""
        if response.get("ok") == False:
            name = response["error"]["name"]
            code = response["error"]["code"]
            raise CryptoPayAPIError(code, name)
        return response

    async def close(self):
        """Close the session graceful."""
        if not isinstance(self._session, ClientSession):
            return

        if self._session.closed:
            return

        await self._session.close()
