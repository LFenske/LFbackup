#!/usr/bin/env python3

from crypt_base import Crypt

from Crypto.Cipher import AES
import hash_sha1


class Crypt_AES(Crypt):
    def __init__(self, key1):
        super().__init__()
        h = hash_sha1.Hash_SHA1()
        h.update(key1)
        keyhash = h.digest()[0:16]
        self.cipher = AES.new(keyhash)

    def encrypt(self, s):
        l = len(s)
        lba = bytearray(4)
        lba[0] = (l >> 24) & 0xff
        lba[1] = (l >> 16) & 0xff
        lba[2] = (l >>  8) & 0xff
        lba[3] = (l >>  0) & 0xff
        s = lba + s
        s += bytearray(16 - ((len(s)+1)%16-1))
        return self.cipher.encrypt(bytes(s))

    def decrypt(self, s):
        r = self.cipher.decrypt(s)
        l = 0
        l = (l << 8) + r[0]
        l = (l << 8) + r[1]
        l = (l << 8) + r[2]
        l = (l << 8) + r[3]
        return r[4:4+l]

if __name__ == "__main__":
    c = Crypt_AES(b"The key is the key.")
    s = b""
    for si in [b"abcdefghijklmnopqrstuvwxyz", b"1", b"2", b"3", b"4"]:
        s += si
        en = c.encrypt(s)
        de = c.decrypt(en)
        print(de)
        assert(de == s)
