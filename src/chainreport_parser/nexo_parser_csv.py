"""Parser implementation for HI"""

from datetime import datetime
from .chainreport_parser_interface import ChainreportParserInterface

class NexoParserCsv(ChainreportParserInterface):
    """Extract all required information from Hi statement."""

    def __init__(self, row):
        self.input_row = row

    NAME = __qualname__
    DELIMITER=","
    CASHBACKTRANSACTION = ['Exchange Cashback']
    DEPOSITTRANSACTION = ['Deposit To Exchange',
                          'Top up Crypto']
    STAKINGTRANSACTION = []
    LENDINGTRANSACTION = ['Interest',
                          'Fixed Term Interest']
    WITHDRAWTRANSACTION = ['Withdrawal']
    EXCLUSIONSTRINGS = ['Exchange Deposited On',
                        'Credit Card Fiaxt Refund',
                        'Unlocking Term Deposit',
                        'Locking Term Deposit',
                        'Credit Card Fiatx Exchange To Withdraw',
                        'Credit Card Fiatx Authorization',
                        'Credit Card Fiatx Refund']
    REFERRALSTRING = []  #unknown
    TRADETRANSACTION = ['Exchange']
    PAYMENTTRANSACTION = ['Withdraw Exchanged']
    AIRDROPTRANSACTION = [] #unknown
    CANCELTRANSACTION = [] #unknown

    POSSIBLE_OUTPUT = PAYMENTTRANSACTION + TRADETRANSACTION + WITHDRAWTRANSACTION

    def get_input_string(self):
        """Return the input data we are using"""
        return self.input_row

    def get_date_string(self):
        """Return datestring in Chainreport format"""
        transaction_time = datetime.strptime(self.input_row['Date / Time (UTC)'], '%Y-%m-%d %H:%M:%S')
        return transaction_time.strftime('%d.%m.%Y %H:%M')

    def get_transaction_type(self):
        """Return transaction type in Chainreport format"""
        transaction_description = self.input_row['Type']
        return_string = 'ERROR'
        if transaction_description in NexoParserCsv.CASHBACKTRANSACTION:
            return_string = 'Cashback'
        elif transaction_description in NexoParserCsv.STAKINGTRANSACTION:
            return_string = 'Staking'
        elif transaction_description in NexoParserCsv.DEPOSITTRANSACTION:
            return_string = 'Deposit'
        elif transaction_description in NexoParserCsv.WITHDRAWTRANSACTION:
            return_string = 'Withdrawal'
        elif transaction_description in NexoParserCsv.REFERRALSTRING:
            return_string = 'Referral_Rewards'
        elif transaction_description in NexoParserCsv.TRADETRANSACTION:
            return_string = 'Trade'
        elif transaction_description in NexoParserCsv.PAYMENTTRANSACTION:
            return_string = 'Payment'
        elif transaction_description in NexoParserCsv.AIRDROPTRANSACTION:
            return_string = 'Airdrop'
        elif transaction_description in NexoParserCsv.LENDINGTRANSACTION:
            return_string = 'Lending'
        elif transaction_description in NexoParserCsv.EXCLUSIONSTRINGS:
            return_string = self.SKIP_STR
        return return_string

    def get_received_amount(self):
        """Return amount of received coins"""
        if self.input_row['Type'] in NexoParserCsv.TRADETRANSACTION:
            return self.input_row['Output Amount'].replace(".", ",")
        if self.input_row['Type'] in NexoParserCsv.PAYMENTTRANSACTION + NexoParserCsv.WITHDRAWTRANSACTION:
            return ""
        return self.input_row['Input Amount'].replace(".", ",")

    def get_received_currency(self):
        """Return currency of receveid coins"""
        if self.input_row['Type'] in NexoParserCsv.TRADETRANSACTION:
            return self.input_row['Output Currency']
        if self.input_row['Type'] in NexoParserCsv.PAYMENTTRANSACTION + NexoParserCsv.WITHDRAWTRANSACTION:
            return ""
        return self.input_row['Input Currency']

    def get_sent_amount(self):
        """Return amount of sent coins"""
        if self.input_row['Type'] in NexoParserCsv.POSSIBLE_OUTPUT:
            return self.input_row['Input Amount'].replace(".", ",")

    def get_sent_currency(self):
        """Return currency of sent coins"""
        if self.input_row['Type'] in NexoParserCsv.POSSIBLE_OUTPUT:
            return self.input_row['Input Currency']

    def get_transaction_fee_amount(self):
        """Return amount of transaction fee coins"""
        return None

    def get_transaction_fee_currency(self):
        """Return currency of transaction fee coins"""
        return None

    def get_order_id(self):
        """Return order id of the exchange"""
        # In the current Hi statement this is always empty
        return self.input_row['Transaction']

    def get_description(self):
        """Return description of the transaction"""
        return self.input_row['Details']
