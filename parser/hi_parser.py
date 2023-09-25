"""Parser implementation for HI"""

from datetime import datetime
from .chainreport_parser_interface import ChainreportParserInterface

class HiParser(ChainreportParserInterface):
    """Extract all required information from Hi statement."""

    def __init__(self, row):
        self.row = row

    CASHBACKTRANSACTION = ['HI rebate']
    DEPOSITTRANSACTION = ['Crypto deposit',
                          'crypto receive']
    STAKINGTRANSACTION = ['Crypto staking yields （HI）']
    WITHDRAWTRANSACTION = ['crypto send',
                       'Crypto withdraw']
    EXCLUSIONSTRINGS = ['Vault HI daily release',
                       'Crypto earning stake',
                       'Crypto earning release']

    def get_date_string(self):
        """Return datestring in Chainreport format"""
        transaction_time = datetime.strptime(self.row['Date'], '%Y-%m-%d %H:%M %Z')
        return transaction_time.strftime('%d.%m.%Y %H:%M')

    def get_transaction_type(self):
        """Return transaction type in Chainreport format"""
        if self.row['Description'] in HiParser.CASHBACKTRANSACTION:
            return 'Cashback'
        if self.row['Description'] in HiParser.STAKINGTRANSACTION:
            return 'Staking'
        if self.row['Description'] in HiParser.DEPOSITTRANSACTION:
            return 'Deposit'
        if self.row['Description'] in HiParser.WITHDRAWTRANSACTION:
            return 'Withdrawal'
        return 'ERROR'

    def get_received_amount(self):
        """Return amount of received coins"""
        return self.row['Received Amount'].replace(".", ",")

    def get_received_currency(self):
        """Return currency of receveid coins"""
        return self.row['Received Currency']

    def get_sent_amount(self):
        """Return amount of sent coins"""
        return self.row['Sent Amount'].replace(".", ",")

    def get_sent_currency(self):
        """Return currency of sent coins"""
        return self.row['Sent Currency']

    def get_transaction_fee_amount(self):
        """Return amount of transaction fee coins"""
        return self.row['Fee Amount']

    def get_transaction_fee_currency(self):
        """Return currency of transaction fee coins"""
        return self.row['Fee Currency']

    def get_order_id(self):
        """Return order id of the exchange"""
        # In the current Hi statement this is always empty
        return self.row['TxHash']

    def get_description(self):
        """Return description of the transaction"""
        return self.row['Description']
