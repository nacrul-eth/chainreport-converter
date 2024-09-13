"""Parser implementation for HI"""

from datetime import datetime
from .chainreport_parser_interface import ChainreportParserInterface

class HiParserCsv(ChainreportParserInterface):
    """Extract all required information from Hi statement."""

    def __init__(self, row):
        """
        Initialize the HiParserCsv class with the input row data.

        Parameters:
        -----------
        row : dict
            A dictionary-like object containing the transaction details.
            The dictionary should have keys representing the transaction attributes such as 'Date', 'Description', etc.

        Returns:
        --------
        None
        """
        self.input_row = row

    NAME = __qualname__
    DELIMITER=","
    CASHBACKTRANSACTION = ['HI rebate']
    DEPOSITTRANSACTION = ['Crypto deposit',
                          'crypto receive',
                          'Crypto purchase'] # Missing Euro Amount in CSV from Hi
    STAKINGTRANSACTION = ['Crypto staking yields （HI）']
    WITHDRAWTRANSACTION = ['crypto send',
                       'Crypto withdraw'] # Missing Euro Amount in CSV from Hi
    SKIPSTRINGS = ['Vault HI daily release',
                   'Crypto earning stake',
                   'Crypto earning release',
                   'Card refund',
                   'Card consume',
                   'Fiat deposit（IBAN）',
                   'Fiat withdraw (IBAN)',
                   'Fiat deposit （BankTransfer）',
                   'Yields', 
                   'crypto transfer to trading', 
                   'crypto transfer to flexible']
    REFERRALSTRING = ['HI referrer reward',
                      'HI referrer rebate']
    TRADETRANSACTION = ['buy Vault HI', # 1. Hi splits trade into two lines
                        'buy HI paid',  # 2. Hi splits trade into two lines
                        'Dust to HI']
    PAYMENTTRANSACTION = ['convert'] # Missing Euro Amount in CSV from Hi
    AIRDROPTRANSACTION = []
    CANCELTRANSACTION = ['Crypto cancel withdraw']
    OTHERINCOMETRANSACTION = ['Yields',
                              'crypto cashhash redeem']

    def check_if_skip_line(self) -> bool:
        """
        Check if the transaction line should be skipped based on the description.

        This function is used to determine whether a transaction line should be skipped based on its description.
        The function checks if the description of the transaction is present in the list of SKIPSTRINGS.
        If the description is found in the list, the function returns True, indicating that the line should be skipped.
        Otherwise, the function returns False.
        Parameters:
        -----------
        None

        Returns:
        --------
        bool: True if the line should be skipped, False otherwise.
              The line is considered to be skipped if its description is found in the SKIPSTRINGS list.
        """
        if 'Description' not in self.input_row:
            return False
        if (self.input_row.get('Description', 'ERROR').strip() in self.SKIPSTRINGS or
                self.input_row.get('Description', 'ERROR').strip() == ""):
            return True
        return False

    def get_input_string(self) -> str:
        """
        Return the input data we are using.

        This function retrieves the input data that is used to parse and process the transaction details.
        The input data is expected to be a dictionary-like object containing the transaction details.

        Parameters:
        -----------
        None

        Returns:
        --------
        dict: A dictionary-like object containing the transaction details.
              The dictionary should have keys representing the transaction attributes such as 'Date',
              'Description', etc.
        """
        return self.input_row

    def get_date_string(self) -> str:
        """
        Return datestring in Chainreport format.

        This function takes the transaction date from the input row and converts it into
        the required format for Chainreport.
        The input date is expected to be in the format '%Y-%m-%d %H:%M %Z'.

        Parameters:
        -----------
        None

        Returns:
        --------
        str: The transaction date in the format '%d.%m.%Y %H:%M'.
             This format is suitable for Chainreport and represents the date and time of the transaction.
        """
        if 'Date' not in self.input_row:
            raise KeyError("The 'Date' key is missing in the input row.")
        transaction_datetime = datetime.strptime(self.input_row['Date'], '%Y-%m-%d %H:%M %Z')
        return transaction_datetime.strftime('%d.%m.%Y %H:%M')

    def get_transaction_type(self) -> str:
        """
        Determine and return the transaction type in Chainreport format based on the transaction description.

        Parameters:
        -----------
        None

        Returns:
        --------
        str : The transaction type in Chainreport format.
              If the transaction description matches any of the predefined transaction types,
              the corresponding type is returned. Otherwise, 'ERROR' is returned.
        """
        transaction_description = self.input_row.get('Description', None)
        if transaction_description is not None and isinstance(transaction_description, str):
            transaction_description = transaction_description.strip()

        transaction_types = {
            'Cashback': self.CASHBACKTRANSACTION,
            'Staking': self.STAKINGTRANSACTION,
            'Deposit': self.DEPOSITTRANSACTION,
            'Withdrawal': self.WITHDRAWTRANSACTION,
            'Trade': self.TRADETRANSACTION,
            'Payment': self.PAYMENTTRANSACTION,
            'Airdrop': self.AIRDROPTRANSACTION,
            'Cancel': self.CANCELTRANSACTION,
            'Other income': self.OTHERINCOMETRANSACTION,
            'Referral_Rewards': self.REFERRALSTRING
        }

        for transaction_type, transaction_list in transaction_types.items():
            if transaction_description.lower() in [item.lower() for item in transaction_list]:
                return transaction_type
        return 'ERROR'

    def get_received_amount(self) -> str:
        """
        Retrieve the amount of received coins from the transaction details.

        This function extracts the 'Received Amount' from the input row dictionary and formats it
        to replace the decimal point with a comma, as required for the output.

        Parameters:
        -----------
        None

        Returns:
        --------
        str : The amount of received coins, formatted with a comma as the decimal separator.
              The returned value is a string to maintain consistency with the rest of the class.
        """
        received_amount = self.input_row.get('Received Amount', None)
        if received_amount is not None and isinstance(received_amount, str):
            received_amount = received_amount.strip()
            received_amount = received_amount.replace(".", ",")
            return received_amount
        return ""

    def get_received_currency(self) -> str:
        """
        Retrieve the currency of the received coins from the transaction details.

        This function extracts the 'Received Currency' from the input row dictionary.
        If the 'Received Currency' is present and not None, it is returned as a string.
        If the 'Received Currency' is None or not a string, an empty string is returned.

        Parameters:
        -----------
        None

        Returns:
        --------
        str : The currency of the received coins.
              If the 'Received Currency' is present and not None, it is returned as a string.
              If the 'Received Currency' is None or not a string, an empty string is returned.
        """
        received_currency = self.input_row.get('Received Currency', None)
        if received_currency is not None and isinstance(received_currency, str):
            return received_currency.strip()
        return ""

    def get_sent_amount(self) -> str:
        """
        Retrieve the amount of sent coins from the transaction details.

        This function extracts the 'Sent Amount' from the input row dictionary and formats it
        to replace the decimal point with a comma, as required for the output.

        Parameters:
        -----------
        None

        Returns:
        --------
        str : The amount of sent coins, formatted with a comma as the decimal separator.
              The returned value is a string to maintain consistency with the rest of the class.
              If the 'Sent Amount' is not present in the input row or is None, an empty string is returned.
        """
        sent_amount = self.input_row.get('Sent Amount', None)
        if sent_amount is not None and isinstance(sent_amount, str):
            sent_amount = sent_amount.strip()
            sent_amount = sent_amount.replace(".", ",")
            return sent_amount
        return ""

    def get_sent_currency(self) -> str:
        """
        Retrieve the currency of the sent coins from the transaction details.

        This function extracts the 'Sent Currency' from the input row dictionary.
        If the 'Sent Currency' is present and not None, it is returned as a string.
        If the 'Sent Currency' is None or not a string, an empty string is returned.

        Parameters:
        -----------
        None

        Returns:
        --------
        str : The currency of the sent coins.
              If the 'Sent Currency' is present and not None, it is returned as a string.
              If the 'Sent Currency' is None or not a string, an empty string is returned.
        """
        sent_currency = self.input_row.get('Sent Currency', None)
        if sent_currency is not None and isinstance(sent_currency, str):
            return sent_currency.strip()
        return ""

    def get_transaction_fee_amount(self) -> str:
        """
        Retrieve the transaction fee amount from the input row.

        This function extracts the 'Fee Amount' from the input row dictionary and formats it
        to replace the decimal point with a comma, as required for the output.

        Parameters:
        -----------
        None

        Returns:
        --------
        str : The transaction fee amount, formatted with a comma as the decimal separator.
              The returned value is a string to maintain consistency with the rest of the class.
              If the 'Fee Amount' is not present in the input row or is None, an empty string is returned.
        """
        fee_amount = self.input_row.get('Fee Amount', None)
        if fee_amount is not None and isinstance(fee_amount, str):
            fee_amount = fee_amount.strip()
            fee_amount = fee_amount.replace(".", ",")
            return fee_amount
        return ""

    def get_transaction_fee_currency(self) -> str:
        """
        Retrieve the currency of the transaction fee from the input row.

        This function extracts the 'Fee Currency' from the input row dictionary.
        If the 'Fee Currency' is present and not None, it is returned as a string.
        If the 'Fee Currency' is None or not a string, an empty string is returned.

        Parameters:
        -----------
        None

        Returns:
        --------
        str : The currency of the transaction fee.
              If the 'Fee Currency' is present and not None, it is returned as a string.
              If the 'Fee Currency' is None or not a string, an empty string is returned.
        """
        fee_currency = self.input_row.get('Fee Currency', None)
        if fee_currency is not None and isinstance(fee_currency, str):
            return fee_currency.strip()
        return ""

    def get_order_id(self) -> str:
        """
        Retrieve the order ID of the exchange from the transaction details.

        This function extracts the 'TxHash' (Transaction Hash) from the input row dictionary,
        which is commonly used as the order ID in cryptocurrency exchanges.

        Parameters:
        -----------
        None

        Returns:
        --------
        str : The order ID of the exchange.
              If the 'TxHash' is present and not None, it is returned as a string.
              If the 'TxHash' is None or not a string, an empty string is returned.
        """
        transaction_id = self.input_row.get('TxHash', None)
        if transaction_id is not None and isinstance(transaction_id, str):
            return transaction_id.strip()
        return ""

    def get_description(self) -> str:
        """
        Retrieve the description of the transaction from the input row.

        This function extracts the 'Description' from the input row dictionary,
        which provides a detailed explanation of the transaction.

        Parameters:
        -----------
        None

        Returns:
        --------
        str : The description of the transaction.
              If the 'Description' is present and not None, it is returned as a string.
              If the 'Description' is None or not a string, an empty string is returned.
        """
        transaction_description = self.input_row.get('Description', None)
        if transaction_description is not None and isinstance(transaction_description, str):
            return transaction_description.strip()
        return ""
