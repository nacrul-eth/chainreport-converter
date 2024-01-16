"""Mandatory parser Interface for Chainreport to guarantee consistant data"""

import abc

class ChainreportParserInterface(metaclass=abc.ABCMeta):
    """Parser Interface with runtime error on missing implementation"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'check_if_skip_line') and
                callable(subclass.check_if_skip_line) and
                hasattr(subclass, 'get_date_string') and
                callable(subclass.get_date_string) and
                hasattr(subclass, 'get_transaction_type') and
                callable(subclass.get_transaction_type) and
                hasattr(subclass, 'get_received_amount') and
                callable(subclass.get_received_amount) and
                hasattr(subclass, 'get_received_currency') and
                callable(subclass.get_received_currency) and
                hasattr(subclass, 'get_sent_amount') and
                callable(subclass.get_sent_amount) and
                hasattr(subclass, 'get_sent_currency') and
                callable(subclass.get_sent_currency) and
                hasattr(subclass, 'get_transaction_fee_amount') and
                callable(subclass.get_transaction_fee_amount) and
                hasattr(subclass, 'get_transaction_fee_currency') and
                callable(subclass.get_transaction_fee_currency) and
                hasattr(subclass, 'get_order_id') and
                callable(subclass.get_order_id) and
                hasattr(subclass, 'get_description') and
                callable(subclass.get_description) or
                NotImplemented)

    @abc.abstractmethod
    def check_if_skip_line(self):
        """Return true, if the line should be skipped
           return false, if the line is relevant"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_date_string(self):
        """Return datestring in Chainreport format"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_transaction_type(self):
        """Return transaction type in Chainreport format"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_received_amount(self):
        """Return amount of received coins"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_received_currency(self):
        """Return currency of receveid coins"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_sent_amount(self):
        """Return amount of sent coins"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_sent_currency(self):
        """Return currency of sent coins"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_transaction_fee_amount(self):
        """Return amount of transaction fee coins"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_transaction_fee_currency(self):
        """Return currency of transaction fee coins"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_order_id(self):
        """Return order id of the exchange"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_description(self):
        """Return description of the transaction"""
        raise NotImplementedError
