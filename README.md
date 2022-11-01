## **[@cryptobot](https://t.me/CryptoBot) asynchronous api wrapper**
**Docs:** https://help.crypt.bot/crypto-pay-api

 - MainNet - [@CryptoBot](http://t.me/CryptoBot)
 - TestNet - [@CryptoTestnetBot](http://t.me/CryptoTestnetBot)


**Install**
``` bash
pip install aiocryptopay
poetry add aiocryptopay
```

**Basic methods**
``` python
from aiocryptopay import AioCryptoPay, Networks

api = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)

profile = await api.get_me()
currencies = await api.get_currencies()
balance = await api.get_balance()
rates = await api.get_exchange_rates()

print(profile, currencies, balance, rates, sep='\n')
```

**Create and get invoice methods**
``` python
from aiocryptopay import AioCryptoPay, Networks

api = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)

invoice = await api.create_invoice(asset='TON', amount=1.5)
print(invoice.pay_url)

invoices = await api.get_invoices(invoice_ids=invoice.invoice_id)
print(invoices.status)
```

**WebHook usage**
``` python
from aiohttp import web

from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.update import Update


web_app = web.Application()
crypto = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)


@crypto.pay_handler()
async def invoice_paid(update: Update) -> None:
    print(update)

async def create_invoice(app) -> None:
    invoice = await crypto.create_invoice(asset='TON', amount=1.5)
    print(invoice.pay_url)


web_app.add_routes([web.post('/crypto-secret-path', crypto.get_updates)])
web_app.on_startup.append(create_invoice)
web.run_app(app=web_app, host='localhost', port=3001)
```