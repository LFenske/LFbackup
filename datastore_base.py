"""
abstract super-class for storing data objects
"""
import abc


class DataStore(object, metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def get(self, key1):
        """
        Retrieve an object by key1.
        """
        return None

    @abc.abstractmethod
    def put(self, key1, val1):
        """
        Store an object.
        """
        pass

    @abc.abstractmethod
    def check(self, key1):
        """
        Return boolean for existence of key1.
        """
        return None

    @abc.abstractmethod
    def delete(self, key1):
        """
        Remove an object forever.
        """
        pass

    @abc.abstractmethod
    def mark_start(self):
        """
        Begin marking objects as in-use.
        """
        pass

    @abc.abstractmethod
    def mark_mark(self, key1):
        """
        Mark this object as in-use.
        """
        pass

    @abc.abstractmethod
    def mark_cancel(self):
        """
        Abort the process of marking objects as in-use.
        """
        pass

    @abc.abstractmethod
    def mark_delete(self):
        """
        Permanently remove objects that are unmarked and end the process
        of marking.

        """
        pass
