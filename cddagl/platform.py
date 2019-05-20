import sys


def sys_name():
    if sys.platform.startswith('linux'):
        return 'Linux'
    if sys.platform in ('win32', 'cygwin'):
        return 'Windows'
    if sys.platform == 'darwin':
        return 'Mac'
    raise RuntimeError("Unknown platform")


def is_linux():
    """
    :return: True if the current OS is Linux, False otherwise
    """
    return sys_name() == 'Linux'


def is_windows():
    """
    :return: True if the current OS is Windows, False otherwise
    """
    return sys_name() == 'Windows'


def is_mac():
    """
    :return: True if the current OS is macOS, False otherwise
    """
    return sys_name() == 'Mac'
