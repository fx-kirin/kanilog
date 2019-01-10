"""kanilog - """

__version__ = '0.1.0'
__author__ = 'fx-kirin <fx.kirin@gmail.com>'
__all__ = []


import logging
import sys
import logzero

DEFAULT_DATE_FORMAT = '%(color)s[%(levelname)1.1s|%(process)s|%(asctime)s %(name)s:%(threadName)s:%(module)s:%(lineno)d]%(end_color)s %(message)s'


def setup_logger(*args, **kwargs):
    if 'level' in kwargs:
        level = kwargs['level']
    else:
        level = logging.INFO
    if 'file_log_level' in kwargs:
        file_log_level = kwargs['file_log_level']
    else:
        file_log_level = logging.DEBUG

    root_log_level = file_log_level if file_log_level < level else level
    kwargs['level'] = root_log_level

    logzero.__name__ = ''
    root_logger = logzero.setup_logger('', disableStderrLogger=True, *args, **kwargs)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    if 'formatter' in kwargs:
        formatter = kwargs['formatter']
    else:
        formatter = logzero.LogFormatter(fmt=DEFAULT_DATE_FORMAT)
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)

    stderr_logger = logging.getLogger('STDERR')
    stderr_logger.propagate = False

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(level)
    stderr_handler.setFormatter(formatter)
    stderr_logger.addHandler(stderr_handler)

    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.setLevel(file_log_level)
            stderr_logger.addHandler(handler)


def get_stderr_logger():
    return logging.getLogger('STDERR')
