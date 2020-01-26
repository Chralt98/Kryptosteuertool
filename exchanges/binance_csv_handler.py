from Kryptosteuertool.csv_formatter import CsvFormatter
from Kryptosteuertool.api_call import get_price_of_currency
from pandas import read_excel


class BinanceCsvHandler(CsvFormatter):
    path = ''
    deposit_file = ''
    withdrawal_file = ''
    trade_file = ''
    account_name = ''
    tx_id = 1
    asset_name = ''
    market = ''
    coin = ''
    total = 0.0
    fee = 0.0
    fee_coin = ''
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
    exchange_name = 'Binance'
    api_exchange = 'CCCAGG'
    deposit_withdrawal_input_column_names = {'Date': 0, 'Coin': 1, 'Amount': 2, 'TransactionFee': 3, 'Address': 4,
                                             'TXID': 5, 'SourceAddress': 6, 'PaymentID': 7, 'Status': 8}
    trading_input_column_names = {'Date(UTC)': 0, 'Market': 1, 'Type': 2, 'Price': 3, 'Amount': 4,
                                  'Total': 5, 'Fee': 6, 'Fee Coin': 7}

    def __init__(self, path, withdrawal_file, deposit_file, trade_file, output_file, account_name):
        super().__init__(path, output_file, self.exchange_name, account_name)
        self.path = path
        self.withdrawal_file = withdrawal_file
        self.deposit_file = deposit_file
        self.trade_file = trade_file
        self.output_file = output_file
        self.account_name = account_name

    def handle(self):
        # find your sheet name at the bottom left of your excel file and assign
        # it to my_sheet
        my_sheet = 'sheet1'
        trades = list(read_excel(self.path + self.trade_file, sheet_name=my_sheet).values.tolist())
        [x.append('trade') for x in trades]
        deposits = list(read_excel(self.path + self.deposit_file, sheet_name=my_sheet).values.tolist())
        [x.append('deposit') for x in deposits]
        withdrawals = list(read_excel(self.path + self.withdrawal_file, sheet_name=my_sheet).values.tolist())
        [x.append('withdrawal') for x in withdrawals]
        transactions = (trades + deposits + withdrawals)
        transactions = sorted(transactions, key=lambda tx: tx[0])
        for row in transactions:
            self.read_raw_data(row)
        self.write_in_csv()

    def read_raw_data(self, row):
        if row[-1] == 'trade':
            self.market = str(row[self.trading_input_column_names['Market']])
            self.date = str(row[self.trading_input_column_names['Date(UTC)']])
            self.input_typ = str(row[self.trading_input_column_names['Type']])
            self.price = float(row[self.trading_input_column_names['Price']])
            self.amount = float(row[self.trading_input_column_names['Amount']])
            self.total = float(row[self.trading_input_column_names['Total']])
            self.fee = float(row[self.trading_input_column_names['Fee']])
            self.fee_coin = str(row[self.trading_input_column_names['Fee Coin']])
            self.choose_input_typ()
        else:
            self.date = str(row[self.deposit_withdrawal_input_column_names['Date']])
            self.coin = str(row[self.deposit_withdrawal_input_column_names['Coin']])
            self.amount = float(row[self.deposit_withdrawal_input_column_names['Amount']])
            self.fee = float(row[self.deposit_withdrawal_input_column_names['TransactionFee']])
            if str(self.coin) == 'IOTA':
                self.coin = 'MIOTA'
        if row[-1] == 'deposit':
            self.deposit()
        elif row[-1] == 'withdrawal':
            self.withdrawal()

    def choose_input_typ(self):
        for asset in self.shortcut_to_name:
            if str(self.market)[:3] in str(asset) or str(self.market)[:4] in str(asset):
                self.input_asset_name = asset
                if str(asset) == 'IOTA':
                    self.input_asset_name = 'MIOTA'
            if str(self.market)[3:] in str(asset) or str(self.market)[4:] in str(asset):
                self.output_asset_name = asset
                if str(asset) == 'IOTA':
                    self.output_asset_name = 'MIOTA'
        if str(self.fee_coin) == 'IOTA':
            self.fee_coin = 'MIOTA'

        if self.input_typ == 'BUY':
            self.buy()
        elif self.input_typ == 'SELL':
            self.sell()
        else:
            print('input type: ' + str(self.input_typ) + ' does not exist')

    def buy(self):
        output_typ = 'Kauf'
        self.input_amount = self.amount
        fee_coin_asset_price = get_price_of_currency(self.date, self.fee_coin, 'EUR', self.api_exchange)
        self.output_amount = self.total
        self.trading_fee = fee_coin_asset_price * self.fee
        input_asset_euro = get_price_of_currency(self.date, self.input_asset_name, 'EUR', self.api_exchange)
        acquisition_cost = (input_asset_euro * self.input_amount) + self.trading_fee
        crypto_asset = self.input_asset_name
        self.save_purchase_row(transaction_id=self.tx_id, date=self.date, output_typ=output_typ,
                               input_amount=self.input_amount,
                               input_asset_name=self.input_asset_name,
                               output_amount=self.output_amount,
                               output_asset_name=self.output_asset_name,
                               fee=self.trading_fee, acquisition_cost=acquisition_cost, crypto_asset=crypto_asset)
        self.tx_id += 1

        output_typ = 'Gebühr'
        selling_price = self.trading_fee
        self.save_withdrawal_or_fee_row(self.tx_id, self.date, output_typ, self.fee,
                                        self.fee_coin,
                                        selling_price, self.input_asset_name)
        self.tx_id += 1

        output_typ = 'Verkauf'
        self.input_amount = self.amount
        self.output_amount = self.total
        selling_price = get_price_of_currency(self.date, self.output_asset_name, 'EUR',
                                              self.api_exchange) * self.output_amount
        crypto_asset = self.output_asset_name
        self.save_sell_row(transaction_id=self.tx_id, date=self.date, output_typ=output_typ,
                           input_amount=self.input_amount, input_asset_name=self.input_asset_name,
                           output_amount=self.output_amount, output_asset_name=self.output_asset_name,
                           selling_price=selling_price, crypto_asset=crypto_asset)
        self.tx_id += 1

    def sell(self):
        output_typ = 'Verkauf'
        self.input_amount = self.total
        self.output_amount = self.amount
        selling_price = get_price_of_currency(self.date, self.output_asset_name, 'EUR',
                                              self.api_exchange) * self.input_amount
        crypto_asset = self.input_asset_name
        self.save_sell_row(transaction_id=self.tx_id, date=self.date, output_typ=output_typ,
                           input_amount=self.input_amount, input_asset_name=self.output_asset_name,
                           output_amount=self.output_amount, output_asset_name=self.input_asset_name,
                           selling_price=selling_price, crypto_asset=crypto_asset)
        self.tx_id += 1

        output_typ = 'Kauf'
        self.input_amount = self.total
        fee_coin_asset_price = get_price_of_currency(self.date, self.fee_coin, 'EUR', self.api_exchange)
        self.output_amount = self.amount
        self.trading_fee = fee_coin_asset_price * self.fee
        output_asset_euro = get_price_of_currency(self.date, self.output_asset_name, 'EUR', self.api_exchange)
        acquisition_cost = (output_asset_euro * self.input_amount) + self.trading_fee
        crypto_asset = self.output_asset_name
        self.save_purchase_row(transaction_id=self.tx_id, date=self.date, output_typ=output_typ,
                               input_amount=self.input_amount,
                               input_asset_name=self.output_asset_name,
                               output_amount=self.output_amount,
                               output_asset_name=self.input_asset_name,
                               fee=self.trading_fee, acquisition_cost=acquisition_cost, crypto_asset=crypto_asset)
        self.tx_id += 1

        output_typ = 'Gebühr'
        output_amount = self.fee
        output_asset_name = self.fee_coin
        selling_price = self.trading_fee
        self.save_withdrawal_or_fee_row(self.tx_id, self.date, output_typ, output_amount,
                                        output_asset_name,
                                        selling_price, output_asset_name)
        self.tx_id += 1

    def withdrawal(self):
        output_typ = 'Auszahlung'
        output_amount = self.amount
        output_asset_name = self.coin
        selling_price = get_price_of_currency(self.date, output_asset_name, 'EUR', self.api_exchange) * output_amount
        self.save_withdrawal_or_fee_row(self.tx_id, self.date, output_typ, output_amount,
                                        output_asset_name,
                                        selling_price, output_asset_name)
        self.tx_id += 1

    def deposit(self):
        output_typ = 'Einzahlung'
        input_amount = self.amount
        input_asset_name = self.coin
        price = get_price_of_currency(self.date, input_asset_name, 'EUR', self.api_exchange)
        acquisition_cost = (price * input_amount) + self.fee
        self.save_deposit_row(self.tx_id, self.date, output_typ, input_amount,
                              input_asset_name,
                              acquisition_cost, input_asset_name)
        self.tx_id += 1
