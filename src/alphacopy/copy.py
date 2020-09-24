from os import fsync, listdir, mkdir
from shutil import copy2, disk_usage
from os.path import join, islink, isdir


def copy_file(src: str, dst: str):
    """
    Copies single file from src to dst
    """
    copy2(src, dst)
    destin = open(dst, "a")
    fsync(destin)
    destin.close()


def check_disks(src: str, dst: str) -> bool:
    """
    Checks whether filesystem on "dst" has enough free space for "src" files
    """
    src_disk_usage = disk_usage(src)[1]
    destinaton_disk_free = disk_usage(dst)[2]
    return src_disk_usage <= destinaton_disk_free

def copy_tree(src: str, dst: str):
    """
    Walks down recursively src tree calling copy_file() to copy it to dst
    """ 
    entries = listdir(src) #returns a list containing the names of entries (files and directories) in the directory
    errors = []
    if not isdir(dst): 
        mkdir(dst)
    for entry in entries:
        #creates full path variables of entry in both src and dst
        srcname = join(src, entry)
        dstname = join(dst, entry)
        try:
            if islink(srcname):
                #what do we do here?
                pass
            elif isdir(srcname):
                mkdir(dstname)
                copy_tree(srcname, dstname)
            else:
                copy_file(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except OSError as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Exception as err:
            errors.extend(err.args[0])
    # try:
    #     copystat(src, dst)
    # except OSError as why:
    #     # can't copy file access times on Windows
    #     if why.winerror is None:
    #         errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)