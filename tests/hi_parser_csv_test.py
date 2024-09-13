import pytest
from datetime import datetime
from src.chainreport_parser.hi_parser_csv import HiParserCsv

class TestCheckIfSkipLine:

    def test_check_if_skip_line_not_referral_rewards(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'Crypto deposit',
            'Received Amount': '100',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        skip_line = parser.check_if_skip_line()

        assert not skip_line

    def test_check_if_skip_line_not_called_for_referral_rewards(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'HI referrer reward',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        parser.check_if_skip_line()  # Call the method to test

        # Assert that the method does not raise an exception
        assert True

    def test_check_if_skip_line_with_empty_input_row(self):
        input_row = {}
        parser = HiParserCsv(input_row)
        skip_line = parser.check_if_skip_line()

        assert not skip_line

    def test_check_if_skip_line_with_whitespace_description(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': '   ',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        skip_line = parser.check_if_skip_line()

        assert skip_line

    def test_check_if_skip_line_with_leading_trailing_whitespace_description(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': '   HI referrer reward   ',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        skip_line = parser.check_if_skip_line()

        assert skip_line == False

    def test_check_if_skip_line_with_multiple_consecutive_whitespace_description(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': '   HI referrer reward   ',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        skip_line = parser.check_if_skip_line()

        assert not skip_line

    def test_check_if_skip_line_with_non_alphanumeric_description(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'HI referrer reward $100!',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        skip_line = parser.check_if_skip_line()

        assert not skip_line

    def test_check_if_skip_line_with_special_characters(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'HI referrer reward $100!',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        skip_line = parser.check_if_skip_line()

        assert not skip_line

    def test_check_if_skip_line_with_numeric_description(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'HI referrer reward 100',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        skip_line = parser.check_if_skip_line()

        assert not skip_line

    def test_check_if_skip_line_with_non_english_description(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'हिंदी रेफरर रिवार्ड',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        skip_line = parser.check_if_skip_line()

        assert not skip_line

class TestGetDateString:

    # correctly parses a valid date string in the expected format
    def test_correctly_parses_valid_date_string(self):
        intput_row = {
            'Date': '2023-01-13 03:06 UTC',
            'Description': 'Crypto deposit',
            'Received Amount': '100',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(intput_row)
        assert parser.get_date_string() == '13.01.2023 03:06'

    # handles missing 'createdAt' field gracefully
    def test_handles_missing_createdAt_field(self):
        intput_row = {
            'Description': 'Crypto deposit',
            'Received Amount': '100',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(intput_row)
        with pytest.raises(KeyError):
            parser.get_date_string()

    # raises an error for malformed date strings
    def test_raises_error_for_malformed_date_strings(self):
        input_row = {
            'Date': 'malformed date string',
            'Description': 'Crypto deposit',
            'Received Amount': '100',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        with pytest.raises(ValueError):
            parser.get_date_string()

    # handles leap year dates accurately
    def test_handles_leap_year_dates(self):
        input_row = {
            'Date': '2024-02-29 12:00 UTC',
            'Description': 'Crypto deposit',
            'Received Amount': '100',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        assert parser.get_date_string() == '29.02.2024 12:00'

    # handles dates at the boundary of months and years correctly
    def test_handles_dates_at_boundary_of_months_and_years_correctly(self):
        input_row = {
            'Date': '2023-01-31 23:59 UTC',
            'Description': 'Crypto deposit',
            'Received Amount': '100',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        assert parser.get_date_string() == '31.01.2023 23:59'

    # processes dates with single-digit days and months correctly
    def test_processes_single_digit_dates_correctly(self):
        input_row = {
            'Date': '2023-01-01 03:59 UTC',
            'Description': 'Crypto deposit',
            'Received Amount': '100',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        assert parser.get_date_string() == '01.01.2023 03:59'

    # ensures no side effects or state changes in the method
    def test_no_side_effects_or_state_changes(self):
        input_row = {
            'Date': '2023-01-01 12:00 UTC',
            'Description': 'Crypto deposit',
            'Received Amount': '100',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        initial_input_row = parser.get_input_string()
        initial_date_string = parser.get_date_string()

        # Call the method again
        second_date_string = parser.get_date_string()

        assert initial_input_row == input_row
        assert initial_date_string == '01.01.2023 12:00'
        assert second_date_string == initial_date_string

class TestGetTransactionType:

    def test_hi_parser_csv_empty_referral_string(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'HI referrer reward',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        transaction_type = parser.get_transaction_type()

        assert transaction_type == 'Referral_Rewards'

    def test_hi_parser_csv_referral_string_lowercase(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'hi referrer reward',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        transaction_type = parser.get_transaction_type()

        assert transaction_type == 'Referral_Rewards'

    def test_hi_parser_csv_referral_string_uppercase(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'HI REFERRER REWARD',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        transaction_type = parser.get_transaction_type()

        assert transaction_type == 'Referral_Rewards'

    def test_hi_parser_csv_multiple_referral_strings(self):
        input_rows = [
            {
                'Date': '2022-01-01 12:00 UTC',
                'Description': 'HI referrer reward',
                'Received Amount': '0',
                'Received Currency': 'HI',
                'Sent Amount': '0',
                'Sent Currency': 'HI',
                'Fee Amount': '0',
                'Fee Currency': 'HI',
                'TxHash': 'abc123'
            },
            {
                'Date': '2022-01-01 12:00 UTC',
                'Description': 'hi referrer rebate',
                'Received Amount': '0',
                'Received Currency': 'HI',
                'Sent Amount': '0',
                'Sent Currency': 'HI',
                'Fee Amount': '0',
                'Fee Currency': 'HI',
                'TxHash': 'abc123'
            },
            {
                'Date': '2022-01-01 12:00 UTC',
                'Description': 'HI REFERRER REWARD',
                'Received Amount': '0',
                'Received Currency': 'HI',
                'Sent Amount': '0',
                'Sent Currency': 'HI',
                'Fee Amount': '0',
                'Fee Currency': 'HI',
                'TxHash': 'abc123'
            }
        ]
        expected_transaction_types = ['Referral_Rewards', 'Referral_Rewards', 'Referral_Rewards']

        for i, input_row in enumerate(input_rows):
            parser = HiParserCsv(input_row)
            transaction_type = parser.get_transaction_type()

            assert transaction_type == expected_transaction_types[i]

    def test_hi_parser_csv_referral_string_special_characters(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'HI referrer reward $100',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        transaction_type = parser.get_transaction_type()

        assert transaction_type == 'ERROR'

    def test_hi_parser_csv_referral_string_mixed_case_special_characters(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'hI Referrer Reward',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        transaction_type = parser.get_transaction_type()

        assert transaction_type == 'Referral_Rewards'

    def test_hi_parser_csv_referral_string_non_english_characters(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'हिंदी रेफरर रिवार्ड',
            'Received Amount': '0',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        transaction_type = parser.get_transaction_type()

        assert transaction_type == 'ERROR'

class TestGetReceivedAmount:
    def test_get_received_amount_handles_non_numeric_received_amount(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'Crypto deposit',
            'Received Amount': 'non-numeric',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        received_amount = parser.get_received_amount()

        assert received_amount == 'non-numeric'

    def test_hi_parser_csv_negative_received_amount(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'Crypto deposit',
            'Received Amount': '-100',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        received_amount = parser.get_received_amount()

        assert received_amount == '-100'

    def test_get_received_amount_handles_leading_zeros_correctly(self):
        input_row = {
            'Date': '2022-01-01 12:00 UTC',
            'Description': 'Crypto deposit',
            'Received Amount': '00100.00',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        received_amount = parser.get_received_amount()

        assert received_amount == '00100,00'

    def test_get_received_amount_trailing_zeros(self):
        input_row = {
            'Received Amount': '100.00',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123',
            'Description': 'Crypto deposit'
        }
        parser = HiParserCsv(input_row)
        received_amount = parser.get_received_amount()

        assert received_amount == '100,00'

    def test_get_received_amount_with_decimal_places(self):
        input_row = {
            'Received Amount': '123.45',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123',
            'Description': 'Crypto deposit'
        }
        parser = HiParserCsv(input_row)
        received_amount = parser.get_received_amount()

        assert received_amount == '123,45'

    def test_get_received_amount_handles_leading_and_trailing_spaces(self):
        input_row = {
            'Received Amount': '  100.00  '
        }
        parser = HiParserCsv(input_row)
        received_amount = parser.get_received_amount()

        assert received_amount == '100,00'

    def test_get_received_amount_handles_multiple_consecutive_spaces_correctly(self):
        input_row = {
            'Received Amount': '  100.00  ',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123'
        }
        parser = HiParserCsv(input_row)
        received_amount = parser.get_received_amount()

        assert received_amount == '100,00'

    def test_get_received_amount_handles_non_alphanumeric_characters_correctly(self):
        input_row = {
            'Received Amount': '100.50',
            'Received Currency': 'HI',
            'Sent Amount': '0',
            'Sent Currency': 'HI',
            'Fee Amount': '0',
            'Fee Currency': 'HI',
            'TxHash': 'abc123',
            'Description': 'Crypto deposit'
        }
        parser = HiParserCsv(input_row)
        received_amount = parser.get_received_amount()

        assert received_amount == '100,50'

    def test_get_received_amount_with_non_english_characters(self):
        input_row = {
            'Received Amount': '100.50',
            'Received Currency': 'HI',
            'Description': 'हिंदी रिसीव्ड'
        }
        parser = HiParserCsv(input_row)
        received_amount = parser.get_received_amount()

        assert received_amount == '100,50'

    # Handles cases where 'Received Amount' key is missing in the input row
    def test_handles_missing_sent_currency_key(self):
        input_row = {}
        parser = HiParserCsv(input_row)
        assert parser.get_received_amount() == ''

class TestGetReceivedCurrency:

    # Returns the received currency when 'Received Currency' is a valid string
    def test_returns_received_currency_when_valid_string(self):
        input_row = {'Received Currency': 'USD'}
        parser = HiParserCsv(input_row)
        assert parser.get_received_currency() == 'USD'

    # Handles cases where 'Received Currency' key is missing in the input row
    def test_handles_missing_received_currency_key(self):
        input_row = {}
        parser = HiParserCsv(input_row)
        assert parser.get_received_currency() == ''

    # Returns an empty string when 'Received Currency' is None
    def test_returns_empty_string_when_received_currency_is_none(self):
        input_row = {'Received Currency': None}
        parser = HiParserCsv(input_row)
        assert parser.get_received_currency() == ''

    # Returns an empty string when 'Received Currency' is not a string
    def test_returns_empty_string_when_received_currency_not_string(self):
        input_row = {'Received Currency': 123}
        parser = HiParserCsv(input_row)
        assert parser.get_received_currency() == ''

    # Handles cases where 'Received Currency' is a numeric value
    def test_handles_numeric_received_currency(self):
        input_row = {'Received Currency': 100}
        parser = HiParserCsv(input_row)
        assert parser.get_received_currency() == ''

    # Handles cases where 'Received Currency' is an empty string
    def test_handles_empty_received_currency(self):
        input_row = {'Received Currency': ''}
        parser = HiParserCsv(input_row)
        assert parser.get_received_currency() == ''

    # Handles cases where 'Received Currency' is a boolean value
    def test_handles_boolean_received_currency(self):
        input_row = {'Received Currency': True}
        parser = HiParserCsv(input_row)
        assert parser.get_received_currency() == ''

    # Handles cases where 'Received Currency' is a list or dictionary
    def test_handles_list_received_currency(self):
        input_row = {'Received Currency': ['USD', 'EUR']}
        parser = HiParserCsv(input_row)
        assert parser.get_received_currency() == ''

    # Handles cases where input_row is an empty dictionary
    def test_empty_input_row(self):
        input_row = {}
        parser = HiParserCsv(input_row)
        assert parser.get_received_currency() == ''

    # Handles cases where input_row contains unexpected data types
    def test_handles_unexpected_data_types(self):
        input_row = {'Received Currency': 123}  # Integer instead of string
        parser = HiParserCsv(input_row)
        assert parser.get_received_currency() == ''

    # Handles cases where input_row contains special characters in 'Received Currency'
    def test_handles_special_characters_in_received_currency(self):
        input_row = {'Received Currency': '$€¥'}
        parser = HiParserCsv(input_row)
        assert parser.get_received_currency() == '$€¥'

    # Handles cases where input_row contains nested dictionaries
    def test_returns_empty_string_when_received_currency_is_nested_dictionary(self):
        input_row = {'Received Currency': {'currency': 'USD'}}
        parser = HiParserCsv(input_row)
        assert parser.get_received_currency() == ''

    # Handles cases where input_row contains unicode characters in 'Received Currency'
    def test_handles_unicode_characters(self):
        input_row = {'Received Currency': u'\u20AC'}  # Euro symbol as unicode character
        parser = HiParserCsv(input_row)
        assert parser.get_received_currency() == u'\u20AC'

class TestGetSentAmount:

    # Returns formatted sent amount when 'Sent Amount' is present and valid
    def test_returns_formatted_sent_amount_when_present_and_valid(self):
        input_row = {'Sent Amount': '1234.56'}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_amount() == '1234,56'

    # Handles 'Sent Amount' with only whitespace correctly
    def test_handles_sent_amount_with_only_whitespace_correctly(self):
        input_row = {'Sent Amount': '   '}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_amount() == ''

    # Returns empty string when 'Sent Amount' is None
    def test_returns_empty_string_when_sent_amount_is_none(self):
        input_row = {'Sent Amount': None}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_amount() == ''

    # Returns empty string when 'Sent Amount' is not present in input_row
    def test_returns_empty_string_when_sent_amount_not_present(self):
        input_row = {'Received Currency': 'USD'}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_amount() == ''

    # Correctly replaces decimal point with comma in 'Sent Amount'
    def test_correctly_replaces_decimal_point_with_comma(self):
        input_row = {'Sent Amount': '123.45'}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_amount() == '123,45'

    # Handles 'Sent Amount' with special characters
    def test_handles_sent_amount_with_special_characters(self):
        input_row = {'Sent Amount': '1,234.56'}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_amount() == '1,234,56'

    # Handles 'Sent Amount' with multiple decimal points
    def test_handles_sent_amount_with_multiple_decimal_points(self):
        input_row = {'Sent Amount': '123.456.789'}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_amount() == '123,456,789'

    # Handles 'Sent Amount' with mixed numeric and alphabetic characters
    def test_handles_mixed_numeric_and_alphabetic_characters(self):
        input_row = {'Sent Amount': '12.34USD'}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_amount() == '12,34USD'

    # Strips leading and trailing whitespace from 'Sent Amount'
    def test_strips_whitespace_from_sent_amount(self):
        input_row = {'Sent Amount': '  100.50  '}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_amount() == '100,50'

    # Handles 'Sent Amount' with different locale-specific number formats
    def test_handles_sent_amount_with_locale_specific_format(self):
        input_row = {'Sent Amount': '123.45'}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_amount() == '123,45'

    # Handles very small numeric values in 'Sent Amount'
    def test_handles_very_small_numeric_values(self):
        input_row = {'Sent Amount': '0.00000001'}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_amount() == '0,00000001'

    # Handles large numeric values in 'Sent Amount'
    def test_handles_large_numeric_values(self):
        input_row = {'Sent Amount': '123456789.987654321'}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_amount() == '123456789,987654321'

    # Handles 'Sent Amount' with negative values
    def test_handles_sent_amount_with_negative_values(self):
        input_row = {'Sent Amount': '-12.345'}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_amount() == '-12,345'

class TestGetSentCurrency:

    # Returns the 'Sent Currency' when it is a non-empty string
    def test_returns_sent_currency_when_valid_string(self):
        input_row = {'Sent Currency': 'BTC'}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_currency() == 'BTC'

    # Handles cases where 'Sent Currency' key is missing in the input row
    def test_handles_missing_sent_currency_key(self):
        input_row = {}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_currency() == ''

    # Handles cases where 'Sent Currency' is a boolean value
    def test_handles_boolean_sent_currency(self):
        input_row = {'Sent Currency': True}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_currency() == ''

    # Returns an empty string when 'Sent Currency' is not a string
    def test_returns_empty_string_when_sent_currency_not_string(self):
        input_row = {'Sent Currency': None}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_currency() == ''

    # Handles cases where 'Sent Currency' is an empty string
    def test_handles_empty_sent_currency(self):
        input_row = {'Sent Currency': ''}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_currency() == ''

    # Returns an empty string when 'Sent Currency' is None
    def test_returns_empty_string_when_sent_currency_is_none(self):
        input_row = {'Sent Currency': None}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_currency() == ''

    # Handles cases where 'Sent Currency' is a numeric value
    def test_handles_numeric_sent_currency(self):
        input_row = {'Sent Currency': 100}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_currency() == ''

    # Handles cases where 'Sent Currency' is a list or dictionary
    def test_handles_list_input(self):
        input_row = {'Sent Currency': ['USD', 'EUR']}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_currency() == ''

    # Handles cases where input_row contains unexpected keys
    def test_handles_unexpected_keys(self):
        input_row = {'Sent Currency': 'BTC', 'Unexpected Key': 'Value'}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_currency() == 'BTC'

    # Handles cases where input_row contains special characters in 'Sent Currency'
    def test_handles_special_characters_in_sent_currency(self):
        input_row = {'Sent Currency': 'BTC$'}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_currency() == 'BTC$'

    # Handles cases where input_row contains very large strings in 'Sent Currency'
    def test_handles_large_string_sent_currency(self):
        input_row = {'Sent Currency': 'A' * 1000000}
        parser = HiParserCsv(input_row)
        assert parser.get_sent_currency() == 'A' * 1000000

class TestGetTransactionFeeAmount:

    # Extracts 'Fee Amount' from input row and formats it correctly
    def test_extracts_and_formats_fee_amount_correctly(self):
        input_row = {'Fee Amount': '1234.56'}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == '1234,56'

    # 'Fee Amount' is an empty string
    def test_fee_amount_is_empty_string(self):
        input_row = {'Fee Amount': ''}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == ''

    # Returns formatted fee amount as a string
    def test_returns_fee_amount_formatted_with_comma(self):
        input_row = {'Fee Amount': '25.50'}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == '25,50'

    # Handles fee amount with decimal points correctly
    def test_handles_fee_amount_with_decimal_points_correctly(self):
        input_row = {'Fee Amount': '25.75'}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == '25,75'

    # Returns empty string if 'Fee Amount' is not present
    def test_returns_empty_string_when_fee_amount_not_present(self):
        input_row = {}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == ''

    # Returns empty string if 'Fee Amount' is None
    def test_returns_empty_string_when_fee_amount_is_none(self):
        input_row = {'Fee Amount': None}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == ''

    # 'Fee Amount' is a numeric string without a decimal point
    def test_fee_amount_numeric_string_no_decimal(self):
        input_row = {'Fee Amount': '500'}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == '500'

    # 'Fee Amount' contains only whitespace
    def test_fee_amount_contains_only_whitespace(self):
        input_row = {'Fee Amount': '   '}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == ''

    # 'Fee Amount' is a numeric string with multiple decimal points
    def test_fee_amount_with_multiple_decimal_points(self):
        input_row = {'Fee Amount': '123.456.789'}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == '123,456,789'

    # Handles large numeric values in 'Fee Amount'
    def test_handles_large_numeric_values(self):
        input_row = {'Fee Amount': '1234567890.1234567890'}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == '1234567890,1234567890'

    # Handles 'Fee Amount' with leading and trailing spaces
    def test_handles_fee_amount_with_spaces(self):
        input_row = {'Fee Amount': '  25.50  '}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == '25,50'

    # 'Fee Amount' contains non-numeric characters
    def test_fee_amount_contains_non_numeric_characters(self):
        input_row = {'Fee Amount': '12.34$'}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == '12,34$'

    # Handles very small numeric values in 'Fee Amount'
    def test_handles_very_small_numeric_values(self):
        input_row = {'Fee Amount': '0.000001'}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == '0,000001'

    # Consistent return type regardless of input
    def test_consistent_return_type(self):
        input_row = {'Fee Amount': '10.50'}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_amount() == '10,50'

    # Ensures no modification to input_row dictionary
    def test_no_modification_to_input_row(self):
        input_row = {'Fee Amount': '10.50'}
        original_input_row = input_row.copy()
        parser = HiParserCsv(input_row)
        parser.get_transaction_fee_amount()
        assert input_row == original_input_row

class TestGetTransactionFeeCurrency:

    # Returns the fee currency when 'Fee Currency' is a valid string
    def test_returns_fee_currency_when_valid_string(self):
        input_row = {'Fee Currency': 'USD'}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_currency() == 'USD'

    # Handles cases where 'Fee Currency' key is missing in the input row
    def test_handles_missing_fee_currency_key(self):
        input_row = {}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_currency() == ''

    # Handles cases where 'Fee Currency' is a numeric value
    def test_handles_numeric_fee_currency(self):
        input_row = {'Fee Currency': 100}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_currency() == ''

    # Handles cases where 'Fee Currency' is a list or dictionary
    def test_handles_list_or_dict_fee_currency(self):
        input_row = {'Fee Currency': ['USD', 'EUR']}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_currency() == ''

    # Returns an empty string when 'Fee Currency' is not a string
    def test_returns_empty_string_when_fee_currency_not_string(self):
        input_row = {'Fee Currency': None}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_currency() == ''

    # Returns an empty string when 'Fee Currency' is None
    def test_returns_empty_string_when_fee_currency_is_none(self):
        input_row = {'Fee Currency': None}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_currency() == ''

    # Handles cases where 'Fee Currency' is a special character string
    def test_handles_special_character_fee_currency(self):
        input_row = {'Fee Currency': '$'}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_currency() == '$'

    # Handles cases where 'Fee Currency' is a very long string
    def test_handles_very_long_fee_currency(self):
        input_row = {'Fee Currency': 'VeryLongFeeCurrencyStringHere'}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_currency() == 'VeryLongFeeCurrencyStringHere'

    # Handles cases where 'Fee Currency' is a whitespace string
    def test_handles_whitespace_fee_currency(self):
        input_row = {'Fee Currency': '   '}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_currency() == ''

    # Handles cases where 'Fee Currency' is an empty string
    def test_handles_empty_fee_currency(self):
        input_row = {'Fee Currency': ''}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_currency() == ''

    # Handles cases where 'Fee Currency' is a boolean value
    def test_handles_boolean_fee_currency(self):
        input_row = {'Fee Currency': True}
        parser = HiParserCsv(input_row)
        assert parser.get_transaction_fee_currency() == ''

class TestGetOrderId:

    # Retrieves 'TxHash' from input_row when it exists and is a string
    def test_retrieves_txhash_when_exists_and_is_string(self):
        input_row = {'TxHash': 'abc123'}
        parser = HiParserCsv(input_row)
        assert parser.get_order_id() == 'abc123'

    # input_row is an empty dictionary
    def test_returns_empty_string_when_input_row_is_empty(self):
        input_row = {}
        parser = HiParserCsv(input_row)
        assert parser.get_order_id() == ''

    # 'TxHash' key is missing in input_row
    def test_txhash_key_missing(self):
        input_row = {}
        parser = HiParserCsv(input_row)
        assert parser.get_order_id() == ""

    # Returns an empty string when 'TxHash' is not a string
    def test_returns_empty_string_when_txhash_not_string(self):
        input_row = {'TxHash': 12345}
        parser = HiParserCsv(input_row)
        assert parser.get_order_id() == ''

    # Returns 'TxHash' as a string when it is valid
    def test_returns_order_id_when_valid_string(self):
        input_row = {'TxHash': 'Tx123'}
        parser = HiParserCsv(input_row)
        assert parser.get_order_id() == 'Tx123'

    # Returns an empty string when 'TxHash' is None
    def test_returns_empty_string_when_txhash_is_none(self):
        input_row = {'TxHash': None}
        parser = HiParserCsv(input_row)
        assert parser.get_order_id() == ''

    # 'TxHash' is a boolean
    def test_txhash_is_boolean(self):
        input_row = {'TxHash': True}
        parser = HiParserCsv(input_row)
        assert parser.get_order_id() == ''

    # 'TxHash' is a list
    def test_txhash_is_list(self):
        input_row = {'TxHash': ['hash1', 'hash2']}
        parser = HiParserCsv(input_row)
        assert parser.get_order_id() == ''

    # 'TxHash' is a nested dictionary
    def test_txhash_nested_dictionary(self):
        input_row = {'TxHash': {'nested_key': 'order123'}}
        parser = HiParserCsv(input_row)
        assert parser.get_order_id() == ''

    # Handles special characters in 'TxHash'
    def test_handles_special_characters_in_txhash(self):
        input_row = {'TxHash': 'abc123!@#'}
        parser = HiParserCsv(input_row)
        assert parser.get_order_id() == 'abc123!@#'

    # Handles large strings as 'TxHash'
    def test_handles_large_strings_as_txhash(self):
        input_row = {'TxHash': 'a' * 1000}  # Creating a large string for TxHash
        parser = HiParserCsv(input_row)
        assert parser.get_order_id() == 'a' * 1000

    # Handles 'TxHash' with leading/trailing spaces
    def test_handles_txhash_with_spaces(self):
        input_row = {'TxHash': '   0x123abc   '}
        parser = HiParserCsv(input_row)
        assert parser.get_order_id() == '0x123abc'

    # Handles 'TxHash' with unicode characters
    def test_handles_txhash_with_unicode_characters(self):
        input_row = {'TxHash': '0x123abc\u0394'}
        parser = HiParserCsv(input_row)
        assert parser.get_order_id() == '0x123abc\u0394'

class TestGetDescription:

    # Returns the description if 'Description' key exists and is a non-empty string
    def test_returns_description_when_key_exists_and_is_non_empty_string(self):
        input_row = {'Description': 'Transaction details'}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == 'Transaction details'

    # Handles input_row with 'Description' key set to None
    def test_handles_input_row_with_description_key_set_to_none(self):
        input_row = {'Description': None}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == ''

    # Returns an empty string if 'Description' key exists but is an empty string
    def test_returns_empty_string_when_description_key_empty(self):
        input_row = {'Description': ''}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == ''

    # Returns an empty string if 'Description' key exists but is not a string
    def test_returns_empty_string_when_description_not_string(self):
        input_row = {'Description': 12345}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == ''

    # Returns an empty string if 'Description' key does not exist
    def test_returns_empty_string_when_description_key_does_not_exist(self):
        input_row = {'Amount': 100, 'Date': '2022-01-01'}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == ''

    # Handles input_row with 'Description' key set to an integer
    def test_handles_description_key_integer(self):
        input_row = {'Description': 123}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == ""

    # Handles input_row with 'Description' key set to a dictionary
    def test_handles_description_key_as_dictionary(self):
        input_row = {'Description': {'details': 'Transaction details'}}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == ''

    # Handles input_row with 'Description' key set to a list
    def test_handles_description_key_as_list(self):
        input_row = {'Description': ['Detailed description']}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == ''

    # Handles input_row with 'Description' key set to a boolean
    def test_handles_description_key_boolean(self):
        input_row = {'Description': True}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == ""

    # Handles input_row with 'Description' key set to a float
    def test_handles_description_key_with_float(self):
        input_row = {'Description': 123.45}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == ""

    # Handles input_row with 'Description' key set to a very long string
    def test_handles_long_description(self):
        input_row = {'Description': 'A very long description that exceeds the normal length limit'}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == 'A very long description that exceeds the normal length limit'

    # Handles input_row with 'Description' key set to a string with special characters
    def test_handles_description_with_special_characters(self):
        input_row = {'Description': 'Special !@#$%^&*()_+ Characters'}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == 'Special !@#$%^&*()_+ Characters'

    # Handles input_row with 'Description' key set to a string with only whitespace
    def test_handles_description_with_whitespace(self):
        input_row = {'Description': '   '}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == ''

    # Handles input_row with 'Description' key set to a string with newline characters
    def test_handles_description_with_newline_characters(self):
        input_row = {'Description': 'This is a description.\nIt has a newline character.'}
        parser = HiParserCsv(input_row)
        assert parser.get_description() == 'This is a description.\nIt has a newline character.'

    # Handles input_row with 'Description' key set to a string with mixed data types
    def test_handles_mixed_data_types(self):
        input_row = {'Description': 123}  # Integer instead of string
        parser = HiParserCsv(input_row)
        assert parser.get_description() == ''
