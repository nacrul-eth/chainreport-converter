"""Mandatory parser Interface for Chainreport to guarantee consistant data"""

import abc

class ChainreportParserInterface(metaclass=abc.ABCMeta):
    """Parser Interface with runtime error on missing implementation"""

    @classmethod
    def __subclasshook__(cls, subclass):
        """
        Class method to check if a subclass implements all required methods.

        This method is used by Python's built-in isinstance() and issubclass() functions to determine if a subclass
        fulfills the requirements of the abstract base class (ABC). It checks if the subclass has all the required
        methods and if they are callable.

        Parameters:
        cls (class): The abstract base class (ABC) being checked.
        subclass (class): The subclass being evaluated.

        Returns:
        bool or NotImplemented: Returns True if the subclass implements all required methods, False if it does not,
        or NotImplemented if the subclass does not inherit from the ABC.
        """
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
        """
        Check if the current line should be skipped during parsing.

        This method should be implemented by any class that inherits from this interface.
        It should return True if the line should be skipped, and False if the line is relevant.

        Parameters:
        None

        Returns:
        bool: True if the line should be skipped, False otherwise.

        Raises:
        NotImplementedError: If the method is not implemented in the inheriting class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_date_string(self):
        """
        Returns the date of the transaction in Chainreport format.

        The date should be in a specific format that Chainreport expects.
        This method should be implemented by any class that inherits from this interface.

        Parameters:
        None

        Returns:
        str: The date of the transaction in Chainreport format.

        Raises:
        NotImplementedError: If the method is not implemented in the inheriting class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_transaction_type(self):
        """
        Returns the type of transaction in Chainreport format.

        This method should be implemented by any class that inherits from this interface.
        It should return a string representing the type of transaction in the format expected by Chainreport.

        Parameters:
        None

        Returns:
        str: The type of transaction in Chainreport format.

        Raises:
        NotImplementedError: If the method is not implemented in the inheriting class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_received_amount(self):
        """
        Returns the amount of received coins.

        This method should be implemented by any class that inherits from this interface.
        It should return a float representing the amount of received coins.

        Parameters:
        None

        Returns:
        float: The amount of received coins.

        Raises:
        NotImplementedError: If the method is not implemented in the inheriting class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_received_currency(self):
        """
        Returns the currency of the received coins.

        This method should be implemented by any class that inherits from this interface.
        It should return a string representing the currency of the received coins.

        Parameters:
        None

        Returns:
        str: The currency of the received coins.

        Raises:
        NotImplementedError: If the method is not implemented in the inheriting class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_sent_amount(self):
        """
        Returns the amount of sent coins.

        This method should be implemented by any class that inherits from this interface.
        It should return a float representing the amount of sent coins.

        Parameters:
        None

        Returns:
        float: The amount of sent coins.

        Raises:
        NotImplementedError: If the method is not implemented in the inheriting class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_sent_currency(self):
        """
        Returns the currency of the sent coins.

        This method should be implemented by any class that inherits from this interface.
        It should return a string representing the currency of the sent coins.

        Parameters:
        None

        Returns:
        str: The currency of the sent coins.

        Raises:
        NotImplementedError: If the method is not implemented in the inheriting class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_transaction_fee_amount(self):
        """
        Returns the amount of transaction fee coins.

        This method should be implemented by any class that inherits from this interface.
        It should return a float representing the amount of transaction fee coins.

        Parameters:
        None

        Returns:
        float: The amount of transaction fee coins.

        Raises:
        NotImplementedError: If the method is not implemented in the inheriting class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_transaction_fee_currency(self):
        """
        Returns the currency of the transaction fee coins.

        This method should be implemented by any class that inherits from this interface.
        It should return a string representing the currency of the transaction fee coins.

        Parameters:
        None

        Returns:
        str: The currency of the transaction fee coins.

        Raises:
        NotImplementedError: If the method is not implemented in the inheriting class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_order_id(self):
        """
        Returns the order id of the exchange.

        This method should be implemented by any class that inherits from this interface.
        It should return a string representing the order id of the exchange.

        Parameters:
        None

        Returns:
        str: The order id of the exchange.

        Raises:
        NotImplementedError: If the method is not implemented in the inheriting class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_description(self):
        """
        Returns the description of the transaction.

        This method should be implemented by any class that inherits from this interface.
        It should return a string representing the description of the transaction.

        Parameters:
        None

        Returns:
        str: The description of the transaction.

        Raises:
        NotImplementedError: If the method is not implemented in the inheriting class.
        """
        raise NotImplementedError
