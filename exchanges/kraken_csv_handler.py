import csv
from Kryptosteuertool.csv_formatter import CsvFormatter
from Kryptosteuertool.api_call import get_price_of_currency


class KrakenCsvHandler(CsvFormatter):
    path = ''
    input_file = ''
    output_file = ''
    account_name = ''
    tx_id = 1
    asset_name = ''
    date = ''
    input_typ = ''
    amount = 0.0
    price = 0.0
    trade_counter = 0
    input_amount = 0.0
    input_asset_name = ''
    output_amount = 0.0
    output_asset_name = ''
    trading_fee = 0.0
    exchange_name = 'Kraken'
    input_column_names = {'txid': 0, 'refid': 1, 'time': 2, 'type': 3, 'aclass': 4,
                          'asset': 5, 'amount': 6, 'fee': 7, 'balance': 8}

    def __init__(self, path, input_file, output_file, account_name):
        super().__init__(path, output_file, self.exchange_name, account_name)
        self.path = path
        self.input_file = input_file
        self.output_file = output_file

    def handle(self):
        first = True
        with open(self.path + self.input_file, 'r', encoding='UTF-8') as file:
            reader = csv.reader(file, delimiter=',', quotechar='\"')
            for row in reader:
                # skip first header line
                if first is True:
                    first = False
                    continue
                self.read_raw_data(row)
                self.choose_input_typ(row)
        self.write_in_csv()

    def read_raw_data(self, row):
        self.asset_name = str(row[self.input_column_names['asset']])[1:]
        if self.asset_name == 'XBT':
            self.asset_name = 'BTC'
        self.date = str(row[self.input_column_names['time']])
        self.input_typ = row[self.input_column_names['type']]
        self.amount = float(row[self.input_column_names['amount']])
        self.price = float(get_price_of_currency(self.date, self.asset_name, 'EUR', self.exchange_name))

    def choose_input_typ(self, row):
        if self.input_typ == 'trade':
            self.trade(row)
        elif self.asset_name != 'EUR':
            if self.input_typ == 'withdrawal':
                self.withdrawal(row)
                self.pay_fee(row)
            elif self.input_typ == 'deposit':
                self.deposit(row)

    def trade(self, row):
        self.trade_counter += 1
        output_typ = 'Kauf'
        if self.amount > 0:
            self.input_amount = self.amount
            self.input_asset_name = self.asset_name
        elif self.amount < 0:
            self.output_amount = self.amount * -1
            self.output_asset_name = self.asset_name
            self.trading_fee = float(row[self.input_column_names['fee']])
        else:
            print('Amount is zero! ' + str(row))
        acquisition_cost = self.output_amount + self.trading_fee
        if self.trade_counter is 2:
            self.save_purchase_row(self.tx_id, self.date, output_typ, self.input_amount,
                                   self.input_asset_name,
                                   self.output_amount,
                                   self.output_asset_name,
                                   self.trading_fee, acquisition_cost, self.input_asset_name)
            self.tx_id += 1
            self.trade_counter = 0

    def withdrawal(self, row):
        if str(row[self.input_column_names['txid']]) == '' and str(
                row[self.input_column_names['balance']]) == '':
            output_asset_name = self.asset_name

            output_typ = 'Auszahlung'
            output_amount = self.amount * -1
            selling_price = self.price * output_amount
            self.save_withdrawal_or_fee_row(self.tx_id, self.date, output_typ, output_amount,
                                            output_asset_name,
                                            selling_price, output_asset_name)
            self.tx_id += 1

    def pay_fee(self, row):
        if str(row[self.input_column_names['txid']]) == '' and str(
                row[self.input_column_names['balance']]) == '':
            output_typ = 'Gebühr'
            output_amount = float(row[self.input_column_names['fee']])
            selling_price = self.price * output_amount
            output_asset_name = self.asset_name
            self.save_withdrawal_or_fee_row(self.tx_id, self.date, output_typ, output_amount,
                                            output_asset_name,
                                            selling_price, output_asset_name)
            self.tx_id += 1

    def deposit(self, row):
        if str(row[self.input_column_names['txid']]) == '' and str(
                row[self.input_column_names['balance']]) == '':
            input_asset_name = self.asset_name

            output_typ = 'Einzahlung'
            input_amount = float(row[self.input_column_names['amount']])
            acquisition_cost = self.price * input_amount
            self.save_deposit_row(self.tx_id, self.date, output_typ, input_amount,
                                  input_asset_name,
                                  acquisition_cost, input_asset_name)
            self.tx_id += 1
