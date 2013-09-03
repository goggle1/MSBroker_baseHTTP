#!../tools/python27/bin/python
#-*- coding:utf-8 -*-
import time
import traceback
from logger import *
import os

log = Logger()
if 0 != log.get_log("one",os.path.dirname(__file__)+"/examplelog.log",500*1024*1024,3,1):
    print "logger get instance failure"

class example_1:
    def start(self,input_dic):

        result_flag = 0
        try:

            print input_dic
            output_dic=input_dic

            result_string = "ms/ms1/example_1: " + str(output_dic)
          
        except:
            result_flag = -1
            print "example_delay: start error"
            print traceback.format_exc()
            log.write("example_delay: start error")
            log.write(traceback.format_exc())
            log.flush()

        finally:
            if 0==result_flag:
                return (result_flag,result_string)
            else:
                return (result_flag,None)

        
'''http://ip:11000/ms/ms1/example_1?a=1&b=2&a=3'''
