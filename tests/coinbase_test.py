import pytest
from src.chainreport_parser.coinbase import CoinbaseParserCsv

class TestCoinbaseParserCsv:

    # Correctly parses date string from input row
    def test_correctly_parses_date_string(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '100.50',
            'Asset': 'BTC',
            'Subtotal': '99.99',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.51',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_date_string() == '01.01.2023 12:00'

    # Handles missing or malformed date in input row
    def test_handles_missing_or_malformed_date(self):
        row = {
            'Timestamp': 'malformed date',
            'Quantity Transacted': '100.50',
            'Asset': 'BTC',
            'Subtotal': '99.99',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.51',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        with pytest.raises(ValueError):
            # pylint: disable=unused-variable
            parser = CoinbaseParserCsv(row)

    # Correctly identifies unknown transaction type as ERROR
    def test_correctly_identifies_transaction_type_as_error(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '100.50',
            'Asset': 'BTC',
            'Subtotal': '99.99',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.51',
            'ID': '1234567890',
            'Transaction Type': 'WRONG'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Correctly identifies transaction type as Deposit
    def test_correctly_identifies_transaction_type_as_deposit(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '100.50',
            'Asset': 'BTC',
            'Subtotal': '99.99',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.51',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Deposit'

    # Correctly identifies transaction type as Withdrawal
    def test_correctly_identifies_transaction_type_as_withdrawal(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '100.50',
            'Asset': 'BTC',
            'Subtotal': '99.99',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.51',
            'ID': '1234567890',
            'Transaction Type': 'Send'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Withdrawal'

    # Correctly identifies transaction type as Trade
    def test_correctly_identifies_transaction_type_as_trade(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '100.50',
            'Asset': 'BTC',
            'Subtotal': '99.99',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.51',
            'ID': '1234567890',
            'Transaction Type': 'Buy'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Trade'

    # Correctly identifies transaction type as Other_Income
    def test_correctly_identifies_transaction_type_as_other_income(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '100.50',
            'Asset': 'BTC',
            'Subtotal': '99.99',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.51',
            'ID': '1234567890',
            'Transaction Type': 'Receive'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Other_Income'

    # Correctly identifies transaction type as Staking
    def test_correctly_identifies_transaction_type_as_staking(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '100.50',
            'Asset': 'BTC',
            'Subtotal': '99.99',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.51',
            'ID': '1234567890',
            'Transaction Type': 'Staking Income'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Staking'

    # Returns received amount for Trade transactions
    def test_returns_received_amount_for_trade_transactions(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '100.50',
            'Asset': 'BTC',
            'Subtotal': '99.99',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.51',
            'ID': '1234567890',
            'Transaction Type': 'Buy'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == "100,50"
        assert parser.get_sent_amount() == "-99,99"

    # Returns received currency for Trade transactions
    def test_returns_received_currency_for_trade_transactions(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '100.50',
            'Asset': 'BTC',
            'Subtotal': '99.99',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.51',
            'ID': '1234567890',
            'Transaction Type': 'Buy'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_currency() == "BTC"
        assert parser.get_sent_currency() == "USD"
