#encoding=utf8
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s [%(filename)s:%(lineno)s] %(message)s '
                    )
info = logging.info
debug = logging.debug
error = logging.error
warn = logging.warn
fatal = logging.fatal
exception = logging.exception