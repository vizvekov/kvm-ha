__author__ = 'Vadim'

import imp
import sys
import hashlib

def import_module(path,name,unique_name, globals=None, locals=None, fromlist=None):
# Fast path: see if unique_name has already been imported.
    try:
        return sys.modules[unique_name]
    except KeyError:
        pass

    sys.path.append(path)
    fp, pathname, description = imp.find_module(name)
    sys.path.pop(-1)

    try:
        return imp.load_module(unique_name,fp, pathname, description)
    finally:
        # Since we may exit via an exception, close fp explicitly.
        if fp:
            fp.close()

def get_index(seq, attr, value):
    return (item for item in seq if item[attr] == value).next()

def update_dic_in_list(seq, old_attr, old_val, new_arrt, new_val):
    iter = 0
    for item in seq:
        if item[old_attr] == old_val:
            item[new_arrt] = new_val
            seq[iter] = item
        iter += 1
    return seq

def get_hash(str):
    return int(hashlib.md5(str).hexdigest(), 16)


