"""Parser implementation for HI"""

from datetime import datetime
from .chainreport_parser_interface import ChainreportParserInterface

class KrakenParserCsv(ChainreportParserInterface):
    """Extract all required information from Plutus Rewards file."""

    def __init__(self, row):
        self.input_row = row
        self.date = datetime.strptime(self.input_row['time'], '%Y-%m-%d %H:%M:%S')
        self.received_amount = self.input_row['amount'].replace(".", ",")
        self.received_currency = self.input_row['asset']
        self.sent_amount = self.input_row['amount'].replace(".", ",")
        self.sent_currency = self.input_row['asset']
        self.fee_amount = self.input_row['fee'].replace(".", ",")
        self.fee_currency = self.input_row['asset']
        self.order_id = self.input_row['txid']
        self.description = self.input_row['type']

    NAME = __qualname__
    DELIMITER=","
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
        """Return true, if the line should be skipped
           return false, if the line is relevant"""
        return self.input_row['type'] in self.SKIPSTRINGS

    def get_input_string(self):
        """Return the input data we are using"""
        return self.input_row

    def get_date_string(self):
        """Return datestring in Chainreport format"""
        return self.date.strftime('%d.%m.%Y %H:%M')

    def get_transaction_type(self):
        """Return transaction type in Chainreport format"""
        transaction_description = self.input_row['type']
        return_string = 'ERROR'
        if transaction_description in KrakenParserCsv.DEPOSITTRANSACTION:
            return_string = 'Deposit'
        if transaction_description in KrakenParserCsv.WITHDRAWTRANSACTION:
            return_string = 'Withdrawal'
        if transaction_description in KrakenParserCsv.TRADETRANSACTION:
            return_string = 'Trade'
        return return_string

    def get_received_amount(self):
        """Return amount of received coins"""
        if self.get_transaction_type() == 'Withdrawal':
            return ""
        if self.get_transaction_type() == 'Trade' and self.received_amount.startswith("-"):
            return ""
        return self.received_amount

    def get_received_currency(self):
        """Return currency of receveid coins"""
        if self.get_transaction_type() == 'Withdrawal':
            return ""
        if self.get_transaction_type() == 'Trade' and self.received_amount.startswith("-"):
            return ""
        return self.received_currency

    def get_sent_amount(self):
        """Return amount of sent coins"""
        if self.get_transaction_type() == 'Deposit':
            return ""
        if self.get_transaction_type() == 'Trade' and not self.sent_amount.startswith("-"):
            return ""
        return self.sent_amount

    def get_sent_currency(self):
        """Return currency of sent coins"""
        if self.get_transaction_type() == 'Deposit':
            return ""
        if self.get_transaction_type() == 'Trade' and not self.sent_amount.startswith("-"):
            return ""
        return self.sent_currency

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