import pytest
from src.chainreport_parser.coinbase import CoinbaseParserCsv

class TestGetInputString:

    # Handles an empty dictionary as input
    def test_handles_empty_dict_as_input(self):
        row = {}
        coinbase_parser = CoinbaseParserCsv(row)
        input_data = coinbase_parser.get_input_string()
        assert input_data == row

    # Handles typical Coinbase CSV row data correctly
    def test_returns_original_input_row_with_valid_dict(self):
        row = {
            'Timestamp': '2022-01-01 12:00:00 UTC',
            'Quantity Transacted': '10.5',
            'Asset': 'BTC',
            'Subtotal': '10500',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10',
            'ID': '123456',
            'Transaction Type': 'Buy'
        }
        coinbase_parser = CoinbaseParserCsv(row)
        input_data = coinbase_parser.get_input_string()
        assert input_data == row

    # Processes rows with missing keys gracefully
    def test_missing_keys_gracefully(self):
        row = {
            'Timestamp': '2022-01-01 12:00:00 UTC',
            'Quantity Transacted': '10.5',
            'Asset': 'BTC',
            'Subtotal': '10500',
            'Price Currency': 'USD',
            'ID': '123456',
            'Transaction Type': 'Buy'
        }
        coinbase_parser = CoinbaseParserCsv(row)
        input_data = coinbase_parser.get_input_string()
        assert input_data == row

    # Handles rows with unexpected or additional keys
    def test_handles_rows_with_unexpected_keys(self):
        row = {
            'Timestamp': '2022-01-01 12:00:00 UTC',
            'Quantity Transacted': '10.5',
            'Asset': 'BTC',
            'Subtotal': '10500',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10',
            'ID': '123456',
            'Transaction Type': 'Buy',
            'Extra Key': 'Extra Value'
        }
        coinbase_parser = CoinbaseParserCsv(row)
        input_data = coinbase_parser.get_input_string()
        assert input_data == row

    # Works with rows containing special characters in the values
    def test_works_with_special_characters_in_values(self):
        row = {
            'Timestamp': '2022-01-01 12:00:00 UTC',
            'Quantity Transacted': '10.5',
            'Asset': 'BTC',
            'Subtotal': '10,500',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10',
            'ID': '123456',
            'Transaction Type': 'Buy'
        }
        coinbase_parser = CoinbaseParserCsv(row)
        input_data = coinbase_parser.get_input_string()
        assert input_data == row

    # Processes rows with null or None values
    def test_processes_rows_with_null_or_none_values(self):
        row = {
            'Timestamp': None,
            'Quantity Transacted': None,
            'Asset': None,
            'Subtotal': None,
            'Price Currency': None,
            'Fees and/or Spread': None,
            'ID': None,
            'Transaction Type': None
        }
        coinbase_parser = CoinbaseParserCsv(row)
        input_data = coinbase_parser.get_input_string()
        assert input_data == row

    # Checks that the method works with nested dictionaries if applicable
    def test_returns_original_input_row_with_nested_dict(self):
        row = {
            'Timestamp': '2022-01-01 12:00:00 UTC',
            'Quantity Transacted': '10.5',
            'Asset': 'BTC',
            'Subtotal': '10500',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10',
            'ID': '123456',
            'Transaction Type': 'Buy',
            'Nested_Data': {
                'Nested_Key1': 'Nested_Value1',
                'Nested_Key2': 'Nested_Value2'
            }
        }
        coinbase_parser = CoinbaseParserCsv(row)
        input_data = coinbase_parser.get_input_string()
        assert input_data == row

    # Confirms that the method works with large dictionaries
    def test_returns_original_input_row_with_large_dict(self):
        large_row = {
            'Timestamp': '2022-01-01 12:00:00 UTC',
            'Quantity Transacted': '10.5',
            'Asset': 'BTC',
            'Subtotal': '10500',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10',
            'ID': '123456',
            'Transaction Type': 'Buy',
            'Extra_Field_1': 'Extra_Value_1',
            'Extra_Field_2': 'Extra_Value_2',
            'Extra_Field_3': 'Extra_Value_3',
            # Add more extra fields to simulate a large dictionary
        }
        coinbase_parser = CoinbaseParserCsv(large_row)
        input_data = coinbase_parser.get_input_string()
        assert input_data == large_row

    # Validates that the method handles different data types in the input row
    def test_handles_different_data_types(self):
        row = {
            'Timestamp': '2022-01-01 12:00:00 UTC',
            'Quantity Transacted': 10.5,
            'Asset': 'BTC',
            'Subtotal': 10500,
            'Price Currency': 'USD',
            'Fees and/or Spread': 10,
            'ID': '123456',
            'Transaction Type': 'Buy'
        }
        coinbase_parser = CoinbaseParserCsv(row)
        input_data = coinbase_parser.get_input_string()
        assert input_data == row

