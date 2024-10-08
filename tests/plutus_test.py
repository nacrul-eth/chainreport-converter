import pytest
from src.chainreport_parser.plutus_parser_csv import PlutusParserCsv

class TestCheckIfSkipLine:

    # Returns False when 'type' is not in input_row
    def test_returns_false_when_type_not_in_input_row(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'reward_plu_value': '10.50',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        with pytest.raises(KeyError):
            parser.check_if_skip_line()


    # Handles input_row with 'type' as None gracefully
    def test_handles_type_as_none_gracefully(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'reward_plu_value': '10.50',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890',
            'type': None
        }
        parser = PlutusParserCsv(row)
        with pytest.raises(KeyError):
            parser.check_if_skip_line()

    # Handles input_row with 'type' containing only whitespace
    def test_handles_input_row_with_type_containing_only_whitespace(self):
        row = {'type': '   '}
        parser = PlutusParserCsv(row)
        assert parser.check_if_skip_line() == True

    # Handles input_row with 'type' as a very long string
    def test_handles_long_string_type(self):
        row = {'type': 'very_long_string_type_to_test_handling_skip'}
        parser = PlutusParserCsv(row)
        assert parser.check_if_skip_line() == False

    # Handles input_row with 'type' as a special character string
    def test_handles_special_character_string(self):
        row = {'type': '!@#$%^&*()'}
        parser = PlutusParserCsv(row)
        assert parser.check_if_skip_line() == False

    # Handles input_row with additional unexpected keys
    def test_handles_input_row_with_additional_unexpected_keys(self):
        row = {
            'type': 'TRANSFER',
            'amount': '100.00',
            'description': 'Transfer from A to B'
        }
        parser = PlutusParserCsv(row)
        parser.SKIPSTRINGS = ['TRANSFER']
        assert parser.check_if_skip_line() is True

class TestGetInputString:

    # Returns the input row as is
    def test_returns_input_row_as_is(self):
        input_row = {
            'createdAt': '2023-10-01T12:00:00.000Z',
            'reward_plu_value': '10.0',
            'statement_id': '12345',
            'description': 'Test description',
            'type': 'DAILY_REBATE_DISTRIBUTION'
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with missing fields
    def test_handles_input_row_with_missing_fields(self):
        input_row = {
            'createdAt': '2023-10-01T12:00:00.000Z',
            'reward_plu_value': '10.0',
            'statement_id': '12345'
            # Missing 'description' and 'type'
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles typical input row with standard fields
    def test_handles_typical_input_row_with_standard_fields(self):
        input_row = {
            'createdAt': '2023-10-01T12:00:00.000Z',
            'reward_plu_value': '10.0',
            'statement_id': '12345',
            'description': 'Test description',
            'type': 'DAILY_REBATE_DISTRIBUTION'
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Works with input row containing all expected keys
    def test_works_with_input_row_containing_all_expected_keys(self):
        input_row = {
            'createdAt': '2023-10-01T12:00:00.000Z',
            'reward_plu_value': '10.0',
            'statement_id': '12345',
            'description': 'Test description',
            'type': 'DAILY_REBATE_DISTRIBUTION'
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with typical string values
    def test_handles_input_row_with_typical_string_values(self):
        input_row = {
            'createdAt': '2023-10-01T12:00:00.000Z',
            'reward_plu_value': '10.0',
            'statement_id': '12345',
            'description': 'Test description',
            'type': 'DAILY_REBATE_DISTRIBUTION'
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with typical numeric values
    def test_handles_input_row_with_typical_numeric_values(self):
        input_row = {
            'createdAt': '2023-10-01T12:00:00.000Z',
            'reward_plu_value': '10.0',
            'statement_id': '12345',
            'description': 'Test description',
            'type': 'DAILY_REBATE_DISTRIBUTION'
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with extra unexpected fields
    def test_handles_input_row_with_extra_unexpected_fields(self):
        input_row = {
            'createdAt': '2023-10-01T12:00:00.000Z',
            'reward_plu_value': '10.0',
            'statement_id': '12345',
            'description': 'Test description',
            'type': 'DAILY_REBATE_DISTRIBUTION',
            'extra_field': 'unexpected'
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with empty strings
    def test_handles_input_row_with_empty_strings(self):
        input_row = {
            'createdAt': '',
            'reward_plu_value': '',
            'statement_id': '',
            'description': '',
            'type': ''
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with null values
    def test_handles_input_row_with_null_values(self):
        input_row = {
            'createdAt': None,
            'reward_plu_value': None,
            'statement_id': None,
            'description': None,
            'type': None
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with mixed data types
    def test_handles_input_row_with_mixed_data_types(self):
        input_row = {
            'createdAt': '2023-10-01T12:00:00.000Z',
            'reward_plu_value': '10.0',
            'statement_id': '12345',
            'description': 'Test description',
            'type': 'DAILY_REBATE_DISTRIBUTION'
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with special characters
    def test_handles_input_row_with_special_characters(self):
        input_row = {
            'createdAt': '2023-10-01T12:00:00.000Z',
            'reward_plu_value': '10.0',
            'statement_id': '12345',
            'description': 'Special characters: !@#$%^&*()_+',
            'type': 'DAILY_REBATE_DISTRIBUTION'
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with boolean values
    def test_handles_input_row_with_boolean_values(self):
        input_row = {
            'createdAt': '2023-10-01T12:00:00.000Z',
            'reward_plu_value': '10.0',
            'statement_id': '12345',
            'description': True,
            'type': 'DAILY_REBATE_DISTRIBUTION'
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with nested dictionaries
    def test_handles_input_row_with_nested_dictionaries(self):
        input_row = {
            'createdAt': '2023-10-01T12:00:00.000Z',
            'reward_plu_value': '10.0',
            'statement_id': '12345',
            'description': 'Test description',
            'type': 'DAILY_REBATE_DISTRIBUTION',
            'nested_data': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with large data sets
    def test_handles_input_row_with_large_data_sets(self):
        input_row = {
            'createdAt': '2023-10-01T12:00:00.000Z',
            'reward_plu_value': '10.0',
            'statement_id': '12345',
            'description': 'Test description',
            'type': 'DAILY_REBATE_DISTRIBUTION'
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

    # Handles input row with date-time objects
    def test_handles_input_row_with_date_time_objects(self):
        input_row = {
            'createdAt': '2023-10-01T12:00:00.000Z',
            'reward_plu_value': '10.0',
            'statement_id': '12345',
            'description': 'Test description',
            'type': 'DAILY_REBATE_DISTRIBUTION'
        }
        parser = PlutusParserCsv(input_row)
        assert parser.get_input_string() == input_row

class TestGetDateString:

    # correctly parses a valid date string in the expected format
    def test_correctly_parses_valid_date_string(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_date_string() == '01.01.2023 12:00'

    # handles missing 'createdAt' field gracefully
    def test_handles_missing_createdAt_field(self):
        row = {
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        with pytest.raises(KeyError):
            parser.get_date_string()

    # handles typical date and time values accurately
    def test_handles_typical_date_and_time_values(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_date_string() == '01.01.2023 12:00'

    # processes input rows with standard datetime format correctly
    def test_processes_input_rows_with_standard_datetime_format_correctly(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_date_string() == '01.01.2023 12:00'

    # raises an error for malformed date strings
    def test_raises_error_for_malformed_date_strings(self):
        row = {
            'createdAt': 'malformed date',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        with pytest.raises(ValueError):
            parser.get_date_string()

    # processes dates with different time zones correctly
    def test_processes_dates_with_different_time_zones_correctly(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_date_string() == '01.01.2023 12:00'

    # handles leap year dates accurately
    def test_handles_leap_year_dates(self):
        row = {
            'createdAt': '2024-02-29T12:00:00.000Z',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_date_string() == '29.02.2024 12:00'

    # processes dates with milliseconds correctly
    def test_processes_dates_with_milliseconds_correctly(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.123Z',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_date_string() == '01.01.2023 12:00'

    # ensures the output format is always consistent
    def test_output_format_consistent(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_date_string() == '01.01.2023 12:00'

    # handles dates at the boundary of months and years correctly
    def test_handles_dates_at_boundary_of_months_and_years_correctly(self):
        row = {
            'createdAt': '2023-01-31T23:59:59.999Z',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_date_string() == '31.01.2023 23:59'

    # processes dates with single-digit days and months correctly
    def test_processes_single_digit_dates_correctly(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_date_string() == '01.01.2023 12:00'

    # handles dates with different separators in the input
    def test_handles_dates_with_different_separators(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_date_string() == '01.01.2023 12:00'

    # ensures no side effects or state changes in the method
    def test_no_side_effects_or_state_changes(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        initial_input_row = parser.get_input_string()
        initial_date_string = parser.get_date_string()
    
        # Call the method again
        second_date_string = parser.get_date_string()
    
        assert initial_input_row == row
        assert initial_date_string == '01.01.2023 12:00'
        assert second_date_string == initial_date_string

class TestGetTransactionType:

    # Returns 'Cashback' for 'DAILY_REBATE_DISTRIBUTION' type
    def test_returns_cashback_for_daily_rebate_distribution(self):
        row = {
            'type': 'DAILY_REBATE_DISTRIBUTION',
            'createdAt': '2022-01-01T12:34:56.789Z',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890',
            'description': 'Daily rebate distribution'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_transaction_type() == 'Cashback'

    # Handles missing 'type' key in input_row gracefully
    def test_handles_missing_type_key_gracefully(self):
        row = {
            'createdAt': '2022-01-01T12:34:56.789Z',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890',
            'description': 'Daily rebate distribution'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Returns 'ERROR' for unknown transaction types
    def test_returns_error_for_unknown_transaction_types(self):
        row = {
            'type': 'UNKNOWN_TYPE',
            'createdAt': '2022-01-01T12:34:56.789Z',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890',
            'description': 'Unknown transaction type'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Correctly identifies transaction type when input_row has valid 'type' key
    def test_correctly_identifies_transaction_type_with_valid_type_key(self):
        row = {
            'type': 'REBATE_BONUS',
            'createdAt': '2022-01-01T12:34:56.789Z',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890',
            'description': 'Rebate bonus'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_transaction_type() == 'Cashback'

    # Handles empty string as transaction type
    def test_handles_empty_string_as_transaction_type(self):
        row = {
            'type': '',
            'createdAt': '2022-01-01T12:34:56.789Z',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890',
            'description': 'Daily rebate distribution'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Handles None as transaction type
    def test_handles_none_as_transaction_type(self):
        row = {
            'type': None,
            'createdAt': '2022-01-01T12:34:56.789Z',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890',
            'description': 'Daily rebate distribution'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Handles unexpected data types for transaction type (e.g., integer, list)
    def test_handles_unexpected_data_types_for_transaction_type(self):
        row = {
            'type': 123,  # unexpected data type
            'createdAt': '2022-01-01T12:34:56.789Z',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890',
            'description': 'Daily rebate distribution'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Handles case sensitivity in transaction type descriptions
    def test_handles_case_sensitivity_in_transaction_type_descriptions(self):
        row = {
            'type': 'daily_rebate_distribution',
            'createdAt': '2022-01-01T12:34:56.789Z',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890',
            'description': 'Daily rebate distribution'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_transaction_type() == 'Cashback'

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
        parser = PlutusParserCsv(row)
        assert parser.get_transaction_type() == 'Cashback'

    # Handles input_row with special characters in 'type'
    def test_handles_special_characters_in_type(self):
        row = {
            'type': 'SPECIAL_CHARACTER$',
            'createdAt': '2022-01-01T12:34:56.789Z',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890',
            'description': 'Special character type'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

    # Handles input_row with whitespace around 'type'
    def test_handles_whitespace_around_type(self):
        row = {
            'type': '   DAILY_REBATE_DISTRIBUTION   ',
            'createdAt': '2022-01-01T12:34:56.789Z',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890',
            'description': 'Daily rebate distribution'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_transaction_type() == 'Cashback'

    # Handles input_row with mixed case 'type' values
    def test_handles_mixed_case_type_values(self):
        row = {
            'type': 'DaILy_ReBaTe_DiStRiBuTiOn',
            'createdAt': '2022-01-01T12:34:56.789Z',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890',
            'description': 'Daily rebate distribution'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_transaction_type() == 'Cashback'

    # Handles input_row with numeric strings as 'type'
    def test_handles_numeric_strings_as_type(self):
        row = {
            'type': '123',
            'createdAt': '2022-01-01T12:34:56.789Z',
            'reward_plu_value': '10.00',
            'statement_id': '1234567890',
            'description': 'Numeric type'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_transaction_type() == 'ERROR'

class TestGetReceivedAmount:

    # correctly parses and returns the received amount with a comma as decimal separator
    def test_correctly_parses_received_amount(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'amount': '10.50',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_received_amount() == "10,50"

    # handles input row where 'reward_plu_value' is an empty string
    def test_handles_empty_reward_plu_value(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'reward_plu_value': '',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_received_amount() == ""

    # handles typical input row with valid 'reward_plu_value'
    def test_handles_typical_input_row(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'reward_plu_value': '10.50',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_received_amount() == "10,50"

    # processes input rows with different valid numerical values for 'reward_plu_value'
    def test_processes_input_rows_with_different_values(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'reward_plu_value': '5.75',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_received_amount() == "5,75"

    # processes input row where 'reward_plu_value' contains only a decimal point
    def test_processes_input_row_with_decimal_point(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'reward_plu_value': '.25',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_received_amount() == ",25"

    # handles input row where 'reward_plu_value' is missing
    def test_missing_received_amount(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        with pytest.raises(KeyError):
            parser.get_received_amount()

    # processes input row where 'reward_plu_value' is a very large number
    def test_large_received_amount(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'reward_plu_value': '1000000000000000000000000000000000000000000000000000000000000000',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_received_amount() == "1000000000000000000000000000000000000000000000000000000000000000"

    # handles input row where 'reward_plu_value' is a negative number
    def test_handles_negative_received_amount(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'reward_plu_value': '-10.50',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_received_amount() == "-10,50"

    # verifies that 'reward_plu_value' with leading or trailing spaces is trimmed and processed correctly
    def test_handles_leading_trailing_spaces(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'reward_plu_value': '  10.50  ',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_received_amount() == "10,50"

    # checks if 'reward_plu_value' with special characters is handled or raises an error
    def test_handles_special_characters_in_received_amount(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'reward_plu_value': '10.50',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_received_amount() == "10,50"

    # verifies that 'reward_plu_value' with different locale-specific formats is handled correctly
    def test_handles_locale_specific_formats(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'reward_plu_value': '10.50',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_received_amount() == "10,50"

class TestGetOrderId:

    # Returns 'statement_id' when present in input_row
    def test_returns_statement_id_when_present(self):
        input_row = {'statement_id': '12345'}
        parser = PlutusParserCsv(input_row)
        assert parser.get_order_id() == '12345'

    # Handles input_row with additional unexpected keys gracefully
    def test_handles_unexpected_keys_gracefully(self):
        input_row = {'unexpected_key': 'value', 'statement_id': '67890'}
        parser = PlutusParserCsv(input_row)
        assert parser.get_order_id() == '67890'

    # Processes input_row with only 'exchange_rate_id' correctly
    def test_processes_input_row_with_only_exchange_rate_id_correctly(self):
        row = {
            'exchange_rate_id': '9876543210'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_order_id() == '9876543210'

    # Returns an empty string when neither 'statement_id' nor 'exchange_rate_id' are present
    def test_returns_empty_string_when_neither_statement_id_nor_exchange_rate_id_present(self):
        input_row = {}
        parser = PlutusParserCsv(input_row)
        with pytest.raises(KeyError):
            parser.get_order_id()

    # Processes input_row with mixed data types for keys
    def test_processes_mixed_data_types(self):
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'reward_plu_value': 10.50,
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '0987654321'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_order_id() == "0987654321"

    # Handles large input_row dictionaries efficiently
    def test_handles_large_input_row(self):
        row = {
            'statement_id': '1234567890',
            'test_key': '9876543210',
            'other_key': 'other_value'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_order_id() == '1234567890'

    # Processes input_row with nested dictionaries
    def test_processes_input_row_with_nested_dictionaries(self):
        row = {
            'statement_id': '1234567890',
            'original_transaction_id': '0987654321'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_order_id() == '1234567890'

    # Handles input_row with non-string values for 'statement_id' and 'exchange_rate_id'
    def test_handles_non_string_values(self):
        row = {
            'statement_id': 123,  # non-string value
            'other_string': 456  # non-string value
        }
        parser = PlutusParserCsv(row)
        assert parser.get_order_id() == ''

class TestGetDescription:

    # Returns 'clean_description' when present in input_row
    def test_returns_clean_description(self):
        row = {
            'clean_description': 'Transaction for groceries',
            'description': 'Grocery shopping'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_description() == 'Transaction for groceries'

    # Raises KeyError if neither 'clean_description' nor 'description' is present
    def test_raises_key_error_when_no_description(self):
        row = {}
        parser = PlutusParserCsv(row)
        with pytest.raises(KeyError, match="missing clean_description or description"):
            parser.get_description()

    # Handles input_row with empty strings for 'clean_description' and 'description'
    def test_handles_empty_strings(self):
        row = {
            'clean_description': '',
            'description': ''
        }
        parser = PlutusParserCsv(row)
        assert parser.get_description() == ''

    # Handles input_row with non-string description values by returning an empty string
    def test_handles_non_string_description(self):
        # Prepare
        row = {
            'clean_description': 12345,
            'description': 67890
        }
        parser = PlutusParserCsv(row)
    
        # Assert
        assert parser.get_description() == ''

    # Strips leading and trailing whitespaces from the description
    def test_strips_whitespaces_from_description(self):
        row = {
            'clean_description': '  REBATE_BONUS  ',
            'description': '  Another Description  '
        }
        parser = PlutusParserCsv(row)
        assert parser.get_description() == "REBATE_BONUS"

    # Returns 'description' when 'clean_description' is absent but 'description' is present
    def test_returns_description_when_clean_description_absent(self):
        row = {
            'description': 'Transaction Description',
            'statement_id': '1234567890'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_description() == 'Transaction Description'

    # Handles input_row with both 'clean_description' and 'description' present, prioritizing 'clean_description'
    def test_handles_both_clean_description_and_description(self):
        row = {
            'clean_description': 'Clean Description',
            'description': 'Description'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_description() == 'Clean Description'

    # Handles input_row with 'clean_description' or 'description' containing only whitespace
    def test_handles_whitespace_description(self):
        # Initialize the class object
        row = {
            'clean_description': '   ',
            'description': '  ',
        }
        parser = PlutusParserCsv(row)
        assert parser.get_description() == ''

    # Handles input_row with 'clean_description' or 'description' containing special characters
    def test_handles_special_characters(self):
        row = {
            'clean_description': 'Special !@#$%^&* Characters',
            'description': 'Another Description',
            'amount': '100.00'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_description() == 'Special !@#$%^&* Characters'

    # Handles input_row with 'clean_description' or 'description' containing numeric values
    def test_handles_numeric_description(self):
        row = {
            'clean_description': 12345,
            'description': '98765'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_description() == ""

    # Handles input_row with additional unexpected keys without affecting output
    def test_handles_additional_keys(self):
        # Prepare input row with additional unexpected keys
        row = {
            'createdAt': '2023-01-01T12:00:00.000Z',
            'reward_plu_value': '10.50',
            'description': 'DAILY_REBATE_DISTRIBUTION',
            'statement_id': '1234567890',
            'unexpected_key1': 'value1',
            'unexpected_key2': 'value2'
        }
        parser = PlutusParserCsv(row)
        assert parser.get_description() == "DAILY_REBATE_DISTRIBUTION"
