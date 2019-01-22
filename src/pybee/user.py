
import os
import pwd


def get_puser_name():
    '''
    获取当前进程的用户名
    '''
    return pwd.getpwuid(os.getuid()).pw_name


def get_puser_info():
    '''
    获取当前进程的用户信息
    '''
    return pwd.getpwuid(os.getuid())


def get_login_name():
    '''
    获取当前登录的用户名
    '''
    return os.getlogin()


def get_login_user_info():
    '''
    获取当前登录的用户信息
    '''
    return pwd.getpwnam(os.getlogin())


def check_user_is_create(name):
    try:
        pwd.getpwname(name)
        return True
    except Exception:
        return False

    return False
