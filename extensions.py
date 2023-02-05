import requests
import json
from config import Currency


class ApiException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = Currency[base.lower()]
        except KeyError:
            raise ApiException(f"Валюта {base} не найдена!")

        try:
            target_key = Currency[quote.lower()]
        except KeyError:
            raise ApiException(f"Валюта {quote} не найдена!")

        if base_key == target_key:
            raise ApiException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ApiException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/7d998f2da711a5fd2592f13f/pair/{base_key}/{target_key}')
        resp = json.loads(r.content)
        new_price = resp['conversion_rate'] * float(amount)
        return round(new_price, 2)
