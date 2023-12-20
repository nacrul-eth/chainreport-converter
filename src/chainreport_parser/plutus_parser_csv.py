"""Parser implementation for HI"""
# pylint: disable=duplicate-code

from datetime import datetime
from .chainreport_parser_interface import ChainreportParserInterface

class PlutusParserCsv(ChainreportParserInterface):
    """Extract all required information from Plutus Rewards file."""

    def __init__(self, row):
        self.input_row = row

    NAME = __qualname__
    DELIMITER="|"
    CASHBACKTRANSACTION = ['DAILY_REBATE_DISTRIBUTION',
                           'REBATE_BONUS']   # user for manual rebates (positive & negative)
    DEPOSITTRANSACTION = []
    STAKINGTRANSACTION = []
    WITHDRAWTRANSACTION = []
    EXCLUSIONSTRINGS = []
    REFERRALSTRING = []
    TRADETRANSACTION = []
    PAYMENTTRANSACTION = []
    AIRDROPTRANSACTION = []
    CANCELTRANSACTION = []

    def get_input_string(self):
        """Return the input data we are using"""
        return self.input_row

    def get_date_string(self):
        """Return datestring in Chainreport format"""
        transaction_time = datetime.strptime(self.input_row['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
        return transaction_time.strftime('%d.%m.%Y %H:%M')

    def get_transaction_type(self):
        """Return transaction type in Chainreport format"""
        transaction_description = self.input_row['type']
        return_string = 'ERROR'
        if transaction_description in PlutusParserCsv.CASHBACKTRANSACTION:
            return_string = 'Cashback'
        return return_string

    def get_received_amount(self):
        """Return amount of received coins"""
        return self.input_row['reward_plu_value'].replace(".", ",")

    def get_received_currency(self):
        """Return currency of receveid coins"""
        return "PLU"

    def get_sent_amount(self):
        """Return amount of sent coins"""
        return ""

    def get_sent_currency(self):
        """Return currency of sent coins"""
        return ""

    def get_transaction_fee_amount(self):
        """Return amount of transaction fee coins"""
        return ""

    def get_transaction_fee_currency(self):
        """Return currency of transaction fee coins"""
        return ""

    def get_order_id(self):
        """Return order id of the exchange"""
        return self.input_row['statement_id']

    def get_description(self):
        """Return description of the transaction"""
        return self.input_row['description']
