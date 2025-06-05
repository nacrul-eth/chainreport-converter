import pytest
from src.chainreport_parser.kraken_parser import KrakenParserCsv

class TestCheckIfSkipLine:

    # returns True when 'type' is 'transfer'
    def test_returns_true_when_type_is_transfer(self):
        row = {'time': '2023-01-01 00:00:00', 'amount': '1.0', 'asset': 'BTC', 'fee': '0.1', 'txid': '12345', 'type': 'transfer'}
        parser = KrakenParserCsv(row)
        assert parser.check_if_skip_line() is True

    # returns False when 'type' is None
    def test_returns_false_when_type_is_none(self):
        row = {'time': '2023-01-01 00:00:00', 'amount': '1.0', 'asset': 'BTC', 'fee': '0.1', 'txid': '12345', 'type': None}
        parser = KrakenParserCsv(row)
        assert parser.check_if_skip_line() is False

    # returns False when 'type' is 'deposit'
    def test_returns_false_when_type_is_deposit(self):
        row = {'time': '2023-01-01 00:00:00', 'amount': '1.0', 'asset': 'BTC', 'fee': '0.1', 'txid': '12345', 'type': 'deposit'}
        parser = KrakenParserCsv(row)
        assert parser.check_if_skip_line() is False

    # returns False when 'type' is 'withdrawal'
    def test_returns_false_when_type_is_withdrawal(self):
        row = {'time': '2023-01-01 00:00:00', 'amount': '1.0', 'asset': 'BTC', 'fee': '0.1', 'txid': '12345', 'type': 'withdrawal'}
        parser = KrakenParserCsv(row)
        assert parser.check_if_skip_line() is False

    # returns False when 'type' is 'trade'
    def test_returns_false_when_type_is_trade(self):
        row = {'time': '2023-01-01 00:00:00', 'amount': '1.0', 'asset': 'BTC', 'fee': '0.1', 'txid': '12345', 'type': 'trade'}
        parser = KrakenParserCsv(row)
        assert parser.check_if_skip_line() is False

    # returns False when 'type' is an empty string
    def test_returns_false_when_type_is_empty_string(self):
        row = {'time': '2023-01-01 00:00:00', 'amount': '1.0', 'asset': 'BTC', 'fee': '0.1', 'txid': '12345', 'type': ''}
        parser = KrakenParserCsv(row)
        assert parser.check_if_skip_line() is False

    # returns False when 'type' is not in SKIPSTRINGS
    def test_returns_false_when_type_is_not_in_skipstrings(self):
        row = {'time': '2023-01-01 00:00:00', 'amount': '1.0', 'asset': 'BTC', 'fee': '0.1', 'txid': '12345', 'type': 'not_skip'}
        parser = KrakenParserCsv(row)
        assert parser.check_if_skip_line() is False

    # returns False when 'type' is a numeric value
    def test_returns_false_when_type_is_numeric(self):
        row = {'time': '2023-01-01 00:00:00', 'amount': '1.0', 'asset': 'BTC', 'fee': '0.1', 'txid': '12345', 'type': '123'}
        parser = KrakenParserCsv(row)
        assert parser.check_if_skip_line() is False

    # returns False when 'type' is a mixed-case string not in SKIPSTRINGS
    def test_returns_false_when_type_is_mixed_case_not_in_skipstrings(self):
        row = {'time': '2023-01-01 00:00:00', 'amount': '1.0', 'asset': 'BTC', 'fee': '0.1', 'txid': '12345', 'type': 'MixedCase'}
        parser = KrakenParserCsv(row)
        assert parser.check_if_skip_line() is False

    # returns False when 'type' is a special character
    def test_returns_false_when_type_is_special_character(self):
        row = {'time': '2023-01-01 00:00:00', 'amount': '1.0', 'asset': 'BTC', 'fee': '0.1', 'txid': '12345', 'type': '!@#$%'}
        parser = KrakenParserCsv(row)
        assert parser.check_if_skip_line() is False

    # returns False when 'type' is a very long string
    def test_returns_false_when_type_is_very_long_string(self):
        row = {'time': '2023-01-01 00:00:00', 'amount': '1.0', 'asset': 'BTC', 'fee': '0.1', 'txid': '12345', 'type': 'a_very_long_string_that_should_make_the_test_return_false'}
        parser = KrakenParserCsv(row)
        assert parser.check_if_skip_line() is False

    # handles missing 'type' key in input_row without crashing
    def test_handles_missing_type_key(self):
        row = {'time': '2023-01-01 00:00:00', 'amount': '1.0', 'asset': 'BTC', 'fee': '0.1', 'txid': '12345'}
        parser = KrakenParserCsv(row)
        assert parser.check_if_skip_line() is False

    # handles unexpected data types for 'type' gracefully
    def test_handles_unexpected_data_types_gracefully(self):
        row = {'time': '2023-01-01 00:00:00', 'amount': '1.0', 'asset': 'BTC', 'fee': '0.1', 'txid': '12345', 'type': 123}
        parser = KrakenParserCsv(row)
        assert parser.check_if_skip_line() is False

