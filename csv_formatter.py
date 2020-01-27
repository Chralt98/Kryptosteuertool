import csv
import math
from datetime import datetime


class CsvFormatter:
    queue = list()
    path = ''
    output_file = ''
    output = []
    transactions = {}
    crypto_exchange = ''
    account_name = ''
    shortcut_to_itin = {'BTC': 'TP3B-248N-Q', 'ETH': 'T22F-QJGB-N', 'XMR': 'HRYR-93E4-W', 'MIOTA': 'DB8C-YKTY-7',
                        'NEO': '9QVR-R258-P',
                        'XEM': '2PTC-P6K4-H', 'EOS': 'A8YZ-WTGR-6', 'NAS': 'RACF-AZ34-H', 'XLM': 'KTG9-BP94-H',
                        'BNB': 'MMRX-72FA-8', '': 'EMPTY'}
    shortcut_to_name = {'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'XMR': 'Monero', 'MIOTA': 'IOTA', 'NEO': 'Neo',
                        'XEM': 'NEM', 'EOS': 'EOS', 'NAS': 'Nebulas', 'XLM': 'Stellar', 'BNB': 'Binance Coin',
                        '': 'EMPTY'}
    tx_mask = {'tx_id': 0, 'date': 1, 'output_typ': 2, 'input_amount': 4, 'input_asset_name': 6, 'output_amount': 7,
               'output_asset_name': 9, 'fee': 10, 'acquisition_cost': 11, 'selling_price': 12, 'capital_gain': 13,
               'holding_period': 14, 'tax_relevant_gain_loss': 15}

    def __init__(self, path, output_file, exchange_name, account_name):
        self.path = path
        self.output_file = output_file
        self.crypto_exchange = exchange_name
        self.account_name = account_name

    def write_in_csv(self):
        self.add_transactions()
        with open(self.path + self.output_file, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
            for row in self.output:
                csv_writer.writerow(row)

    def add_transactions(self):
        for asset in self.transactions:
            self.build_header(self.crypto_exchange, self.account_name, asset, self.shortcut_to_name[asset],
                              self.shortcut_to_itin[asset])
            for t in self.transactions[asset]:
                date = t[self.tx_mask['date']]
                t[self.tx_mask['date']] = self.format_german_date(date)
                t[self.tx_mask['input_amount']] = '\'  ' + t[self.tx_mask['input_amount']]
                t[self.tx_mask['output_amount']] = '\'  ' + t[self.tx_mask['output_amount']]
                t[self.tx_mask['fee']] = '\'  ' + t[self.tx_mask['fee']]
                t[self.tx_mask['acquisition_cost']] = '\'  ' + t[self.tx_mask['acquisition_cost']]
                t[self.tx_mask['selling_price']] = '\'  ' + t[self.tx_mask['selling_price']]
                t[self.tx_mask['capital_gain']] = '\'  ' + t[self.tx_mask['capital_gain']]
                t[self.tx_mask['tax_relevant_gain_loss']] = '\'  ' + t[self.tx_mask['tax_relevant_gain_loss']]
                self.output.append(t)
            self.output.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

    def build_header(self, crypto_exchange, account_name, crypto_shortcut, crypto_name, itin):
        self.output.append(
            ['Datenquelle', '', '', 'Account', '', ' ', '', '', ' ', '', '', '', 'Asset', '', '', '', ''])
        self.output.append(['', '', '', '', '', '', '', '', '', '', '', '', 'Ticker', 'Name', '', 'ITIN'])
        self.output.append(
            [crypto_exchange, '', '', account_name, '', '', '', '', '', '', '', '', crypto_shortcut, crypto_name, '',
             itin])
        self.output.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        self.output.append(
            ['ID', 'Datum (UTC)', 'Art', '', 'Eingang', '', '', 'Ausgang', '', '', 'Gebühr\nin EUR',
             'Anschaffungs-\nkosten\nin EUR',
             'Veräußerungs-\npreis\nin EUR', 'Veräußerungs-\ngewinn\nin EUR', 'Haltedauer\nin Tagen',
             'Steuerrelevanter\nKursgewinn-/verlust'])
        self.output.append(['', '', '', '', 'Anzahl', '', 'Asset', 'Anzahl', '', 'Asset', '', '', '', '', '', ''])

    def append_csv_line(self, transaction_id, date='', output_typ='', input_amount='', input_asset_name='',
                        output_amount='',
                        output_asset_name='',
                        fee='', acquisition_cost='', selling_price='', capital_gain='', holding_period='',
                        tax_relevant_gain_loss='', crypto_asset=''):
        transaction = [str(transaction_id), str(date), str(output_typ), '', str(input_amount), '',
                       str(input_asset_name),
                       str(output_amount), '', str(output_asset_name), str(fee), str(acquisition_cost),
                       str(selling_price),
                       str(capital_gain), str(holding_period), str(tax_relevant_gain_loss)]
        if str(crypto_asset) != '':
            try:
                specific_asset_list = list(self.transactions[str(crypto_asset)])
                specific_asset_list.append(transaction)
                self.transactions[str(crypto_asset)] = specific_asset_list
            except:
                self.transactions[str(crypto_asset)] = [transaction]
        return transaction

    @staticmethod
    def format_german_date(date):
        # german format
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        day = str(date.day)
        month = str(date.month)
        year = str(date.year)
        hour = str(date.hour)
        minute = str(date.minute)
        second = str(date.second)
        if len(day) == 1:
            day = '0' + day
        if len(month) == 1:
            month = '0' + month
        if len(hour) == 1:
            hour = '0' + hour
        if len(minute) == 1:
            minute = '0' + minute
        if len(second) == 1:
            second = '0' + second
        date = str(day + '.' + month + '.' + year + ' ' + hour + ':' + minute + ':' + second)
        return date

    def format_and_append_csv_line(self, transaction_id='', date='', output_typ='', input_amount='',
                                   input_asset_name='', output_amount='',
                                   output_asset_name='',
                                   fee=0.0, acquisition_cost=0.0, selling_price=0.0, capital_gain=0.0,
                                   holding_period='',
                                   tax_relevant_gain_loss=0.0, crypto_asset=''):
        if fee == 0:
            fee = ''
        else:
            fee = round(fee, 2)
        if acquisition_cost == 0:
            acquisition_cost = ''
        else:
            acquisition_cost = round(acquisition_cost, 2)
        if selling_price == 0:
            selling_price = ''
        else:
            selling_price = round(selling_price, 2)
        if capital_gain == 0 and not output_amount == '' and not selling_price == 0.0:
            capital_gain = ''
        else:
            capital_gain = round(capital_gain, 2)
        if tax_relevant_gain_loss == 0:
            tax_relevant_gain_loss = ''
        else:
            tax_relevant_gain_loss = round(tax_relevant_gain_loss, 2)

        if type(input_amount) is float:
            input_amount = '{0:.8f}'.format(float(input_amount))
        if type(output_amount) is float:
            output_amount = '{0:.8f}'.format(float(output_amount))
        input_amount = str(input_amount).replace('.', ',')
        output_amount = str(output_amount).replace('.', ',')
        if type(fee) is float:
            fee = '{0:.2f}'.format(float(fee))
        fee = str(fee).replace('.', ',')
        if type(acquisition_cost) is float:
            acquisition_cost = '{0:.2f}'.format(float(acquisition_cost))
        acquisition_cost = str(acquisition_cost).replace('.', ',')
        if type(selling_price) is float:
            selling_price = '{0:.2f}'.format(float(selling_price))
        selling_price = str(selling_price).replace('.', ',')
        if type(capital_gain) is float:
            capital_gain = '{0:.2f}'.format(float(capital_gain))
        capital_gain = str(capital_gain).replace('.', ',')
        if type(tax_relevant_gain_loss) is float:
            tax_relevant_gain_loss = '{0:.2f}'.format(float(tax_relevant_gain_loss))
        tax_relevant_gain_loss = str(tax_relevant_gain_loss).replace('.', ',')

        return self.append_csv_line(transaction_id, date, output_typ, input_amount, input_asset_name, output_amount,
                                    output_asset_name,
                                    fee, acquisition_cost, selling_price, capital_gain, holding_period,
                                    tax_relevant_gain_loss,
                                    crypto_asset)

    def save_purchase_row(self, transaction_id, date, output_typ, input_amount, input_asset_name, output_amount,
                          output_asset_name, fee,
                          acquisition_cost, crypto_asset):
        transaction = self.format_and_append_csv_line(transaction_id=transaction_id, date=date, output_typ=output_typ,
                                                      input_amount=input_amount, input_asset_name=input_asset_name,
                                                      output_amount=output_amount, output_asset_name=output_asset_name,
                                                      fee=fee,
                                                      acquisition_cost=acquisition_cost, crypto_asset=crypto_asset)
        self.enqueue(input_amount, transaction)

    def save_sell_row(self, transaction_id, date, output_typ, input_amount, input_asset_name, output_amount,
                      output_asset_name, selling_price, crypto_asset):
        transaction = self.format_and_append_csv_line(transaction_id=transaction_id, date=date, output_typ=output_typ,
                                                      input_amount=input_amount, input_asset_name=input_asset_name,
                                                      output_amount=output_amount, output_asset_name=output_asset_name,
                                                      selling_price=selling_price,
                                                      crypto_asset=crypto_asset)
        self.dequeue(output_amount, transaction)

    def save_deposit_row(self, transaction_id, date, output_typ, input_amount, input_asset_name,
                         acquisition_cost, crypto_asset):
        transaction = self.format_and_append_csv_line(transaction_id=transaction_id, date=date,
                                                      output_typ=output_typ,
                                                      input_amount=input_amount, input_asset_name=input_asset_name,
                                                      acquisition_cost=acquisition_cost, crypto_asset=crypto_asset)
        self.enqueue(input_amount, transaction)

    def save_withdrawal_or_fee_row(self, transaction_id, date, output_typ, output_amount, output_asset_name,
                                   selling_price, crypto_asset):
        transaction = self.format_and_append_csv_line(transaction_id=transaction_id, date=date,
                                                      output_typ=output_typ,
                                                      output_amount=output_amount,
                                                      output_asset_name=output_asset_name,
                                                      selling_price=selling_price,
                                                      crypto_asset=crypto_asset)
        self.dequeue(output_amount, transaction)

    def save_purchase_fifo_row(self, trade_date, output_typ, input_amount, input_asset_name,
                               output_amount,
                               output_asset_name, acquisition_cost, selling_price, capital_gain, holding_period,
                               crypto_asset):
        self.format_and_append_csv_line(date=trade_date, output_typ=output_typ,
                                        input_amount=input_amount, input_asset_name=input_asset_name,
                                        output_amount=output_amount, output_asset_name=output_asset_name,
                                        acquisition_cost=acquisition_cost, selling_price=selling_price,
                                        capital_gain=capital_gain, holding_period=holding_period,
                                        crypto_asset=crypto_asset)

    # purchase tx
    def enqueue(self, amount, buy_tx):
        self.queue.append((amount, buy_tx))

    def dequeue(self, amount, sell_tx):
        if not self.queue:
            return
        i = 0
        for tx in self.queue:
            if str(tx[1][self.tx_mask['input_asset_name']]) == str(sell_tx[self.tx_mask['output_asset_name']]):
                first_in_queue_by_crypto_asset = self.queue.pop(i)
                first_in_queue_amount = first_in_queue_by_crypto_asset[0]
                buy_tx = first_in_queue_by_crypto_asset[1]
                diff = first_in_queue_amount - amount
                if math.isclose(diff, 0.0, rel_tol=1e-08):
                    return
                if diff < 0:
                    self.selling(buy_tx, sell_tx, first_in_queue_amount)
                    self.dequeue(-1 * diff, sell_tx)
                    return
                elif diff > 0:
                    self.selling(buy_tx, sell_tx, amount)
                    self.queue.insert(0, (diff, buy_tx))
                    return
                return
            i += 1
        if (i + 1) == len(self.queue):
            print(str(sell_tx) + ' , could not be done because there are no funds')
            return

    def selling(self, buy_tx, sell_tx, amount):
        if str(buy_tx[self.tx_mask['output_amount']]) == '':
            self.selling_deposit(buy_tx, sell_tx, amount)
            return
        input_amount = float(str(buy_tx[self.tx_mask['input_amount']]).replace(',', '.'))
        output_amount_in_euro = float(str(buy_tx[self.tx_mask['acquisition_cost']]).replace(',', '.')) - float(
            str(buy_tx[self.tx_mask['fee']]).replace(',', '.'))
        buy_price = output_amount_in_euro / input_amount

        output_amount = buy_price * amount

        sell_price = float(str(sell_tx[self.tx_mask['selling_price']]).replace(',', '.')) / float(
            str(sell_tx[self.tx_mask['output_amount']]).replace(',', '.'))
        selling_price = sell_price * amount

        fee = float(str(buy_tx[self.tx_mask['fee']]).replace(',', '.'))
        acquisition_cost = (buy_price * amount) + fee
        capital_gain = selling_price - acquisition_cost
        output_amount = round(output_amount, 8)
        amount = round(amount, 8)
        holding_period = self.days_between(str(buy_tx[self.tx_mask['date']]), str(sell_tx[self.tx_mask['date']]))
        self.save_purchase_fifo_row(buy_tx[self.tx_mask['date']], 'vom Kauf (FIFO)',
                                    amount, buy_tx[self.tx_mask['input_asset_name']],
                                    output_amount, buy_tx[self.tx_mask['output_asset_name']],
                                    acquisition_cost, selling_price,
                                    capital_gain, holding_period, buy_tx[self.tx_mask['input_asset_name']])

    def selling_deposit(self, buy_tx, sell_tx, amount):
        sell_price = float(str(sell_tx[self.tx_mask['selling_price']]).replace(',', '.')) / float(
            str(sell_tx[self.tx_mask['output_amount']]).replace(',', '.'))
        selling_price = sell_price * amount
        acquisition_cost = selling_price
        capital_gain = selling_price - acquisition_cost
        amount = round(amount, 8)
        holding_period = self.days_between(str(buy_tx[self.tx_mask['date']]), str(sell_tx[self.tx_mask['date']]))
        self.save_purchase_fifo_row(buy_tx[self.tx_mask['date']], 'von Einzahlung (FIFO)',
                                    amount, buy_tx[self.tx_mask['input_asset_name']],
                                    '', buy_tx[self.tx_mask['output_asset_name']],
                                    acquisition_cost, selling_price,
                                    capital_gain, holding_period, buy_tx[self.tx_mask['input_asset_name']])

    @staticmethod
    def days_between(date1, date2):
        date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
        date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S')
        days_between = abs((date1 - date2).days)
        if days_between == -1 or days_between == 0:
            return str(0)
        else:
            return str(days_between - 1)
