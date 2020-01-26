from exchanges.kraken_csv_handler import KrakenCsvHandler
from exchanges.binance_csv_handler import BinanceCsvHandler
from Kryptosteuertool.secret import account_name_binance, account_name_kraken

path = '/home/chralt/Krypto/'
if __name__ == '__main__':
    kraken_csv_handler = KrakenCsvHandler(path=path, input_file='Ledgers_2019_Kraken.csv',
                                          output_file='Einzeltransaktionsaufstellung_Kraken.csv',
                                          account_name=account_name_kraken)
    # kraken_csv_handler.handle()
    binance_csv_handler = BinanceCsvHandler(path=path, withdrawal_file='WithdrawalHistory_2019_binance.xlsx',
                                            deposit_file='DepositHistory_2019_binance.xlsx',
                                            trade_file='Handelsgeschichte_2019_Binance.xlsx',
                                            account_name=account_name_binance,
                                            output_file='Einzeltransaktionsaufstellung_Binance.csv')
    binance_csv_handler.handle()
exit()
