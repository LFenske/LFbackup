"""
abstract superclass for storing file information
"""
import abc


class DataMeta_Base(object):

    def __init__(self):
        pass

    @abc.abstractmethod
    def put(self, filename, is_dir, stats, depth, hsh):
        pass

    @abc.abstractmethod
    def get(self, filename):
#       return (is_dir, stats, depth, hsh)
        return None
