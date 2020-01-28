# Einzeltransaktionsaufstellung für den Handel mit Kryptowährungen (german tax trading single transaction lineup for crypto currencies) 
### kostenloses Python FIFO (first in first out) Tool für die Transaktionsaufzeichnung von Kryptoeinheiten 

##### WICHTIG: Bitte überprüfen Sie die Werte, der Autor übernimmt keine Haftung! 

#### Anleitung:
1.\
Go to https://min-api.cryptocompare.com/ and get your **free API key**. The program needs the price history of every crypto asset.

2.\
Create the file **secret.py** in the root of the project. Paste in this code with your private values. 


    account_name_kraken = 'your_secret_kraken_account_name'
    api_key = 'your_secret_api_key_of_cryptocompare'
    account_name_binance = 'your_secret_binance_account_name'


3.\
**Binance:**\
Go to https://www.binance.com/userCenter/tradeHistory.html and download the **trade** history of binance. 
Visit https://www.binance.com/de/usercenter/wallet/money-log/withdraw and https://www.binance.com/de/usercenter/wallet/money-log/deposit 
to download the **withdrawal** and **deposit** history.

structure of binance trades:

![Alt text](examples/binance_trades.png?raw=true "binance trades")

structure of binance withdrawal and deposit:

![Alt text](examples/binance_withdrawal_deposit.png?raw=true "binance withdrawals and deposits")

**Kraken (experimental, currently works only with deposit euro, withdrawal and buy with euro):**\
Go to https://www.kraken.com/u/history/export and select export type **Ledgers**!

structure of kraken ledgers:

![Alt text](examples/kraken_ledgers.png?raw=true "kraken ledgers")

4.\
Change **main.py** to your file locations and **run** the main.py (wait until finished, could be 60 seconds run time):


    path = '/path/to/your/exchanges/files'
    if __name__ == '__main__':
        kraken_csv_handler = KrakenCsvHandler(path=path, input_file='ledgers_kraken.csv',
                                              output_file='Einzeltransaktionsaufstellung_Kraken.csv',
                                              account_name=account_name_kraken)
        # uncomment if kraken exchange single transaction lineup for crypto currencies are needed
        # kraken_csv_handler.handle()
        binance_csv_handler = BinanceCsvHandler(path=path, withdrawal_file='withdrawals_binance.xlsx',
                                                deposit_file='deposits_binance.xlsx',
                                                trade_file='trades_binance.xlsx',
                                                account_name=account_name_binance,
                                                output_file='Einzeltransaktionsaufstellung_Binance.csv')
        # START reading xlsx files
        binance_csv_handler.handle()

5.\
If required extend crypto currencies in **csv_formatter.py :**

    shortcut_to_itin = {'BTC': 'TP3B-248N-Q', 'ETH': 'T22F-QJGB-N', 'XMR': 'HRYR-93E4-W', 'MIOTA': 'DB8C-YKTY-7',
                        'NEO': '9QVR-R258-P',
                        'XEM': '2PTC-P6K4-H', 'EOS': 'A8YZ-WTGR-6', 'NAS': 'RACF-AZ34-H', 'XLM': 'KTG9-BP94-H',
                        'BNB': 'MMRX-72FA-8', '': 'EMPTY'}
    shortcut_to_name = {'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'XMR': 'Monero', 'MIOTA': 'IOTA', 'NEO': 'Neo',
                        'XEM': 'NEM', 'EOS': 'EOS', 'NAS': 'Nebulas', 'XLM': 'Stellar', 'BNB': 'Binance Coin',
                        '': 'EMPTY'}


THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.