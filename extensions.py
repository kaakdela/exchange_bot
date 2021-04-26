import json
import requests

from config import keys, my_key

class ConverterExceptions(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise ConverterExceptions('Неверное количество параметров')
        quote, base, amount = values

        if quote == base:
            raise ConverterExceptions(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_form = keys[quote]
        except KeyError:
            raise ConverterExceptions(f'Нет такой валюты{quote}')
        try:
            base_form = keys[base]
        except KeyError:
            raise ConverterExceptions(f'Нет такой валюты{base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConverterExceptions(f'Не удалоссь обработать количество {amount}')

        # r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
        r = requests.get(f'http://data.fixer.io/api/latest?access_key={my_key}&base={quote_form}&symbols={base_form}')
        text = round(float(json.loads(r.content)['rates'][base_form]) * float(amount), 2)
        return text

