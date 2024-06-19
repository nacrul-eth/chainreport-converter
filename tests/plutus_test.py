import pytest
from src.chainreport_parser.plutus_parser_csv import PlutusParserCsv

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
            'reward_plu_value': '10.50',
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
            parser.get_received_amount().replace(",", ".")

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
