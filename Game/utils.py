ERROR: str = 'ERROR'
WARNING: str = 'WARNING'
INFO: str = 'INFO'
DEBUG: str = 'DEBUG'


def LOG(msg, level: str = DEBUG, log=False):
    if log:
        print(f'[{level}]: {msg}')
