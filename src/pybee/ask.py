
import getpass


YES_LIST = ['yes', 'y']
NO_LIST = ['no', 'n']

def confirm(msg, default='', allow_empty=True):
    if default:
        m = '%s[%s]: ' %(msg, default)
    else:
        m = '%s: ' % msg

    while True:
        p = input(m)
        p = p if p else default

        if not p and allow_empty:
            return p

        if not p: continue

        return p

def _input_one_password(msg, allow_empty=True):

    while True:
        v = getpass.getpass(msg)
        if not v and not allow_empty: continue

        return v

def input_password(msg, allow_empty=True, confirm=True):
    m = '%s: ' % msg
    retype_msg = 'Retype %s: ' % msg
    v1, v2 = None, None

    while True:
        v1 = _input_one_password(m, allow_empty)
        if confirm:
            v2 = _input_one_password(retype_msg, allow_empty)
            if v1 == v2:
                break

            print('Sorry, passwords do not match.')
            continue

    return v1


def choice(msg, v_list, type=str):
    m = '%s: ' % msg
    while True:
        p = input(m)
        if not p: continue
        p = type(p)
        if p not in v_list: continue 

        return p

def choice_list(msg, v_list, type=str):
    m = '%s: ' % msg
    while True:
        p = input(m)
        if not p: continue
        p_list = p.split(' ')
        l = []
        for x in p_list:
            if not x: continue 
            v = type(x)
            if v not in v_list: 
                l.clear()
                break
            else: 
                l.append(v)

        if not l: continue
        return l

def yes_or_no(msg, default=None):
    m = '%s[Y/N]:' % msg
    while True:
        p = input(m)
        p = p if p else default
        if not p: continue

        p = p.lower()
        if p not in YES_LIST and p not in NO_LIST: continue 

        if p in YES_LIST: return True

        return False

