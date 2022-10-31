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