"""
abstract super-class for file hashes
"""
import abc


class Hash(object, metaclass=abc.ABCMeta):
    def __init__(self):
        None

    def __str__(self):
        return self.hexify(self)

    @abc.abstractmethod
    def hashlen(self):
        return None

    @abc.abstractmethod
    def update(self, s):
        None

    @abc.abstractmethod
    def digest(self):
        return None

    def hexdigest(self):
        return self.hexify(self.digest())

    @classmethod
    def hexify(cls, dig):
        return ''.join(['%.2x' % x for x in dig])

    # arithmetic

    @classmethod
    def min(cls):
        return b'\x00' * cls().hashlen()

    @classmethod
    def max(cls):
        return b'\xff' * cls().hashlen()

    def isincluded(self, a, b):
        return a <= self.digest() <= b

    @classmethod
    def split_range(cls, a, b, n=2):
        assert(n==2)  # We can currently only handle n=2.
        carry = 1 if b == cls.max() else 0
        assert(len(a) == len(b))
        # sum into list of numbers
        s = []  # list of numbers
        for i in range(len(a), 0, -1):
            (q, r) = divmod(ord(a[i-1]) + ord(b[i-1]) + carry, 256)
            s.insert(0, r)
            carry = q
        # "carry" holds the MSB
        # divide by 2 into list of characters
        v = []  # list of characters
        for i in range(len(a)):
            (q, r) = divmod(carry*256 + s[i], 2)
            v.append(chr(q))
            carry = r
        # Convert back to string.
        return "".join(v)

