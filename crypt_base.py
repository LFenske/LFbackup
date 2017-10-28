"""
abstract super-class for encryption and decryption
"""
import abc

class Crypt(object, metaclass=abc.ABCMeta):
    def __init__(self):
        None

    @abc.abstractmethod
    def encrypt(self, s):
        None

    @abc.abstractmethod
    def decrypt(self, s):
        None
