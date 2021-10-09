"""импорт библиотек времени/аннотаций и определение формата"""

from typing import Optional, List
import datetime as dt
FORMAT = '%d.%m.%Y'


class Record:
    """Создаем класс для хранения след. записей:
    - число amount (денежная сумма или количество килокалорий);
    - дата создания записи date (передаётся в явном виде в конструктор,
    либо присваивается значение по умолчанию — текущая дата);
    - комментарий comment (на что потрачены деньги или откуда взялись кКал).
    """

    def __init__(self, amount: float, comment: str,
                 date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, FORMAT).date()


class Calculator:
    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []
        self.now = dt.date.today()
        self.past_week = self.now - dt.timedelta(days=7)

    def add_record(self, the_record: Record) -> None:
        """Сохранение записи о расходах и приёме пищи.
        Метод принимает объект класса record и сохраняет его в списке records.
        """

        self.records.append(the_record)

    def get_today_stats(self) -> float:
        """сколько денег потрачено и
        сколько калорий съедено сегодня.
        """

        now = dt.date.today()
        return sum([record.amount for record in self.records
                     if record.date == now])

    def get_week_stats(self) -> float:
        """сколько денег/калорий потрачено 
        за последние 7 дней.
        """

        week_stats = []
        for record in self.records:
            if self.past_week <= record.date <= self.now:
                week_stats.append(record.amount)
        return sum(week_stats)       

    def today_remain(self):
        """создали метод для подсчета остатка на сегодня"""

        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    """дочерний класс Calculator
    определяет сколько денег можно потратить сегодня
    в разной валюте.
    """

    RUB_RATE = 1.0
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, hello: str) -> str:
        cash_result = self.get_today_stats()
        currency_dict = {'rub': (1.0, 'руб'),
                         'usd': (self.USD_RATE, 'USD'),
                         'eur': (self.EURO_RATE, 'Euro')}
        abbr, coin = currency_dict[hello]
        fiat = round((self.limit - cash_result) / abbr, 2)
        if cash_result == self.limit:
            output = 'Денег нет, держись'
        elif cash_result < self.limit:
            output = f'На сегодня осталось {fiat} {coin}'
        else:
            if fiat < 0:
                cash = abs(fiat)
                output = f'Денег нет, держись: твой долг - {cash} {coin}'
        return output


class CaloriesCalculator(Calculator):
    """дочерний класс Calculator
    определяет сколько калорий можно/нужно получить сегодня
    """
    def get_calories_remained(self) -> str:
        calories_result = self.today_remain()
        if calories_result > 0:
            return ('Сегодня можно съесть'
                    ' что-нибудь ещё, но с общей калорийностью'
                    f' не более {calories_result} кКал')
        return 'Хватит есть!'