class TestGetInputString:

    # Returns the exact input row that was passed during initialization
    def test_returns_exact_input_row(self):
        input_row = {
            'time': '2023-10-01 12:00:00',
            'amount': '100.0',
            'asset': 'BTC',
            'fee': '0.1',
            'txid': '12345',
            'type': 'deposit'
        }
        parser = KrakenParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles missing 'type' field gracefully
    def test_handles_missing_type_field(self):
        input_row = {
            'time': '2023-10-01 12:00:00',
            'amount': '100.0',
            'asset': 'BTC',
            'fee': '0.1',
            'txid': '12345'
        }
        parser = KrakenParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Can handle rows with additional unexpected fields without issues
    def test_handles_additional_unexpected_fields(self):
        input_row = {
            'time': '2023-10-01 12:00:00',
            'amount': '100.0',
            'asset': 'BTC',
            'fee': '0.1',
            'txid': '12345',
            'type': 'deposit',
            'extra_field': 'additional_data'
        }
        parser = KrakenParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Works correctly with empty input row
    def test_works_correctly_with_empty_input_row(self):
        input_row = {}
        parser = KrakenParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with None values
    def test_handles_input_row_with_none_values(self):
        input_row = {
            'time': None,
            'amount': None,
            'asset': None,
            'fee': None,
            'txid': None,
            'type': None
        }
        parser = KrakenParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Deals with input row containing special characters
    def test_deals_with_input_row_containing_special_characters(self):
        input_row = {
            'time': '2023-10-01 12:00:00',
            'amount': '100.0',
            'asset': 'BTC$',
            'fee': '0.1',
            'txid': '12345',
            'type': 'deposit'
        }
        parser = KrakenParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Manages input row with very large strings
    def test_manages_input_row_with_very_large_strings(self):
        input_row = {
            'time': '2023-10-01 12:00:00',
            'amount': '100.0',
            'asset': 'BTC',
            'fee': '0.1',
            'txid': '12345',
            'type': 'deposit'
        }
        # Create a very large string for testing
        large_string = "A" * 1000000
        input_row['large_string'] = large_string
    
        parser = KrakenParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with mixed data types (e.g., strings, numbers)
    def test_handles_mixed_data_types(self):
        input_row = {
            'time': '2023-10-01 12:00:00',
            'amount': 100.0,
            'asset': 'BTC',
            'fee': 0.1,
            'txid': '12345',
            'type': 'deposit'
        }
        parser = KrakenParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Manages input row with boolean values
    def test_manages_input_row_with_boolean_values(self):
        input_row = {
            'time': '2023-10-01 12:00:00',
            'amount': True,
            'asset': False,
            'fee': True,
            'txid': False,
            'type': True
        }
        parser = KrakenParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with nested dictionaries
    def test_handles_input_row_with_nested_dictionaries(self):
        input_row = {
            'time': '2023-10-01 12:00:00',
            'amount': '100.0',
            'asset': 'BTC',
            'fee': '0.1',
            'txid': '12345',
            'type': 'deposit',
            'nested_data': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        parser = KrakenParserCsv(input_row)
        assert parser.get_input_string() == input_row

class TestGetDateString:

    # correctly parses a valid date string in the expected format
    def test_correctly_parses_valid_date_string(self):
        row = {
            'time': '2023-01-01 12:00:00'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_date_string() == '01.01.2023 12:00'

    # raises an error for malformed date strings
    def test_raises_error_for_malformed_date_strings(self):
        row = {
            'time': 'malformed date'
        }
        parser = KrakenParserCsv(row)
        with pytest.raises(ValueError):
            parser.get_date_string()

    # handles dates at the boundary of months and years correctly
    def test_handles_dates_at_boundary_of_months_and_years_correctly(self):
        row = {
            'time': '2023-01-31 23:59:59'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_date_string() == '31.01.2023 23:59'

    # handles missing 'time' field gracefully
    def test_handles_missing_time_field_gracefully(self):
        row = {}
        parser = KrakenParserCsv(row)
        with pytest.raises(KeyError):
            parser.get_date_string()

    # handles leap year dates accurately
    def test_handles_leap_year_dates(self):
        row = {
            'time': '2024-02-29 12:00:00'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_date_string() == '29.02.2024 12:00'

    # handles dates with varying lengths of whitespace
    def test_handles_dates_with_varying_whitespace(self):
        row = {
            'time': '2023-01-01  12:00:00'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_date_string() == '01.01.2023 12:00'

    # ensures no side effects or state changes in the method
    def test_no_side_effects_or_state_changes(self):
        row = {
            'time': '2023-01-01 12:00:00'
        }
        parser = KrakenParserCsv(row)
        initial_input_row = parser.get_input_string()
        initial_date_string = parser.get_date_string()

        # Call the method again
        second_date_string = parser.get_date_string()

        assert initial_input_row == row
        assert initial_date_string == '01.01.2023 12:00'
        assert second_date_string == initial_date_string

class TestGetTransactionType:

    # Returns 'Deposit' for transaction descriptions in DEPOSITTRANSACTION
    def test_returns_deposit_for_deposit_transaction(self):
        row = {
            'type': 'deposit',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'Deposit'

    # Handles missing 'type' key in input_row gracefully
    def test_handles_missing_type_key_gracefully(self):
        row = {
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Returns 'Withdrawal' for transaction descriptions in WITHDRAWTRANSACTION
    def test_returns_withdrawal_for_withdrawal_transaction(self):
        row = {
            'type': 'withdrawal',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'Withdrawal'

    # Returns 'Trade' for transaction descriptions in TRADETRANSACTION
    def test_returns_trade_for_trade_transaction(self):
        row = {
            'type': 'trade',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'Trade'

    # Returns 'ERROR' for transaction descriptions not in any defined lists
    def test_returns_error_for_unknown_transaction_descriptions(self):
        row = {
            'type': 'unknown_transaction',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Handles unexpected data types for transaction type (e.g., integer, list)
    def test_handles_unexpected_data_types_for_transaction_type(self):
        row = {
            'type': 123,  # unexpected data type
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Handles input_row with whitespace around 'type'
    def test_handles_whitespace_around_type(self):
        row = {
            'type': '   deposit   ',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'Deposit'

    # Handles empty string as transaction type
    def test_handles_empty_string_as_transaction_type(self):
        row = {
            'type': '',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Handles None as transaction type
    def test_handles_none_as_transaction_type(self):
        row = {
            'type': None,
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Handles input_row with special characters in 'type'
    def test_handles_special_characters_in_type(self):
        row = {
            'type': 'SPECIAL_CHARACTER$',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Handles input_row with numeric strings as 'type'
    def test_handles_numeric_strings_as_type(self):
        row = {
            'type': '123',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Returns 'ERROR' for unknown transaction types
    def test_returns_error_for_unknown_transaction_types(self):
        row = {
            'type': 'unknown_type',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Correctly identifies transaction type with minimal input_row
    def test_correctly_identifies_transaction_type_with_minimal_input_row(self):
        row = {
            'type': 'deposit'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'Deposit'

    # Handles input_row with multiple valid transaction types
    def test_handles_multiple_valid_transaction_types(self):
        row = {
            'type': 'deposit',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'Deposit'
        row['type'] = 'withdrawal'
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'Withdrawal'
        row['type'] = 'trade'
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'Trade'

    # Handles input_row with additional irrelevant keys
    def test_handles_additional_irrelevant_keys(self):
        row = {
            'type': 'deposit',
            'amount': '100.50',
            'asset': 'BTC',
            'irrelevant_key1': 'value1',
            'irrelevant_key2': 'value2'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'Deposit'

    # Handles large input_row dictionaries with many keys
    def test_handles_large_input_row_with_many_keys(self):
        row = {
            'type': 'DAILY_REBATE_DISTRIBUTION',
            'createdAt': '2022-01-01T12:34:56.789Z',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890',
            'description': 'Daily rebate distribution',
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
        parser = KrakenParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

class TestGetReceivedAmount:

    # Returns received amount with comma as decimal separator for deposit transactions
    def test_returns_received_amount_with_comma_for_deposit(self):
        row = {
            'amount': '100.50',
            'type': 'deposit'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_amount() == '100,50'

    # Returns empty string for trade transactions with negative amount
    def test_returns_empty_string_for_negative_trade(self):
        row = {
            'amount': '-100.50',
            'type': 'trade'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_amount() == ''

    # Returns received amount with comma as decimal separator for trade transactions with positive amount
    def test_returns_received_amount_with_comma_for_trade_positive_amount(self):
        row = {
            'amount': '50.75',
            'type': 'trade'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_amount() == '50,75'

    # Returns empty string for withdrawal transactions
    def test_returns_empty_string_for_withdrawal_transactions(self):
        row = {
            'amount': '50.25',
            'type': 'withdrawal'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_amount() == ''

    # Handles input row where amount is an empty string
    def test_handles_empty_amount(self):
        row = {
            'amount': '',
            'type': 'deposit'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_amount() == ''

    # # Processes input row where amount contains only a decimal point
    # def test_received_amount_with_decimal_point_only(self):
    #     row = {
    #         'amount': '.',
    #         'type': 'deposit'
    #     }
    #     parser = KrakenParserCsv(row)
    #     assert parser.get_received_amount() == ''

    # Handles input row where amount is missing
    def test_handles_input_row_where_amount_is_missing(self):
        row = {
            'type': 'deposit'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_amount() == ''

    # Handles input row where amount is a negative number
    def test_handles_negative_received_amount(self):
        row = {
            'amount': '-50.75',
            'type': 'trade'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_amount() == ''

    # Checks if amount with special characters is handled or raises an error
    def test_special_characters_handling(self):
        row = {
            'amount': '100.50$',
            'type': 'deposit'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_amount() == '100,50$'

    # Verifies that amount with leading or trailing spaces is trimmed and processed correctly
    def test_amount_with_spaces_trimmed_correctly(self):
        row = {
            'amount': '  50.25  ',
            'type': 'deposit'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_amount() == '50,25'

    # # Ensures that the method handles unexpected transaction types gracefully
    # def test_handles_unexpected_transaction_types_gracefully(self):
    #     row = {
    #         'amount': '50.25',
    #         'type': 'unknown'
    #     }
    #     parser = KrakenParserCsv(row)
    #     assert parser.get_received_amount() == ''

    # # Confirms that the method handles non-string amount values gracefully
    # def test_handles_non_string_amount_values_gracefully(self):
    #     row = {
    #         'amount': 100.50,
    #         'type': 'deposit'
    #     }
    #     parser = KrakenParserCsv(row)
    #     assert parser.get_received_amount() == '100,50'

    # Verifies that amount with different locale-specific formats is handled correctly
    def test_handles_locale_specific_formats(self):
        row = {
            'amount': '100.50',
            'type': 'deposit'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_amount() == '100,50'

class TestGetReceivedCurrency:

    # Returns the correct currency for deposit transactions
    def test_returns_correct_currency_for_deposit_transactions(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'deposit',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == "BTC"

    # Returns an empty string for withdrawal transactions
    def test_returns_empty_string_for_withdrawal_transactions(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'withdrawal',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == ""

    # Returns the correct currency for trade transactions with positive received amount
    def test_returns_correct_currency_for_trade_transactions(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'trade',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == "BTC"

    # Returns the correct currency for staking transactions
    def test_returns_correct_currency_for_staking_transactions(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'staking',
            'amount': '50.25',
            'asset': 'ETH'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == "ETH"

    # Returns the correct currency for airdrop transactions
    def test_returns_correct_currency_for_airdrop_transactions(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'airdrop',
            'amount': '50.25',
            'asset': 'ETH'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == "ETH"

    # Returns the correct currency for cashback transactions
    def test_returns_correct_currency_for_cashback_transactions(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'cashback',
            'amount': '10.00',
            'asset': 'ETH'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == "ETH"

    # Returns the correct currency for payment transactions
    def test_returns_correct_currency_for_payment_transactions(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'payment',
            'amount': '50.25',
            'asset': 'ETH'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == "ETH"

    # Handles missing 'asset' key gracefully
    def test_handles_missing_asset_key_gracefully(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'deposit',
            'amount': '100.50'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == ""

    # Returns an empty string for trade transactions with negative received amount
    def test_returns_empty_string_for_negative_received_amount_in_trade_transactions(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'trade',
            'amount': '-50.25',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == ""

    # Handles missing 'type' key gracefully
    def test_handles_missing_type_key_gracefully(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == ""

    # Handles missing 'amount' key gracefully
    def test_handles_missing_amount_key_gracefully(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'deposit',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == ""

    # Handles non-string 'asset' values
    def test_handles_non_string_asset_values(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'trade',
            'amount': '100.50',
            'asset': 12345
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == ""

    # Handles mixed case in 'type' values
    def test_handles_mixed_case_in_type_values(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'DePoSit',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == "BTC"

    # Handles extra whitespace in 'asset' values
    def test_handles_extra_whitespace_in_asset_values(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'trade',
            'amount': '100.50',
            'asset': '   BTC   '
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == "   BTC   "

    # Handles extra whitespace in 'type' values
    def test_handles_extra_whitespace_in_type_values(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': '  trade  ',
            'amount': '100.50',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == "BTC"

    # Handles unexpected transaction types by returning the currency
    def test_handles_unexpected_transaction_types(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'unexpected_type',
            'amount': '-50.25',
            'asset': 'ETH'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == "ETH"

    # Handles extra whitespace in 'amount' values
    def test_handles_extra_whitespace_in_amount_values(self):
        row = {
            'time': '2023-01-01 12:00:00',
            'type': 'trade',
            'amount': '  100.50  ',
            'asset': 'BTC'
        }
        parser = KrakenParserCsv(row)
        assert parser.get_received_currency() == "BTC"