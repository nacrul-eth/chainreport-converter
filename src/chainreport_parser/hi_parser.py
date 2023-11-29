"""Parser implementation for HI"""

from datetime import datetime
from .chainreport_parser_interface import ChainreportParserInterface

class HiParser(ChainreportParserInterface):
    """Extract all required information from Hi statement."""

    def __init__(self, row):
        self.row = row

    NAME = __qualname__
    DELIMITER=","
    CASHBACKTRANSACTION = ['HI rebate']
    DEPOSITTRANSACTION = ['Crypto deposit',
                          'crypto receive',
                          'Crypto purchase'] # Missing Euro Amount in CSV from Hi
    STAKINGTRANSACTION = ['Crypto staking yields （HI）']
    WITHDRAWTRANSACTION = ['crypto send',
                       'Crypto withdraw'] # Missing Euro Amount in CSV from Hi
    EXCLUSIONSTRINGS = ['Vault HI daily release',
                       'Crypto earning stake',
                       'Crypto earning release',
                       'Yields']
    REFERRALSTRING = ['HI referrer reward',
                      'HI referrer rebate']
    TRADETRANSACTION = ['buy Vault HI', # 1. Hi splits trade into two lines
                        'buy HI paid',  # 2. Hi splits trade into two lines
                        'Dust to HI']
    PAYMENTTRANSACTION = ['Fiat deposit（IBAN）',
                          'Fiat withdraw (IBAN)',
                          'Card refund',
                          'Card consume',
                          'Fiat deposit （BankTransfer）',
                          'convert'] # Missing Euro Amount in CSV from Hi
    AIRDROPTRANSACTION = ['crypto cashhash redeem']
    CANCELTRANSACTION = ['Crypto cancel withdraw']

    def get_date_string(self):
        """Return datestring in Chainreport format"""
        transaction_time = datetime.strptime(self.row['Date'], '%Y-%m-%d %H:%M %Z')
        return transaction_time.strftime('%d.%m.%Y %H:%M')

    def get_transaction_type(self):
        """Return transaction type in Chainreport format"""
        transaction_description = self.row['Description']
        return_string = 'ERROR'
        if transaction_description in HiParser.CASHBACKTRANSACTION:
            return_string = 'Cashback'
        elif transaction_description in HiParser.STAKINGTRANSACTION:
            return_string = 'Staking'
        elif transaction_description in HiParser.DEPOSITTRANSACTION:
            return_string = 'Deposit'
        elif transaction_description in HiParser.WITHDRAWTRANSACTION:
            return_string = 'Withdrawal'
        elif transaction_description in HiParser.REFERRALSTRING:
            return_string = 'Referral_Rewards'
        elif transaction_description in HiParser.TRADETRANSACTION:
            return_string = 'Trade'
        elif transaction_description in HiParser.PAYMENTTRANSACTION:
            return_string = 'Payment'
        elif transaction_description in HiParser.AIRDROPTRANSACTION:
            return_string = 'Airdrop'

        return return_string

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
