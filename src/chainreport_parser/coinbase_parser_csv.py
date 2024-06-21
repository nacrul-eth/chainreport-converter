"""Parser implementation for Coinbase export file."""

from datetime import datetime
from .chainreport_parser_interface import ChainreportParserInterface

class CoinbaseParserCsv(ChainreportParserInterface):
    """Extract all required information from Coinbase export file."""

    def __init__(self, row):
        """
        Initialize a new instance of CoinbaseParserCsv.

        Parameters:
        row (dict): A dictionary representing a single row from the Coinbase export file.
                    The keys represent the column names and the values represent the corresponding data.

        Attributes:
        input_row (dict): The original input data row.
        date (datetime): The date of the transaction.
        received_amount (str): The amount of received coins.
        received_currency (str): The currency of the received coins.
        sent_amount (str): The amount of sent coins.
        sent_currency (str): The currency of the sent coins.
        fee_amount (str): The amount of transaction fee coins.
        fee_currency (str): The currency of the transaction fee coins.
        order_id (str): The unique identifier for the exchange order.
        description (str): The description of the transaction.
        """
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
        """
        Return datestring in Chainreport format.

        This method formats the date attribute of the CoinbaseParserCsv object into a string 
        using the strftime function with the format '%d.%m.%Y %H:%M'. This format is commonly 
        used in the Chainreport format for dates.

        Parameters:
        None

        Returns:
        str: The date attribute of the CoinbaseParserCsv object formatted as a string in 
            the Chainreport format.
        """
        return self.date.strftime('%d.%m.%Y %H:%M')

    def get_transaction_type(self):
        """
        Return transaction type in Chainreport format.

        This method maps the 'Transaction Type' from the input row to the corresponding 
        transaction type in the Chainreport format. The mapping is done by checking if the 
        'Transaction Type' is present in the class-level lists (DEPOSITTRANSACTION, 
        WITHDRAWTRANSACTION, TRADETRANSACTION, OTHERINCOMETRANSACTION, STAKINGTRANSACTION). 
        If a match is found, the corresponding transaction type in the Chainreport format is 
        returned. If no match is found, the method returns 'ERROR'.

        Parameters:
        None

        Returns:
        str: The transaction type in the Chainreport format.
        """
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
        """
        Return the amount of received coins.

        If the transaction type is 'Withdrawal', an empty string is returned, 
        indicating that no coins were received. Otherwise, the amount of received coins 
        is returned.

        Parameters:
        None

        Returns:
        str: The amount of received coins if the transaction type is not 'Withdrawal', 
            otherwise an empty string.
        """
        if self.get_transaction_type() == 'Withdrawal':
            return ""
        return self.received_amount

    def get_received_currency(self):
        """
        Return the currency of received coins.

        If the transaction type is 'Withdrawal', an empty string is returned, 
        indicating that no coins were received. Otherwise, the currency of received coins 
        is returned.

        Parameters:
        None

        Returns:
        str: The currency of received coins if the transaction type is not 'Withdrawal', 
            otherwise an empty string.
        """
        if self.get_transaction_type() == 'Withdrawal':
            return ""
        return self.received_currency

    def get_sent_amount(self):
        """
        Return the amount of sent coins.

        If the transaction type is 'Trade', the negative value of the 'sent_amount' is returned, 
        indicating that coins were sent. If the transaction type is 'Withdrawal', the negative 
        value of the 'received_amount' is returned, indicating that coins were sent. If the 
        transaction type is neither 'Trade' nor 'Withdrawal', an empty string is returned, 
        indicating that no coins were sent.

        Parameters:
        None

        Returns:
        str: The negative value of the 'sent_amount' if the transaction type is 'Trade', 
            the negative value of the 'received_amount' if the transaction type is 'Withdrawal', 
            otherwise an empty string.
        """
        if self.get_transaction_type() == 'Trade':
            return "-" + self.sent_amount
        if self.get_transaction_type() == 'Withdrawal':
            return "-" + self.received_amount
        return ""

    def get_sent_currency(self):
        """
        Return the currency of sent coins.

        If the transaction type is 'Trade', the currency of the coins sent is returned.
        If the transaction type is 'Withdrawal', the currency of the coins received (which are then sent) is returned.
        If the transaction type is neither 'Trade' nor 'Withdrawal', an empty string is returned.

        Parameters:
        None

        Returns:
        str: The currency of sent coins if the transaction type is 'Trade' or 'Withdrawal', otherwise an empty string.
        """
        if self.get_transaction_type() == 'Trade':
            return self.sent_currency
        if self.get_transaction_type() == 'Withdrawal':
            return self.received_currency
        return ""

    def get_transaction_fee_amount(self):
        """
        Return the amount of transaction fee coins.

        This method retrieves the transaction fee amount from the 'fee_amount' attribute of the 
        CoinbaseParserCsv object. The 'fee_amount' attribute is a string that represents the 
        amount of transaction fee coins.

        Parameters:
        None

        Returns:
        str: The amount of transaction fee coins as a string.
        """
        return self.fee_amount

    def get_transaction_fee_currency(self):
        """
        Return the currency of transaction fee coins.

        This method retrieves the currency of transaction fee coins from the 'fee_currency' 
        attribute of the CoinbaseParserCsv object. The 'fee_currency' attribute is a string 
        that represents the currency of transaction fee coins.

        Parameters:
        None

        Returns:
        str: The currency of transaction fee coins as a string.
        """
        return self.fee_currency

    def get_order_id(self):
        """
        Return order id of the exchange.

        This method retrieves the order id from the 'order_id' attribute of the 
        CoinbaseParserCsv object. The 'order_id' attribute is a string that represents 
        the unique identifier for the exchange order.

        Parameters:
        None

        Returns:
        str: The order id of the exchange as a string.
        """
        return self.order_id

    def get_description(self):
        """
        Return description of the transaction.

        This method retrieves the description of the transaction from the 'description' 
        attribute of the CoinbaseParserCsv object. The 'description' attribute is a string 
        that provides a brief explanation of the transaction.

        Parameters:
        None

        Returns:
        str: The description of the transaction as a string.
        """
        return self.description
