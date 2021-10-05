import datetime as dt
FORMAT = '%d.%m.%Y'

class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, FORMAT).date()

class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, Record):
        self.records.append(Record)

    def get_today_stats(self):
        now = dt.datetime.now().date()
        result = sum([record.amount for record in self.records
                     if record.date == now])
        return result

    def get_week_stats(self):
        '''days=7'''
        now = dt.datetime.now().date()
        past_week = now - dt.timedelta(7)
        week_result = sum(record.amount for record in self.records
                          if past_week <= record.date <= now)
        return week_result   

class CashCalculator(Calculator):
     RUB_RATE = 1.0
     USD_RATE = 60.0
     EURO_RATE = 70.0
                  
     def get_today_cash_remained(self, hello=None):
          cash_result = self.get_today_stats()
          currency_dict = {'rub': (1.0, 'руб'),
                           'usd': (self.USD_RATE, 'USD'),
                           'eur': (self.EURO_RATE, 'Euro'),
          }
          abbr, coin = currency_dict[hello]
          fiat = round((self.limit-cash_result)/abbr,2)
          if cash_result < self.limit:
               output = f'На сегодня осталось {fiat} {coin}'
          elif cash_result == self.limit: 
               output = 'Денег нет, держись'
          else:
               if fiat < 0:
                    cash = abs(fiat)
                    output = f'Денег нет, держись: твой долг - {cash} {coin}'     
          return output            

class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_result = self.limit - self.get_today_stats()
        if calories_result > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более {calories_result} кКал')
        return 'Хватит есть!'
