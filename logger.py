#!/home/admin/broker_project/build_tools/python272/bin/python
#-*- coding:utf-8 -*-

'''logger.py'''

import logging
from logging.handlers import RotatingFileHandler


'''
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

#file_handler = logging.FileHandler('test.log')
#file_handler.setLevel(logging.DEBUG)
#文件回滚，每个文件最大400个字节，最大回滚3个文件
file_handler = RotatingFileHandler('myapp.log', maxBytes = 400, backupCount = 10)
file_handler.setLevel(logging.DEBUG)

#stream_handler = logging.StreamHandler()
#stream_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(message)s')

file_handler.setFormatter(formatter)
#stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
#logger.addHandler(stream_handler)
'''
class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class Logger(Singleton):
    def __init__(self):
        self.__log = None
        self.__hdlr = None


    def __del__(self):
        self.close()

    '''
    introduction: 
        get instance of loggger
    @parameter:
        log_instance: id of logger
        file_name: name you are going to produce
        max_bytes: capacity of file
        backup_count: rollback number of file
        timeopen: 0 -----close, others -----open

    return:
        0 ----- success
        -1 ----- failure
    '''
    def get_log(self, log_instance, file_name, max_bytes, backup_count, timeopen = 0):
        result = 0
        try:
            self.__log = logging.getLogger(log_instance)
        except:
            self.__log = None
            result = -1
        else:
            # print id(self.__log)
            self.__log.setLevel(logging.DEBUG)
            try:
                self.__hdlr = RotatingFileHandler(file_name, maxBytes = max_bytes, backupCount = backup_count)
            except:
                self.__hdlr = None
                result = -1
            else:
                self.__hdlr.setLevel(logging.DEBUG)
                formatter = None
                if 0 != timeopen:
                    formatter = logging.Formatter('%(asctime)s - %(message)s')
                else:
                    formatter = logging.Formatter('%(message)s')
                self.__hdlr.setFormatter(formatter)
                self.__log.addHandler(self.__hdlr)
        finally:
            return result

    def write(self, value):
        if None != self.__log and None != self.__hdlr:
            self.__log.debug(value)

    def flush(self):
        if None != self.__hdlr:
            self.__hdlr.flush()

    def close(self):
        if None != self.__log:
            self.__log.removeHandler(self.__hdlr)
            self.__log = None

        if None != self.__hdlr:
            self.__hdlr.flush()
            self.__hdlr.close()
            self.__hdlr = None


if __name__ == '__main__':

    num = 1000
    name = 'bad boy'
    # fo = 19.9
    log = Logger()
    if(0 != log.get_log('one', 'test.log', 1000, 3, 1)):
        print 'logger get instance failure'
    # log1 = Logger()
    # if(0 != log1.get_log('one677', 'test1.log', 1000, 3, 1)):
    #     print 'error'
    # print id(log)
    # print id(log1)
    # print log == log1
    
    # if(0 != log1.get_log('one', 'test.log', 50, 3)):
    #     print 'logger get instance failure'
    log.write('num:%d name:%s'%(num,name))
    log.write('123456789413252')
    # log.close()
    # log1.write('yes or no')
    # log1.flush()
    # log1.close()
    log.write('zaiciaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    log.flush()

    log.write('return = ok: \n'+name)
    log.flush()


    log.close()
    
