"""
abstract super-class for storing data objects
"""
import abc

class DataStore(object, metaclass=abc.ABCMeta):
    def __init__(self):
        None
    
    @abc.abstractmethod
    def get(self, key):
        """
        Retrieve an object by key.
        """
        return None
    
    @abc.abstractmethod
    def put(self, key, val):
        """
        Store an object.
        """
        None
    
    @abc.abstractmethod
    def check(self, key):
        """
        Return boolean for existence of key.
        """
        None

    @abc.abstractmethod
    def delete(self, key):
        """
        Remove an object forever.
        """
        None
    
    @abc.abstractmethod
    def mark_start(self):
        """
        Begin marking objects as in-use.
        """
        None
    
    @abc.abstractmethod
    def mark_mark(self, key):
        """
        Mark this object as in-use.
        """
        None
    
    @abc.abstractmethod
    def mark_cancel(self):
        """
        Abort the process of marking objects as in-use.
        """
        None
    
    @abc.abstractmethod
    def mark_delete(self):
        """
        Permanently remove objects that are unmarked and end the process of marking.
        """
        None
    