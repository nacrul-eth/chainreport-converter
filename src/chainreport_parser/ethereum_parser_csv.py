"""Parser implementation for HI"""

from datetime import datetime
from .chainreport_parser_interface import ChainreportParserInterface

class EthereumParserCsv(ChainreportParserInterface):
    """Extract all required information from Plutus Rewards file."""

    def __init__(self, row):
        self.input_row = row

    NAME = __qualname__
    DELIMITER=","
    CASHBACKTRANSACTION = []
    DEPOSITTRANSACTION = ['Transfer']
    STAKINGTRANSACTION = []
    WITHDRAWTRANSACTION = ['Deposit',
                           'Transfer From']
    SKIPSTRINGS = []
    REFERRALSTRING = []
    TRADETRANSACTION = ['Buy',
                        'Mint',
                        'Pre Sale Mint']
    PAYMENTTRANSACTION = []
    AIRDROPTRANSACTION = []
    CANCELTRANSACTION = []

    def check_if_skip_line(self):
        """Return true, if the line should be skipped
           return false, if the line is relevant"""
        return self.input_row['Method'] in self.SKIPSTRINGS

    def get_input_string(self):
        """Return the input data we are using"""
        return self.input_row

    def get_date_string(self):
        """Return datestring in Chainreport format"""
        transaction_time = datetime.strptime(self.input_row['DateTime (UTC)'], '%Y-%m-%d %H:%M:%S')
        return transaction_time.strftime('%d.%m.%Y %H:%M')

    def get_transaction_type(self):
        """Return transaction type in Chainreport format"""
        transaction_description = self.input_row['Method']
        return_string = 'ERROR'
        if transaction_description in EthereumParserCsv.DEPOSITTRANSACTION:
            return_string = 'Deposit'
        if transaction_description in EthereumParserCsv.WITHDRAWTRANSACTION:
            return_string = 'Withdrawal'
        return return_string

    def get_received_amount(self):
        """Return amount of received coins"""
        receive_amount = self.input_row['Value_IN(ETH)'].replace(".", ",")
        if receive_amount == 0:
            return ""
        return receive_amount

    def get_received_currency(self):
        """Return currency of receveid coins"""
        return "ETH"

    def get_sent_amount(self):
        """Return amount of sent coins"""
        sent_amount = self.input_row['Value_OUT(ETH)'].replace(".", ",")
        if sent_amount == 0:
            return ""
        return sent_amount

    def get_sent_currency(self):
        """Return currency of sent coins"""
        return "ETH"

    def get_transaction_fee_amount(self):
        """Return amount of transaction fee coins"""
        return self.input_row['TxnFee(ETH)'].replace(".", ",")

    def get_transaction_fee_currency(self):
        """Return currency of transaction fee coins"""
        return "ETH"

    def get_order_id(self):
        """Return order id of the exchange"""
        return self.input_row['Transaction Hash']

    def get_description(self):
        """Return description of the transaction"""
        return self.input_row['Method']
