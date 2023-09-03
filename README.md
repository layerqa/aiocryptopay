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

crypto = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)

profile = await crypto.get_me()
currencies = await crypto.get_currencies()
balance = await crypto.get_balance()
rates = await crypto.get_exchange_rates()

print(profile, currencies, balance, rates, sep='\n')
```

**Create and get invoice methods**
``` python
from aiocryptopay import AioCryptoPay, Networks

crypto = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)

invoice = await crypto.create_invoice(asset='TON', amount=1.5)
print(invoice.pay_url)

invoices = await crypto.get_invoices(invoice_ids=invoice.invoice_id)
print(invoices.status)

# Get amount in crypto by fiat summ
amount = await crypto.get_amount_by_fiat(summ=100, asset='TON', target='USD')
invoice = await crypto.create_invoice(asset='TON', amount=amount)
print(invoice.pay_url)
```

**WebHook usage**
``` python
from aiohttp import web

from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.update import Update


web_app = web.Application()
crypto = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)


@crypto.pay_handler()
async def invoice_paid(update: Update, app) -> None:
    print(update)

async def create_invoice(app) -> None:
    invoice = await crypto.create_invoice(asset='TON', amount=1.5)
    print(invoice.pay_url)

async def close_session(app) -> None:
    await crypto.close()


web_app.add_routes([web.post('/crypto-secret-path', crypto.get_updates)])
web_app.on_startup.append(create_invoice)
web_app.on_shutdown.append(close_session)
web.run_app(app=web_app, host='localhost', port=3001)
```