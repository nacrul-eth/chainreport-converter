"""Parser implementation for Coinbase export file."""

from datetime import datetime
from .chainreport_parser_interface import ChainreportParserInterface

class CoinbaseParserCsv(ChainreportParserInterface):
    """Extract all required information from Coinbase export file."""

    def __init__(self, row):
        self.input_row = row
        self.date = datetime.strptime(self.input_row['Timestamp'], '%Y-%m-%d %H:%M:%S UTC')
        self.received_amount = self.input_row['Quantity Transacted'].replace(".", ",")
        self.received_currency = self.input_row['Asset']
        self.sent_amount = self.input_row['Subtotal'].replace(".", ",")
        self.sent_currency = self.input_row['Price Currency']
        self.fee_amount = self.input_row['Fees and/or Spread'].replace(".", ",")
        self.fee_currency = self.input_row['Price Currency']
        self.order_id = self.input_row['ID']
        self.description = self.input_row['Transaction Type']

    NAME = __qualname__
    DELIMITER=","
    SKIPINITIALLINES=3
    CASHBACKTRANSACTION = []
    DEPOSITTRANSACTION = ['Deposit']
    STAKINGTRANSACTION = ['Staking Income']
    WITHDRAWTRANSACTION = ['Send']
    SKIPSTRINGS = []
    REFERRALSTRING = []
    TRADETRANSACTION = ['Buy']
    PAYMENTTRANSACTION = []
    AIRDROPTRANSACTION = []
    CANCELTRANSACTION = []
    FEETRANSACTION = []
    OTHERINCOMETRANSACTION = ['Receive']

    def check_if_skip_line(self):
        """
        Check if the current transaction line should be skipped based on the transaction type.

        Returns:
        bool: True if the line should be skipped, False otherwise.

        The function checks if the 'Transaction Type' in the input row is present in the 
        'SKIPSTRINGS' list. If it is, the function returns True, indicating that the line should 
        be skipped. Otherwise, it returns False, indicating that the line is relevant.
        """
        return self.input_row['Transaction Type'] in self.SKIPSTRINGS

    def get_input_string(self):
        """
        Return the input data we are using.

        This method retrieves the original input data row that was used to initialize the 
        CoinbaseParserCsv object. The input data is a dictionary where the keys represent 
        the column names from the CSV file and the values represent the corresponding data 
        for that column.

        Parameters:
        None

        Returns:
        dict: The original input data row as a dictionary.
        """
        return self.input_row

    def get_date_string(self):
        """Return datestring in Chainreport format"""
        return self.date.strftime('%d.%m.%Y %H:%M')

    def get_transaction_type(self):
        """Return transaction type in Chainreport format"""
        transaction_description = self.input_row['Transaction Type']
        return_string = 'ERROR'
        if transaction_description in CoinbaseParserCsv.DEPOSITTRANSACTION:
            return_string = 'Deposit'
        if transaction_description in CoinbaseParserCsv.WITHDRAWTRANSACTION:
            return_string = 'Withdrawal'
        if transaction_description in CoinbaseParserCsv.TRADETRANSACTION:
            return_string = 'Trade'
        if transaction_description in CoinbaseParserCsv.OTHERINCOMETRANSACTION:
            return_string = 'Other_Income'
        if transaction_description in CoinbaseParserCsv.STAKINGTRANSACTION:
            return_string = 'Staking'
        return return_string

    def get_received_amount(self):
        """Return amount of received coins"""
        if self.get_transaction_type() == 'Withdrawal':
            return ""
        return self.received_amount

    def get_received_currency(self):
        """Return currency of receveid coins"""
        if self.get_transaction_type() == 'Withdrawal':
            return ""
        return self.received_currency

    def get_sent_amount(self):
        """Return amount of sent coins"""
        if self.get_transaction_type() == 'Trade':
            return "-" + self.sent_amount
        if self.get_transaction_type() == 'Withdrawal':
            return "-" + self.received_amount
        return ""

    def get_sent_currency(self):
        """Return currency of sent coins"""
        if self.get_transaction_type() == 'Trade':
            return self.sent_currency
        if self.get_transaction_type() == 'Withdrawal':
            return self.received_currency
        return ""

    def get_transaction_fee_amount(self):
        """Return amount of transaction fee coins"""
        return self.fee_amount

    def get_transaction_fee_currency(self):
        """Return currency of transaction fee coins"""
        return self.fee_currency

    def get_order_id(self):
        """Return order id of the exchange"""
        return self.order_id

    def get_description(self):
        """Return description of the transaction"""
        return self.description
