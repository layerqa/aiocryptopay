## **[@cryptobot](https://t.me/CryptoBot) asynchronous api wrapper**
**Docs:** https://help.crypt.bot/crypto-pay-api

 - MainNet - [@CryptoBot](http://t.me/CryptoBot)
 - TestNet - [@CryptoTestnetBot](http://t.me/CryptoTestnetBot)


``` python
from cryptopay import AioCryptoPay, Networks

api = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)

profile = await api.get_me()
print(profile)
```