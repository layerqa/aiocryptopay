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

**Create, get and delete invoice methods**
``` python
from aiocryptopay import AioCryptoPay, Networks

crypto = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)

invoice = await crypto.create_invoice(asset='TON', amount=1.5)
print(invoice.pay_url)

# Create invoice in fiat
fiat_invoice = await crypto.create_invoice(amount=5, fiat='USD', currency_type='fiat')
print(fiat_invoice)

old_invoice = await crypto.get_invoices(invoice_ids=invoice.invoice_id)
print(old_invoice.status)

deleted_invoice = await crypto.delete_invoice(invoice_id=invoice.invoice_id)
print(deleted_invoice)

# Get amount in crypto by fiat summ
amount = await crypto.get_amount_by_fiat(summ=100, asset='TON', target='USD')
invoice = await crypto.create_invoice(asset='TON', amount=amount)
print(invoice.pay_url)
```

**Create, get and delete check methods**
``` python
# The check creation method works when enabled in the application settings

from aiocryptopay import AioCryptoPay, Networks

crypto = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)

check = await crypto.create_check(asset='USDT', amount=1)
print(check)

old_check = await crypto.get_checks(check_ids=check.check_id)
print(old_check)

deleted_check = await crypto.delete_check(check_id=check.check_id)
print(deleted_check)
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