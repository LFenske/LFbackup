"""
abstract super-class for compression and decompression
"""
import abc


class Compress(object, metaclass=abc.ABCMeta):
    def __init__(self):
        None

    @abc.abstractmethod
    def compress(self, s):
        None

    @abc.abstractmethod
    def decompress(self, s):
        None
