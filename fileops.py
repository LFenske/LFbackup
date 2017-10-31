#!/usr/bin/env python3

import os.path
import stat
import sys

class FileOps(object):

    blocksize = 64*1024
    # os.supports_follow_symlinks is only in Python 3.3 and later.
    fsl_chmod = False if os.chmod in os.supports_follow_symlinks else True
    fsl_chown = False if os.chown in os.supports_follow_symlinks else True
    fsl_utime = False if os.utime in os.supports_follow_symlinks else True
    fsl_stat  = False if os.stat  in os.supports_follow_symlinks else True

    def __init__(self, dm, ds, compress, crypt, hashfact):
        self.dm       = dm        # instance of DataBase
        self.ds       = ds        # instance of DataStore
        self.compress = compress  # instance of Compress
        self.crypt    = crypt     # instance of Crypt
        self.hashfact = hashfact  # instance of Hash

    def backup(self, filename):
        """
        Backup a file; data and metadata.
        """
        stats = os.stat(filename, follow_symlinks=self.fsl_stat)
        print(filename)
        print(stats)
        is_dir = os.path.isdir(filename)  #TODO What about symlinks, sockets, fifos, device files?
        depth, hsh = (0,0) if is_dir else self.__put_data(filename)
        print(depth, hsh)
        self.dm.put(filename, is_dir, stats, depth, hsh)

    def restore(self, filename, desname):
        """
        Restore a file; data and metadata.
        """
        (is_dir, stats, depth, hsh) = self.dm.get(filename)
        is_dir=is_dir
        fmt  = stat.S_IFMT (stats.st_mode)
        mode = stat.S_IMODE(stats.st_mode)
        if   stat.S_ISREG (fmt):
            self.__get_data(desname, depth, hsh)
            # st_mode
            # st_nlink  restore hard links
            # st_uid
            # st_gid
            # st_atime, st_mtime, st_atime_ns, st_mtime_ns
        elif stat.S_ISBLK (fmt) or stat.S_ISCHR (fmt) or stat.S_ISFIFO(fmt):
            os.mknod(desname, mode=stats.st_mode, device=stats.st_rdev)  #TODO st_rdev might not exist
        elif stat.S_ISDIR (fmt):
            os.makedirs(desname, mode=mode, exist_ok=True)
        elif stat.S_ISLNK (fmt):
            pass  #TODO
        elif stat.S_ISSOCK(fmt):
            pass  #TODO
        #TODO Should these be set on the linkee if we can't set the link?
        os.chmod(desname, mode, follow_symlinks=self.fsl_chmod)
        os.chown(desname, stats.st_uid, stats.st_gid, follow_symlinks=self.fsl_chown)
        os.utime(desname, ns=(stats.st_atime_ns, stats.st_mtime_ns), follow_symlinks=self.fsl_utime)
        # os.makedirs
        # os.mkfifo
        # os.mknod
        # os.symlink
        # os.chown
        # os.chmod
        #TODO
        pass

    def __put_data(self, filename):
        """
        Backup the data for a file.
        Return depth, hash.
        """
        groups = []
        with open(filename, "rb") as f:
            while True:
                buf = f.read(self.blocksize)
                if buf:
                    hsh = self.__put_block(buf)
                else:
                    break
                gnum = 0
                while True:
                    if len(groups) <= gnum:
                        groups.append(b"")
                    if len(groups[gnum]) + len(hsh) > self.blocksize:
                        carry = self.__put_block(groups[gnum])
                        groups[gnum] = b""
                    else:
                        carry = None
                    groups[gnum] += hsh
                    if carry:
                        hsh = carry
                        gnum += 1
                    else:
                        break
        # flush
        gnum = 0
        hsh = b""
        while True:
            if len(groups) <= gnum:
                groups.append(b"")
                if len(groups) > 10:
                    print("too many levels")
                    sys.exit(-1)
            if len(groups[gnum]) + len(hsh) > self.blocksize:
                carry = self.__put_block(groups[gnum])
                groups[gnum] = b""
            else:
                carry = b""
            groups[gnum] += hsh
            if len(groups) == gnum+1 and len(groups[gnum]) == self.hashfact().hashlen() and not carry:
                return gnum, groups[gnum]
            if len(groups[gnum]):
                carry += self.__put_block(groups[gnum])
                groups[gnum] = b""
            hsh = carry
            gnum += 1

    def __get_data(self, filename, depth, hsh):
        """
        Restore the data for a file.
        """
        def __get_block(curdepth):
            if hashpointers[curdepth] >= len(hashlists[curdepth]):
                if curdepth+1 >= len(hashlists):
                    return None
                hashlists[curdepth] = __get_block(curdepth+1)
                hashpointers[curdepth] = 0
                if hashlists[curdepth] is None:
                    return None
            hsh = hashlists[curdepth][hashpointers[curdepth]:hashpointers[curdepth]+self.hashfact().hashlen()]
            hashpointers[curdepth] += self.hashfact().hashlen()
            bufe = ds.get(hsh)
            bufc = self.crypt.decrypt(bufe)
            buf  = self.compress.decompress(bufc)
            return buf

        hashlists = [b""] * depth
        hashlists.append(hsh)
        hashpointers = [0] * (depth+1)
        with open(filename, "wb") as f:
            while True:
                block = __get_block(0)
                if block is None:
                    break
                f.write(block)

    def __put_block(self, buf):
        bufc = self.compress.compress(buf)
        bufe = self.crypt.encrypt(bufc)
        h = self.hashfact()
        h.update(bufe)
        hsh = h.digest()
        self.ds.put(hsh, bufe)
        return hsh

if __name__ == "__main__":
    import datameta_tree
    import datastore_tree
    import compress_none
    import crypt_none
    import compress_gzip
    import crypt_aes
    import hash_sha1

    basepath = "/tmp/testtree"
    key      = b"12345678"

    dm       = datameta_tree.DataMeta_Tree(basepath)
    ds       = datastore_tree.DataStore_Tree(basepath)
#     compress = compress_none.Compress_None()
#     crypt    = crypt_none.Crypt_None(key)
    compress = compress_gzip.Compress_Gzip()
    crypt    = crypt_aes.Crypt_AES(key)
    hashfact = hash_sha1.Hash_SHA1
    fo = FileOps(dm, ds, compress, crypt, hashfact)

    fo.backup("qd")
    fo.backup("fileops.py")
    fo.restore("fileops.py", "q1")
    fo.backup("initrd.img-3.19.0-84-generic")
    fo.restore("initrd.img-3.19.0-84-generic", "q")