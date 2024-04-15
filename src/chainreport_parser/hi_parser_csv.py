"""Parser implementation for HI"""

from datetime import datetime
from .chainreport_parser_interface import ChainreportParserInterface

class HiParserCsv(ChainreportParserInterface):
    """Extract all required information from Hi statement."""

    def __init__(self, row):
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

    def check_if_skip_line(self):
        """Return true, if the line should be skipped
           return false, if the line is relevant"""
        return self.input_row['Description'] in self.SKIPSTRINGS

    def get_input_string(self):
        """Return the input data we are using"""
        return self.input_row

    def get_date_string(self):
        """Return datestring in Chainreport format"""
        transaction_time = datetime.strptime(self.input_row['Date'], '%Y-%m-%d %H:%M %Z')
        return transaction_time.strftime('%d.%m.%Y %H:%M')

    def get_transaction_type(self):
        """Return transaction type in Chainreport format"""
        transaction_description = self.input_row['Description']
        return_string = 'ERROR'
        if transaction_description in HiParserCsv.CASHBACKTRANSACTION:
            return_string = 'Cashback'
        elif transaction_description in HiParserCsv.STAKINGTRANSACTION:
            return_string = 'Staking'
        elif transaction_description in HiParserCsv.DEPOSITTRANSACTION:
            return_string = 'Deposit'
        elif transaction_description in HiParserCsv.WITHDRAWTRANSACTION:
            return_string = 'Withdrawal'
        elif transaction_description in HiParserCsv.REFERRALSTRING:
            return_string = 'Referral_Rewards'
        elif transaction_description in HiParserCsv.TRADETRANSACTION:
            return_string = 'Trade'
        elif transaction_description in HiParserCsv.PAYMENTTRANSACTION:
            return_string = 'Payment'
        elif transaction_description in HiParserCsv.AIRDROPTRANSACTION:
            return_string = 'Airdrop'
        elif transaction_description in HiParserCsv.OTHERINCOMETRANSACTION:
            return_string = 'Other_Income'

        return return_string

    def get_received_amount(self):
        """Return amount of received coins"""
        return self.input_row['Received Amount'].replace(".", ",")

    def get_received_currency(self):
        """Return currency of receveid coins"""
        return self.input_row['Received Currency']

    def get_sent_amount(self):
        """Return amount of sent coins"""
        return self.input_row['Sent Amount'].replace(".", ",")

    def get_sent_currency(self):
        """Return currency of sent coins"""
        return self.input_row['Sent Currency']

    def get_transaction_fee_amount(self):
        """Return amount of transaction fee coins"""
        return self.input_row['Fee Amount']

    def get_transaction_fee_currency(self):
        """Return currency of transaction fee coins"""
        return self.input_row['Fee Currency']

    def get_order_id(self):
        """Return order id of the exchange"""
        # In the current Hi statement this is always empty
        return self.input_row['TxHash']

    def get_description(self):
        """Return description of the transaction"""
        return self.input_row['Description']
