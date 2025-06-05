"""Parser implementation for HI"""

from datetime import datetime
from .chainreport_parser_interface import ChainreportParserInterface

class KrakenParserCsv(ChainreportParserInterface):
    """Extract all required information from Plutus Rewards file."""

    def __init__(self, row):
        self.input_row = row

    NAME = __qualname__
    DELIMITER=","
    SKIPINITIALLINES=0
    CASHBACKTRANSACTION = []
    DEPOSITTRANSACTION = ['deposit']
    STAKINGTRANSACTION = []
    WITHDRAWTRANSACTION = ['withdrawal']
    SKIPSTRINGS = ['transfer']
    REFERRALSTRING = []
    TRADETRANSACTION = ['trade']
    PAYMENTTRANSACTION = []
    AIRDROPTRANSACTION = []
    CANCELTRANSACTION = []
    FEETRANSACTION = []

    def check_if_skip_line(self):
        """
        Check if the current transaction line should be skipped based on the transaction type.

        Returns:
        bool: True if the line should be skipped, False otherwise.

        The method checks if the transaction type is present in the list of SKIPSTRINGS.
        If it is, the method returns True, indicating that the line should be skipped.
        Otherwise, it returns False, indicating that the line is relevant.

        Parameters:
        None

        Raises:
        None
        """
        if 'type' not in self.input_row:
            return False
        if self.input_row.get('type', 'ERROR') in self.SKIPSTRINGS:
            return True
        return False

    def get_input_string(self):
        """
        Return the input data we are using.

        This method returns the original data row that was passed to the parser during initialization.
        This data can be used for further processing or debugging purposes.

        Parameters:
        None

        Returns:
        dict: The original data row that was passed to the parser during initialization.
        """
        return self.input_row

    def get_date_string(self) -> str:
        """
        Return datestring in Chainreport format.

        This method takes the date and time from the input row, converts it to a datetime object,
        and then formats it according to the required Chainreport format.

        Parameters:
        None

        Returns:
        str: The date and time in the format 'dd.mm.yyyy hh:mm'

        Raises:
        ValueError: If the date and time format in the input row does not match the expected format.
        """
        if 'time' not in self.input_row:
            raise KeyError("The 'time' key is missing in the input row.")
        date = datetime.strptime(self.input_row['time'], '%Y-%m-%d %H:%M:%S')

        return date.strftime('%d.%m.%Y %H:%M')

    def get_transaction_type(self) -> str:
        """
        Return transaction type in Chainreport format.

        This method takes the transaction description from the input row,
        and maps it to the corresponding transaction type in the Chainreport format.
        The transaction types are defined in the class attributes DEPOSITTRANSACTION,
        WITHDRAWTRANSACTION, and TRADETRANSACTION.

        Parameters:
        None

        Returns:
        str: The transaction type in the Chainreport format.
            Returns 'ERROR' if the transaction description is not found in any of the defined lists.

        """
        transaction_description = self.input_row.get('type', None)
        if transaction_description is not None and isinstance(transaction_description, str):
            transaction_description = transaction_description.strip().lower()

        transaction_types = {
            'Deposit': self.DEPOSITTRANSACTION,
            'Withdrawal': self.WITHDRAWTRANSACTION,
            'Trade': self.TRADETRANSACTION
        }
        for transaction_type, transaction_list in transaction_types.items():
            if transaction_description in transaction_list:
                return transaction_type
        return 'ERROR'

    def get_received_amount(self) -> str:
        """
        Return the amount of received coins.

        The method calculates the received amount based on the transaction type and the amount in the input row.
        It replaces the decimal point with a comma for consistency with the Chainreport format.

        Parameters:
        None

        Returns:
        str: The received amount in the format 'x,xx'.
            Returns an empty string if the transaction type is 'Withdrawal' or 
            if the transaction type is 'Trade' and the received amount is negative.
        """
        received_amount = self.input_row.get('amount', None)
        if received_amount is not None and isinstance(received_amount, str):
            received_amount = received_amount.strip()
            received_amount = received_amount.replace(".", ",")

            if self.get_transaction_type() == 'Withdrawal':
                return ""
            elif self.get_transaction_type() == 'Trade' and received_amount.startswith("-"):
                return ""
            return received_amount
        return ""

    def get_received_currency(self) -> str:
        """
        Return the currency of received coins.

        This method retrieves the currency of received coins from the input row.
        It checks the transaction type and returns an empty string if the transaction type is 'Withdrawal'
        or if the transaction type is 'Trade' and the received amount is negative.

        Parameters:
        None

        Returns:
        str: The currency of received coins.
            Returns an empty string if the transaction type is 'Withdrawal' or if the transaction type is 'Trade' and the received amount is negative.

        """
        received_amount = self.get_received_amount()
        received_currency = self.input_row.get('asset', None)
        if received_currency is not None and received_amount is not None and isinstance(received_currency, str):
            if self.get_transaction_type() == 'Withdrawal':
                return ""
            # TODO: Check if the received amount is negative (indicating a deposit) and return an empty string
            if self.get_transaction_type() == 'Trade' and received_amount == "":
                return ""
            return received_currency
        return ""

    def get_sent_amount(self):
        """
        Return the amount of sent coins.

        This method calculates the sent amount based on the transaction type and the amount in the input row.
        It replaces the decimal point with a comma for consistency with the Chainreport format.
        If the transaction type is 'Deposit', an empty string is returned.
        If the transaction type is 'Trade' and the sent amount is not negative (indicating a deposit), an empty string is returned.

        Parameters:
        None

        Returns:
        str: The sent amount in the format 'x,xx'.
            Returns an empty string if the transaction type is 'Deposit' or if the transaction type is 'Trade' and the sent amount is not negative.
        """
        sent_amount = self.input_row['amount'].replace(".", ",")

        if self.get_transaction_type() == 'Deposit':
            return ""
        if self.get_transaction_type() == 'Trade' and not sent_amount.startswith("-"):
            return ""
        return sent_amount

    def get_sent_currency(self):
        """
        Return the currency of sent coins.

        This method calculates the currency of sent coins based on the transaction type and the input row.
        It checks the transaction type and returns an empty string if the transaction type is 'Deposit'
        or if the transaction type is 'Trade' and the sent amount is not negative (indicating a deposit).

        Parameters:
        None

        Returns:
        str: The currency of sent coins.
            Returns an empty string if the transaction type is 'Deposit' or if the transaction type is 'Trade' and the sent amount is not negative.
        """
        sent_amount = self.input_row['amount'].replace(".", ",")
        sent_currency = self.input_row['asset']

        if self.get_transaction_type() == 'Deposit':
            return ""
        if self.get_transaction_type() == 'Trade' and not sent_amount.startswith("-"):
            return ""
        return sent_currency

    def get_transaction_fee_amount(self):
        """
        Return the amount of transaction fee coins.

        This method retrieves the transaction fee amount from the input row,
        and replaces the decimal point with a comma for consistency with the Chainreport format.

        Parameters:
        None

        Returns:
        str: The transaction fee amount in the format 'x,xx'.

        Raises:
        KeyError: If the 'fee' key is not present in the input row.
        """
        fee_amount = self.input_row['fee'].replace(".", ",")

        return fee_amount

    def get_transaction_fee_currency(self):
        """
        Return the currency of transaction fee coins.

        This method retrieves the currency of transaction fee from the input row.
        The currency is extracted from the 'asset' key in the input row.

        Parameters:
        None

        Returns:
        str: The currency of transaction fee coins.

        Raises:
        KeyError: If the 'asset' key is not present in the input row.
        """
        fee_currency = self.input_row['asset']

        return fee_currency

    def get_order_id(self):
        """
        Return order id of the exchange.

        This method retrieves the order id from the input row, which is assumed to be a dictionary.
        The order id is expected to be present in the 'txid' key of the input row.

        Parameters:
        None

        Returns:
        str: The order id of the exchange.

        Raises:
        KeyError: If the 'txid' key is not present in the input row.
        """
        order_id = self.input_row['txid']

        return order_id

    def get_description(self):
        """
        Return description of the transaction.

        This method retrieves the description of the transaction from the input row.
        The description is expected to be present in the 'type' key of the input row.

        Parameters:
        None

        Returns:
        str: The description of the transaction.

        Raises:
        KeyError: If the 'type' key is not present in the input row.
        """
        description = self.input_row['type']

        return description
