ERROR: str = 'ERROR'
WARNING: str = 'WARNING'
INFO: str = 'INFO'
DEBUG: str = 'DEBUG'


def LOG(msg, level: str = DEBUG, logging=False):
    if logging:
        print(f'[{level}]: {msg}')