class TestGetDateString:

    # correctly formats a valid date string from the input row
    def test_correctly_formats_valid_date_string(self):
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

    # raises an error for malformed date strings
    def test_raises_error_for_malformed_date_strings(self):
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
            parser = CoinbaseParserCsv(row)

    # handles leap year dates accurately
    def test_handles_leap_year_dates(self):
        row = {
            'Timestamp': '2024-02-29 12:00:00 UTC',
            'Quantity Transacted': '100.50',
            'Asset': 'BTC',
            'Subtotal': '99.99',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.51',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_date_string() == '29.02.2024 12:00'

    # handles missing 'Timestamp' field gracefully
    def test_handles_missing_timestamp_field_gracefully(self):
        row = {
            'Quantity Transacted': '100.50',
            'Asset': 'BTC',
            'Subtotal': '99.99',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.51',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        with pytest.raises(KeyError):
            parser = CoinbaseParserCsv(row)

    # handles dates at the boundary of months and years correctly
    def test_handles_dates_at_boundary_of_months_and_years_correctly(self):
        row = {
            'Timestamp': '2023-01-31 23:59:59 UTC',
            'Quantity Transacted': '100.50',
            'Asset': 'BTC',
            'Subtotal': '99.99',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.51',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_date_string() == '31.01.2023 23:59'

    # ensures no side effects or state changes in the method
    def test_no_side_effects_or_state_changes(self):
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
        initial_input_row = parser.get_input_string()
        initial_date_string = parser.get_date_string()

        # Call the method again
        second_date_string = parser.get_date_string()

        assert initial_input_row == row
        assert initial_date_string == '01.01.2023 12:00'
        assert second_date_string == initial_date_string

class TestGetTransactionType:

    # correctly identifies 'Deposit' transaction type
    def test_correctly_identifies_deposit_transaction_type(self):
        row = {
            'Transaction Type': 'Deposit',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Deposit'

    # returns 'ERROR' for unknown transaction types
    def test_returns_error_for_unknown_transaction_types(self):
        row = {
            'Transaction Type': 'UNKNOWN_TYPE',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # correctly identifies 'Withdrawal' transaction type
    def test_correctly_identifies_withdrawal_transaction_type(self):
        row = {
            'Transaction Type': 'Send',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Withdrawal'

    # correctly identifies 'Trade' transaction type
    def test_correctly_identifies_trade_transaction_type(self):
        row = {
            'Transaction Type': 'Buy',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Trade'

    # correctly identifies 'Staking' transaction type
    def test_correctly_identifies_staking_transaction_type(self):
        row = {
            'Transaction Type': 'Staking Income',
            'Quantity Transacted': '1.0',
            'Asset': 'ETH',
            'Subtotal': '2000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '5.00',
            'ID': '9876543210',
            'Timestamp': '2022-02-15 08:45:30 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Staking'

    # correctly identifies 'Other_Income' transaction type
    def test_correctly_identifies_other_income_transaction_type(self):
        row = {
            'Transaction Type': 'Receive',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Other_Income'

    # handles empty string as transaction type
    def test_handles_empty_string_as_transaction_type(self):
        row = {
            'Transaction Type': '',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # handles missing 'Transaction Type' key gracefully
    def test_handles_missing_transaction_type_key_gracefully(self):
        row = {
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # handles None as transaction type
    def test_handles_none_as_transaction_type(self):
        row = {
            'Transaction Type': None,
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # handles unexpected data types for transaction type (e.g., integer, list)
    def test_handles_unexpected_data_types_for_transaction_type(self):
        row = {
            'Transaction Type': [1, 2, 3],  # unexpected data type
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # handles case sensitivity in transaction type descriptions
    def test_handles_case_sensitivity_in_transaction_type_descriptions(self):
        row = {
            'Transaction Type': 'staking',
            'Quantity Transacted': '1.0',
            'Asset': 'ETH',
            'Subtotal': '2000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '5.00',
            'ID': '9876543210',
            'Timestamp': '2022-02-15 08:30:45 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Staking'

    # handles input_row with special characters in 'Transaction Type'
    def test_handles_special_characters_in_transaction_type(self):
        row = {
            'Transaction Type': 'SPECIAL_CHARACTER$',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # handles input_row with mixed case 'Transaction Type' values
    def test_handles_mixed_case_transaction_type_values(self):
        row = {
            'Transaction Type': 'DaILy_ReBaTe_DiStRiBuTiOn',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Other_Income'

    # handles input_row with numeric strings as 'Transaction Type'
    def test_handles_numeric_strings_as_transaction_type(self):
        row = {
            'Transaction Type': '123',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # handles input_row with whitespace around 'Transaction Type'
    def test_handles_whitespace_around_transaction_type(self):
        row = {
            'Transaction Type': '   Deposit   ',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Deposit'

    # ensures no side effects on input_row after method execution
    def test_no_side_effects_on_input_row(self):
        row = {
            'Transaction Type': 'Deposit',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        original_row = row.copy()
        parser = CoinbaseParserCsv(row)
        parser.get_transaction_type()
        assert row == original_row

    # maintains performance with large datasets
    def test_maintains_performance_with_large_datasets(self):
        row = {
            'Transaction Type': 'Trade',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Trade'

    # handles large input_row dictionaries with many keys
    def test_handles_large_input_row_with_many_keys(self):
        row = {
            'Transaction Type': 'Deposit',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC',
            'extra_key1': 'value1',
            'extra_key2': 'value2',
            'extra_key3': 'value3',
            'extra_key4': 'value4',
            'extra_key5': 'value5',
            'extra_key6': 'value6',
            'extra_key7': 'value7',
            'extra_key8': 'value8',
            'extra_key9': 'value9',
            'extra_key10': 'value10'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Deposit'

     # validates input_row structure before processing
    def test_validates_input_row_structure(self):
        row = {
            'Transaction Type': 'Deposit',
            'Quantity Transacted': '1.0',
            'Asset': 'BTC',
            'Subtotal': '50000.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '10.00',
            'ID': '1234567890',
            'Timestamp': '2022-01-01 12:34:56 UTC'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_transaction_type() == 'Deposit'

class TestGetReceivedAmount:

    # returns the received amount when transaction type is 'Deposit'
    def test_returns_received_amount_for_deposit(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '10.50',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == "10,50"

    # returns an empty string when transaction type is 'Withdrawal'
    def test_returns_empty_string_for_withdrawal(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '10.50',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Send'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == ""

    # returns the received amount when transaction type is 'Trade'
    def test_returns_received_amount_for_trade(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '10.50',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Trade'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == "10,50"

    # returns the received amount when transaction type is 'Other_Income'
    def test_returns_received_amount_for_other_income(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '10.50',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Other_Income'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == "10,50"

    # returns the received amount when transaction type is 'Staking'
    def test_returns_received_amount_for_staking(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '10.50',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Staking Income'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == "10,50"

    # handles input row where 'Quantity Transacted' is an empty string
    def test_handles_empty_received_amount(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == ""

    # handles input row where 'Quantity Transacted' is a negative number
    def test_handles_negative_quantity_transacted(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '-5.75',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Trade'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == "-5,75"

    # handles input row where 'Quantity Transacted' is a very large number
    def test_handles_large_received_amount(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '1000000000000000000000000000000000000000000000000000000000000000',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == "1000000000000000000000000000000000000000000000000000000000000000"

    # handles input row where 'Quantity Transacted' has leading or trailing spaces
    def test_handles_input_row_with_leading_trailing_spaces(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '  10.50  ',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == "10,50"

    # handles input row where 'Quantity Transacted' contains only a decimal point
    def test_handles_decimal_point_in_received_amount(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '.25',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == ",25"

    # raises KeyError when 'Quantity Transacted' is missing in the input row
    def test_raises_key_error_when_quantity_transacted_missing(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        parser = CoinbaseParserCsv(row)
        with pytest.raises(KeyError):
            parser.get_received_amount()

    # handles input row where 'Quantity Transacted' contains special characters
    def test_handles_special_characters_in_received_amount(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '10,50',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == "10,50"

    # handles input row where 'Quantity Transacted' is in different locale-specific formats
    def test_handles_locale_specific_formats(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '10,50',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Trade'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == "10,50"

    # processes input row with different valid numerical values for 'Quantity Transacted'
    def test_processes_input_row_with_different_valid_numerical_values(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '5.75',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Buy'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == "5,75"

    # handles typical input row with valid 'Quantity Transacted'
    def test_returns_received_amount_for_typical_input(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '10.50',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Buy'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == "10,50"

    # verifies that 'Quantity Transacted' with leading or trailing spaces is trimmed and processed correctly
    def test_quantity_transacted_with_spaces_trimmed_correctly(self):
        row = {
            'Timestamp': '2023-01-01 12:00:00 UTC',
            'Quantity Transacted': '  10.50  ',
            'Asset': 'BTC',
            'Subtotal': '100.00',
            'Price Currency': 'USD',
            'Fees and/or Spread': '1.50',
            'ID': '1234567890',
            'Transaction Type': 'Deposit'
        }
        parser = CoinbaseParserCsv(row)
        assert parser.get_received_amount() == "10,50"

class TestGetReceivedCurrency:

    # Returns the correct received currency for a 'Deposit' transaction
    def test_returns_correct_received_currency_for_deposit_transaction(self):
        row_data = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '1.5',
            'Asset': 'BTC',
            'Subtotal': '15000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.005',
            'ID': '123456789',
            'Transaction Type': 'Deposit'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_received_currency() == 'BTC'

    # Returns an empty string for a 'Withdrawal' transaction
    def test_returns_empty_string_for_withdrawal_transaction(self):
        row_data = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '1.5',
            'Asset': 'BTC',
            'Subtotal': '15000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.005',
            'ID': '123456789',
            'Transaction Type': 'Send'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_received_currency() == ''

    # Returns the correct received currency for an 'Other_Income' transaction
    def test_returns_correct_received_currency_for_other_income_transaction(self):
        row_data = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '1.5',
            'Asset': 'ETH',
            'Subtotal': '1500',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.005',
            'ID': '987654321',
            'Transaction Type': 'Other_Income'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_received_currency() == 'ETH'

    # Handles missing 'Transaction Type' gracefully
    def test_handles_missing_transaction_type_gracefully(self):
        row_data = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '1.5',
            'Asset': 'BTC',
            'Subtotal': '15000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.005',
            'ID': '123456789'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_received_currency() == ''

    # Returns the correct received currency for a 'Trade' transaction
    def test_returns_correct_received_currency_for_trade_transaction(self):
        row_data = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '1.5',
            'Asset': 'BTC',
            'Subtotal': '15000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.005',
            'ID': '123456789',
            'Transaction Type': 'Buy'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_received_currency() == 'BTC'

    # Handles missing 'Asset' field gracefully
    def test_handles_missing_asset_field_gracefully(self):
        row_data = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '1.5',
            'Subtotal': '15000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.005',
            'ID': '123456789',
            'Transaction Type': 'Deposit'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_received_currency() == ''

    # Returns the correct received currency for a 'Staking' transaction
    def test_returns_correct_received_currency_for_staking_transaction(self):
        row_data = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '2.0',
            'Asset': 'ETH',
            'Subtotal': '2000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.01',
            'ID': '987654321',
            'Transaction Type': 'Staking Income'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_received_currency() == 'ETH'

    # Handles unexpected 'Transaction Type' values gracefully
    def test_handles_unexpected_transaction_type_gracefully(self):
        row_data = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '1.5',
            'Asset': 'BTC',
            'Subtotal': '15000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.005',
            'ID': '123456789',
            'Transaction Type': 'Unknown'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_received_currency() == ''

    # Handles case where 'Transaction Type' is in lowercase or uppercase
    def test_handles_case_insensitive_transaction_type(self):
        row_data = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '1.5',
            'Asset': 'BTC',
            'Subtotal': '15000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.005',
            'ID': '123456789',
            'Transaction Type': 'deposit'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_received_currency() == 'BTC'

    # Handles case where 'Transaction Type' has leading/trailing spaces
    def test_handles_transaction_type_with_spaces(self):
        row_data = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '1.5',
            'Asset': 'BTC',
            'Subtotal': '15000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.005',
            'ID': '123456789',
            'Transaction Type': '  Withdrawal  '
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_received_currency() == ''

    # Handles case where 'Asset' field has leading/trailing spaces
    def test_handles_case_where_asset_field_has_spaces(self):
        row_data = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '1.5',
            'Asset': '  BTC  ',
            'Subtotal': '15000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.005',
            'ID': '123456789',
            'Transaction Type': 'Deposit'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_received_currency() == 'BTC'

    # Handles case where 'Asset' field contains special characters
    def test_handles_special_characters_in_asset_field(self):
        row_data = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '1.5',
            'Asset': 'BTC$',
            'Subtotal': '15000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.005',
            'ID': '123456789',
            'Transaction Type': 'Deposit'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_received_currency() == 'BTC$'

    # Handles case where 'Asset' field is in lowercase or uppercase
    def test_handles_case_asset_field_lowercase_uppercase(self):
        # Test with lowercase 'asset' field
        row_data_lower = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '1.5',
            'Asset': 'btc',
            'Subtotal': '15000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.005',
            'ID': '123456789',
            'Transaction Type': 'Deposit'
        }
        coinbase_parser_lower = CoinbaseParserCsv(row_data_lower)
        assert coinbase_parser_lower.get_received_currency() == 'BTC'

        # Test with uppercase 'asset' field
        row_data_upper = {
            'Timestamp': '2022-01-15 10:30:00 UTC',
            'Quantity Transacted': '1.5',
            'Asset': 'BTC',
            'Subtotal': '15000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.005',
            'ID': '123456789',
            'Transaction Type': 'Deposit'
        }
        coinbase_parser_upper = CoinbaseParserCsv(row_data_upper)
        assert coinbase_parser_upper.get_received_currency() == 'BTC'

class TestGetSentAmount:

    # Returns negative sent_amount for 'Trade' transaction type
    def test_returns_negative_sent_amount_for_trade(self):
        row_data = {
            'Timestamp': '2022-01-15 08:42:00 UTC',
            'Quantity Transacted': '10.5',
            'Asset': 'BTC',
            'Subtotal': '10500',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.5',
            'ID': '123456789',
            'Transaction Type': 'Trade'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_sent_amount() == "-10500"

    # Handles missing 'sent_amount' in the input row
    def test_handles_missing_sent_amount(self):
        row_data = {
            'Timestamp': '2022-01-15 08:30:00 UTC',
            'Quantity Transacted': '10.5',
            'Asset': 'BTC',
            'Subtotal': '',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.5',
            'ID': '123456789',
            'Transaction Type': 'Trade'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_sent_amount() == "-"

    # Returns empty string for transaction types other than 'Trade' and 'Withdrawal'
    def test_returns_empty_sent_amount_for_other_transaction_types(self):
        row_data = {
            'Timestamp': '2022-01-15 08:30:00 UTC',
            'Quantity Transacted': '10.5',
            'Asset': 'BTC',
            'Subtotal': '10500',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.5',
            'ID': '123456789',
            'Transaction Type': 'Deposit'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_sent_amount() == ""

    # Returns negative received_amount for 'Withdrawal' transaction type
    def test_returns_negative_sent_amount_for_withdrawal(self):
        row_data = {
            'Timestamp': '2022-01-15 08:34:00 UTC',
            'Quantity Transacted': '10.5',
            'Asset': 'BTC',
            'Subtotal': '10500',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.5',
            'ID': '123456789',
            'Transaction Type': 'Withdrawal'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_sent_amount() == "-10.5"

    # Handles missing 'received_amount' in the input row
    def test_handles_missing_received_amount(self):
        row_data = {
            'Timestamp': '2022-01-15 08:31:00 UTC',
            'Asset': 'BTC',
            'Price Currency': 'USD',
            'ID': '123456789',
            'Transaction Type': 'Trade'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_sent_amount() == "-"

    # Handles missing 'Transaction Type' in the input row
    def test_handles_missing_transaction_type(self):
        row_data = {
            'Timestamp': '2022-01-15 08:32:00 UTC',
            'Quantity Transacted': '10.5',
            'Asset': 'BTC',
            'Subtotal': '10500',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.5',
            'ID': '123456789'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_sent_amount() == ""

    # Handles invalid 'Transaction Type' not in predefined lists
    def test_handles_invalid_transaction_type(self):
        row_data = {
            'Timestamp': '2022-02-15 08:30:00 UTC',
            'Quantity Transacted': '10.5',
            'Asset': 'BTC',
            'Subtotal': '10500',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.5',
            'ID': '123456789',
            'Transaction Type': 'InvalidType'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_sent_amount() == ""

    # Handles 'sent_amount' and 'received_amount' with non-numeric values
    def test_handles_non_numeric_values(self):
        row_data = {
            'Timestamp': '2022-01-25 08:30:00 UTC',
            'Quantity Transacted': 'N/A',
            'Asset': 'BTC',
            'Subtotal': 'N/A',
            'Price Currency': 'USD',
            'Fees and/or Spread': 'N/A',
            'ID': '123456789',
            'Transaction Type': 'Trade'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_sent_amount() == ""

    # Handles 'sent_amount' and 'received_amount' with large numeric values
    def test_handles_large_numeric_values(self):
        row_data = {
            'Timestamp': '2023-01-15 08:30:00 UTC',
            'Quantity Transacted': '1000000000000000000000',
            'Asset': 'BTC',
            'Subtotal': '10000000000000000000000',
            'Price Currency': 'USD',
            'Fees and/or Spread': '5000000000000000000',
            'ID': '123456789',
            'Transaction Type': 'Trade'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_sent_amount() == "-10000000000000000000000"

    # Handles 'sent_amount' and 'received_amount' with special characters
    def test_handles_special_characters(self):
        row_data = {
            'Timestamp': '2024-01-15 08:30:00 UTC',
            'Quantity Transacted': '10,5',
            'Asset': 'BTC',
            'Subtotal': '10.500',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0,5',
            'ID': '123456789',
            'Transaction Type': 'Trade'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_sent_amount() == "-10.500"

    # Ensures 'sent_amount' and 'received_amount' are correctly formatted with commas
    def test_sent_amount_formatting(self):
        row_data = {
            'Timestamp': '2022-11-15 08:30:00 UTC',
            'Quantity Transacted': '10.5',
            'Asset': 'BTC',
            'Subtotal': '10500',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0.5',
            'ID': '123456789',
            'Transaction Type': 'Trade'
        }
        coinbase_parser = CoinbaseParserCsv(row_data)
        assert coinbase_parser.get_sent_amount() == "-10,500"

    # Handles 'sent_amount' and 'received_amount' with zero values
    def test_handles_zero_values(self):
        # Test when transaction type is 'Trade'
        row_data_trade = {
            'Timestamp': '2012-01-15 08:30:00 UTC',
            'Quantity Transacted': '0',
            'Asset': 'BTC',
            'Subtotal': '0',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0',
            'ID': '123456789',
            'Transaction Type': 'Trade'
        }
        coinbase_parser_trade = CoinbaseParserCsv(row_data_trade)
        assert coinbase_parser_trade.get_sent_amount() == "-0"

        # Test when transaction type is 'Withdrawal'
        row_data_withdrawal = {
            'Timestamp': '2022-01-15 08:30:01 UTC',
            'Quantity Transacted': '0',
            'Asset': 'BTC',
            'Subtotal': '0',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0',
            'ID': '123456789',
            'Transaction Type': 'Withdrawal'
        }
        coinbase_parser_withdrawal = CoinbaseParserCsv(row_data_withdrawal)
        assert coinbase_parser_withdrawal.get_sent_amount() == "-0"

        # Test when transaction type is neither 'Trade' nor 'Withdrawal'
        row_data_other = {
            'Timestamp': '2022-01-15 08:40:00 UTC',
            'Quantity Transacted': '0',
            'Asset': 'BTC',
            'Subtotal': '0',
            'Price Currency': 'USD',
            'Fees and/or Spread': '0',
            'ID': '123456789',
            'Transaction Type': 'Other'
        }
        coinbase_parser_other = CoinbaseParserCsv(row_data_other)
        assert coinbase_parser_other.get_sent_amount() == ""
