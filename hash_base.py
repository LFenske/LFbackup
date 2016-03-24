"""
abstract super-class for file hashes
"""
import abc

class Hash(object, metaclass=abc.ABCMeta):
    def __init__(self):
        None
    
    @abc.abstractmethod
    def update(self, s):
        None
    
    @abc.abstractmethod
    def digest(self):
        return None

    @abc.abstractmethod
    def hexdigest(self):
        return None
