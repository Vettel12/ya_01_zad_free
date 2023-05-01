import datetime as dt
from typing import Optional
date_format: str = '%d.%m.%Y'
'''Калькулятор денег и калорий'''


class Calculator:
    '''Родительский класс Calculator принимает один
    аргумент - limit (дневной лимит трат/калорий).
    В конструкторе создается пустой список records
    для хранения записей. Имеется три общих функции.
    Метод add_record нужен для создания записей в
    records. Метод get_today_stats для подсчета за
    день съединных калорий и потраченных денег.
    Метод get_week_stats для того же, но за
    последние 7 дней.'''

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_record):

        self.records.append(new_record)

    def get_today_stats(self):

        self.count: float = 0

        for record in self.records:
            # print(dt.datetime.now().date())
            if record.date == dt.datetime.now().date():
                self.count += record.amount

        return self.count

    def get_week_stats(self):

        offset_week = dt.datetime.now().date() - dt.timedelta(days=7)
        return sum(
            day.amount for day in self.records
            if offset_week <= day.date <= dt.datetime.now().date())


class Record:
    '''Класс для создания записей. На входе три
    аргумента - это amount (кал. или деньги),
    date (необязательно, то тогда текущая),
    comment (комментарии, необязательно).'''

    def __init__(self, amount: int,
                 date: Optional[str] = None, comment: str = None):

        self.amount = amount

        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()
        self.comment = comment


class CaloriesCalculator(
        Calculator):
    '''Класс Калькулятора калорий наследует свойства Calculator.
    Метод get_calories_remained считает сколько калорий потрачено
    и сколько еще можно съесть или нельзя'''

    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):

        today_calories = super().get_today_stats()

        if today_calories < self.limit:
            message = f'Сегодня можно съесть что-нибудь ещё, ' \
                      f'но с общей калорийностью не более' \
                      f' {self.limit - today_calories} кКал'
        else:
            message = 'Хватит есть!'

        return message


class CashCalculator(Calculator):
    '''Класс Калькулятора денег наследует свойства Calculator.
    Метод get_today_cash_remained переводит валюты в руб.,
    проверяет сколько еще можно потратить или нельзя.'''

    USD_RATE: float = 60.00
    EURO_RATE: float = 70.00
    RUB_RATE: float = 1.00

    all_currency = {
        'usd': ('USD', USD_RATE),
        'eur': ('Euro', EURO_RATE),
        'rub': ('руб', RUB_RATE),
    }

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency: str):

        if currency not in self.all_currency:
            raise ValueError('Валюта введена некорректно')

        currency_name, currency_course = self.all_currency[currency]

        today_cash = round(
            (self.limit - super().get_today_stats()) / currency_course, 2)

        if today_cash > 0:
            message = f'На сегодня осталось {today_cash} {currency_name}'
        elif today_cash == 0:
            message = 'Денег нет, держись'
        else:
            message = f'Денег нет, держись: твой долг ' \
                f'- {abs(today_cash)} {currency_name}'
        return message


if __name__ == "__main__":
    limit = 1000
    cash_calculator = CashCalculator(limit)
    calories_calculator = CaloriesCalculator(limit)

    # записи для денег
    r1 = Record(amount=145, comment='кофе')
    r2 = Record(amount=300, comment='Серёге за обед')
    r3 = Record(
        amount=3000,
        comment='Бар на Танин день рождения',
        date='08.11.2022')

    # записи для калорий
    r4 = Record(
        amount=118,
        comment='Кусок тортика. И ещё один.')
    r5 = Record(
        amount=84,
        comment='Йогурт.')
    r6 = Record(
        amount=1140,
        comment='Баночка чипсов.',
        date='24.02.2019')

    cash_calculator.add_record(r1)
    cash_calculator.add_record(r2)
    cash_calculator.add_record(r3)

    calories_calculator.add_record(r4)
    calories_calculator.add_record(r5)
    calories_calculator.add_record(r6)

    # вывод результатов
    print(cash_calculator.get_today_cash_remained('rub'))
    print(calories_calculator.get_calories_remained())
