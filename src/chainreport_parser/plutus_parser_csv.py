"""Parser implementation for HI"""

from datetime import datetime
from .chainreport_parser_interface import ChainreportParserInterface

class PlutusParserCsv(ChainreportParserInterface):
    """Extract all required information from Plutus Rewards file."""

    def __init__(self, row):
        """
        Initialize PlutusParserCsv instance with input row data.

        Parameters:
        -----------
        row : dict
            A dictionary containing transaction data. The keys and values represent the transaction details.

        Returns:
        -----------
        None
        """
        self.input_row = row

    NAME = __qualname__
    DELIMITER="|"
    SKIPINITIALLINES=0
    CASHBACKTRANSACTION = ['DAILY_REBATE_DISTRIBUTION',
                           'REBATE_BONUS']   # user for manual rebates (positive & negative)
    DEPOSITTRANSACTION = []
    STAKINGTRANSACTION = []
    WITHDRAWTRANSACTION = []
    SKIPSTRINGS = []
    REFERRALSTRING = []
    TRADETRANSACTION = []
    PAYMENTTRANSACTION = []
    AIRDROPTRANSACTION = []
    CANCELTRANSACTION = []

    def check_if_skip_line(self) -> bool:
        """
        Check if the transaction line should be skipped based on certain conditions.

        This function checks if the transaction line should be skipped based on the 'type' field in the input row.
        If the 'type' field is not present in the input row, the function returns False.
        If the 'type' field is present, the function checks if its value (after stripping leading/trailing whitespaces)
        is in the list of SKIPSTRINGS or if it is an empty string.
        If either condition is met, the function returns True.
        Otherwise, the function returns False.

        Parameters:
        -----------
        None

        Returns:
        -----------
        bool: True if the transaction line should be skipped, False otherwise.
        """
        if 'type' not in self.input_row or self.input_row['type'] is None:
            raise KeyError("missing required field 'type'")
        if (self.input_row.get('type', 'ERROR').strip() in self.SKIPSTRINGS or
                self.input_row.get('type', 'ERROR').strip() == ""):
            return True
        return False

    def get_input_string(self) -> str:
        """
        Retrieve the input data used for parsing.

        This function returns the input data that was provided during the initialization
        of the PlutusParserCsv instance.
        The input data is a dictionary containing transaction details.

        Parameters:
        -----------
        None

        Returns:
        -----------
        dict: A dictionary containing transaction data. The keys and values represent the transaction details.
        """
        return self.input_row

    def get_date_string(self) -> str:
        """
        Retrieve the date and time of the transaction in Chainreport format.

        This function extracts the date and time from the input row, which contains transaction data.
        It checks for two possible keys: 'createdAt' and 'date'.
        If 'createdAt' is present, it assumes the date and time are in ISO 8601 format and
        converts it to the desired format.
        If 'createdAt' is not present but 'date' is present,
        it tries to convert the date and time to the desired format.
        If neither 'createdAt' nor 'date' is present, it returns an empty string.

        Parameters:
        -----------
        None

        Returns:
        -----------
        str: The date and time of the transaction in the format 'dd.mm.yyyy hh:mm'.
             If 'createdAt' or 'date' is not present, returns an empty string.
        """
        if 'createdAt' in self.input_row:
            transaction_time = datetime.strptime(self.input_row['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
            return transaction_time.strftime('%d.%m.%Y %H:%M')
        raise KeyError("missing required field 'createdAt'")

    def get_transaction_type(self) -> str:
        """
        Retrieve the transaction type in Chainreport format.

        This function extracts the transaction type from the input row and converts it to the required format.
        It checks the 'type' field in the input row and compares it with the list of cashback transaction types.

        Parameters:
        -----------
        None

        Returns:
        -----------
        str: The transaction type in Chainreport format. If the transaction type is found in the
             cashback transaction types, it returns 'Cashback'. Otherwise, it returns 'ERROR'.
        """
        transaction_description = self.input_row.get('type', 'ERROR')
        if isinstance(transaction_description, str):
            transaction_description = transaction_description.upper().strip()
            if transaction_description in PlutusParserCsv.CASHBACKTRANSACTION:
                return 'Cashback'
        return 'ERROR'

    def get_received_amount(self) -> str:
        """
        Retrieve the amount of received coins from the transaction data.

        This function extracts the amount of received coins from the input row, which contains transaction data.
        It checks for two possible keys: 'reward_plu_value' and 'plu_amount'.
        If 'reward_plu_value' is present, it assigns its value to 'receive_amount'.
        If 'reward_plu_value' is not present but 'plu_amount' is present, it assigns its value to 'receive_amount'.
        If neither 'reward_plu_value' nor 'plu_amount' is present,
        it raises a KeyError with the message 'reward_plu_value'.
        After assigning the value to 'receive_amount',
        it checks if it is a string and removes any leading/trailing whitespaces.
        Finally, it replaces any decimal points with commas and returns the 'receive_amount'.

        Parameters:
        -----------
        None

        Returns:
        -----------
        str: The amount of received coins, formatted with commas as decimal separators.
        """
        receive_amount = None
        if 'amount' in self.input_row:
            receive_amount = self.input_row.get('amount', None)
        elif 'reward_plu_value' in self.input_row:
            receive_amount = self.input_row.get('reward_plu_value', None)
        if receive_amount is None:
            raise KeyError("missing amount or reward_plu_value")
        if isinstance(receive_amount, str):
            receive_amount = receive_amount.strip()
        receive_amount = receive_amount.replace(".", ",")
        return receive_amount

    def get_received_currency(self) -> str:
        """Return currency of receveid coins"""
        return "PLU"

    def get_sent_amount(self) -> str:
        """Return amount of sent coins"""
        return ""

    def get_sent_currency(self) -> str:
        """Return currency of sent coins"""
        return ""

    def get_transaction_fee_amount(self) -> str:
        """Return amount of transaction fee coins"""
        return ""

    def get_transaction_fee_currency(self) -> str:
        """Return currency of transaction fee coins"""
        return ""

    def get_order_id(self) -> str:
        """
        Retrieve the order ID from the transaction data.

        This function extracts the order ID from the input row, which contains transaction details.
        It checks for two possible keys: 'statement_id' and 'exchange_rate_id'.
        If 'statement_id' is present, it assigns its value to 'order_id'.
        If 'statement_id' is not present but 'exchange_rate_id' is present, it assigns its value to 'order_id'.
        If neither 'statement_id' nor 'exchange_rate_id' is present,
        it raises a KeyError with the message 'missing statement_id or exchange_rate_id'.
        After assigning the value to 'order_id',
        it checks if it is a string and removes any leading/trailing whitespaces.
        Finally, it returns the 'order_id'.

        Parameters:
        -----------
        None

        Returns:
        -----------
        str: The order ID of the transaction. If 'statement_id' or 'exchange_rate_id' is not present,
             raises a KeyError.
        """
        order_id = None
        if 'statement_id' in self.input_row:
            order_id = self.input_row.get('statement_id', '')
        elif 'exchange_rate_id' in self.input_row:
            order_id = self.input_row.get('exchange_rate_id','')
        if order_id is None:
            raise KeyError("missing statement_id or exchange_rate_id")
        if isinstance(order_id, str):
            order_id = order_id.strip()
        else:
            order_id = ''
        return order_id

    def get_description(self) -> str:
        """
        Return description of the transaction.

        This function retrieves the description of the transaction from the input row.
        It checks for the 'reference_type' and 'description' keys in the input row.
        If 'reference_type' is present, it returns the value of 'reference_type'.
        If 'reference_type' is not present but 'description' is present, it returns the value of 'description'.
        If neither 'reference_type' nor 'description' is present, it returns an empty string.

        Parameters:
        -----------
        None

        Returns:
        -----------
        str: The description of the transaction. If 'reference_type' or 'description' is not present,
             returns an empty string.
        """
        description = None
        if 'reference_type' in self.input_row:
            description  = self.input_row.get('reference_type','')
        elif 'description' in self.input_row:
            description = self.input_row.get('description','')
        if description is None:
            raise KeyError("missing reference_type or description")
        if isinstance(description, str):
            description = description.strip()
        else:
            description = ''
        return description
