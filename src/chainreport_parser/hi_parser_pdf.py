"""Parser implementation for HI"""

import re
from datetime import datetime
from .chainreport_parser_interface import ChainreportParserInterface

class HiParserPdf(ChainreportParserInterface):
    """Extract all required information from Hi statement."""

    def __init__(self, line):
        self.plain_line = line
        for data in re.finditer(r'(?P<date>\d+-\d+-\d+\s\d+\d+:\d+\s[UTC]+) (?P<description>[/a-zA-Z ()]+) (?P<amount>-*[\d]*[.]*[\d]*) (?P<currency>[\w]+$)', line):
            self.date = data.group('date')
            self.description = data.group('description')
            self.amount = data.group('amount').replace(".", ",")
            self.currency = data.group('currency')

    NAME = __qualname__
    CASHBACKTRANSACTION = ['HI rebate']
    DEPOSITTRANSACTION = ['Crypto deposit',
                          'crypto receive',
                          'Crypto purchase']
    STAKINGTRANSACTION = ['Crypto staking yields HI']
    WITHDRAWTRANSACTION = ['crypto send',
                           'Crypto withdraw']
    EXCLUSIONSTRINGS = ['Vault HI daily release',
                        'Crypto earning stake',
                        'Crypto earning release',
                        'Yields', 
                        'crypto transfer to trading', 
                        'crypto transfer to flexible',
                        'Card refund',
                        'Fiat deposit BankTransfer',
                        'Fiat depositIBAN',
                        'Card consume',
                        'Fiat withdraw (IBAN)']
    REFERRALSTRING = ['HI referrer reward',
                      'HI referrer rebate']
    TRADETRANSACTION = ['buy Vault HI', # 1. Hi splits trade into two lines
                        'buy HI paid',  # 2. Hi splits trade into two lines
                        'Dust to HI']
    PAYMENTTRANSACTION = ['convert']
    AIRDROPTRANSACTION = ['crypto cashhash redeem']
    CANCELTRANSACTION = ['Crypto cancel withdraw']
    OTHERINCOMETRANSACTION = ['Yields']

    def get_date_string(self):
        """Return datestring in Chainreport format"""
        transaction_time = datetime.strptime(self.date, '%Y-%m-%d %H:%M %Z')
        return transaction_time.strftime('%d.%m.%Y %H:%M')

    def get_transaction_type(self):
        """Return transaction type in Chainreport format"""
        return_string = 'ERROR'
        if self.description in HiParserPdf.CASHBACKTRANSACTION:
            return_string = 'Cashback'
        elif self.description in HiParserPdf.STAKINGTRANSACTION:
            return_string = 'Staking'
        elif self.description in HiParserPdf.DEPOSITTRANSACTION:
            return_string = 'Deposit'
        elif self.description in HiParserPdf.WITHDRAWTRANSACTION:
            return_string = 'Withdrawal'
        elif self.description in HiParserPdf.REFERRALSTRING:
            return_string = 'Referral_Rewards'
        elif self.description in HiParserPdf.TRADETRANSACTION:
            return_string = 'Trade'
        elif self.description in HiParserPdf.PAYMENTTRANSACTION:
            return_string = 'Payment'
        elif self.description in HiParserPdf.AIRDROPTRANSACTION:
            return_string = 'Airdrop'
        elif self.description in HiParserPdf.OTHERINCOMETRANSACTION:
            return_string = 'Other_Income'

        return return_string

    def get_received_amount(self):
        """Return amount of received coins"""
        if not self.amount.startswith("-"):
            return self.amount
        return ""

    def get_received_currency(self):
        """Return currency of receveid coins"""
        if not self.amount.startswith("-"):
            return self.currency
        return ""
    
    def get_sent_amount(self):
        """Return amount of sent coins"""
        if self.amount.startswith("-"):
            return self.amount
        return ""

    def get_sent_currency(self):
        """Return currency of sent coins"""
        if self.amount.startswith("-"):
            return self.currency
        return ""

    def get_transaction_fee_amount(self):
        """Return amount of transaction fee coins"""
        return ""

    def get_transaction_fee_currency(self):
        """Return currency of transaction fee coins"""
        return ""

    def get_order_id(self):
        """Return order id of the exchange"""
        # In the current Hi statement this is always empty
        return ""

    def get_description(self):
        """Return description of the transaction"""
        return self.description
