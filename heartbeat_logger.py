# encoding=utf8
#################################################
import logging
import os
import datetime

class HeartbeatLogger(logging.Logger):
    def __init__(self, name, directory, level=logging.INFO):
        logging.Logger.__init__(self, name, level)
        rotate_handler = DatetimeFileHandler(directory=directory, flag=name)
        fmt_str = '%(asctime)s %(process)d %(module)s.%(funcName)s.%(lineno)d %(levelname)s : %(message)s'
        fmt = logging.Formatter(fmt_str, datefmt='%Y-%m-%d %H:%M:%S')
        rotate_handler.setFormatter(fmt)
        self.addHandler(rotate_handler)

class DatetimeFileHandler(logging.StreamHandler):
    """
    A handler which records the logrecords of all the levels, stored in directories and files which named by datetime.
    @flag  文件名的后缀
    """

    def __init__(self, directory, mode='a',flag = ''):
        self.mode = mode
        self.directory = directory
        self.flag = flag
        logging.StreamHandler.__init__(self, self._open())

    def close(self):
        """
        Closes the stream.
        """
        self.acquire()
        try:
            if self.stream:
                self.flush()
                if hasattr(self.stream, "close"):
                    self.stream.close()
                logging.StreamHandler.close(self)
                self.stream = None
        finally:
            self.release()

    def _open(self):
        now  = datetime.datetime.now()
        log_directory = self.directory + '/' + '%04d-%02d'%(now.year, now.month)
        os.system("mkdir -p %s"%log_directory)
        log_file = log_directory + '/' + '%s.%s.log'%(now.day,self.flag)
        stream = open(log_file, self.mode)
        return stream

    def emit(self, record):
        """
        Emit a record.

        If the stream was not opened because 'delay' was specified in the
        constructor, open it before calling the superclass's emit.
        """
        if self.stream is None:
            self.stream = self._open()
        logging.StreamHandler.emit(self, record)
        self.close()

if __name__== "__main__":
    logger = HeartbeatLogger('her', ".")
    print logger.error('hello')
