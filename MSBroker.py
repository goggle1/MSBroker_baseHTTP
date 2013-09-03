#!/home/admin/broker_project/build_tools/python272/bin/python
#-*- coding:utf-8 -*-

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from logger import *
import threading
import urlparse
import sys
import traceback
import time
import socket

msbroker_log = Logger()
if 0 != msbroker_log.get_log("one","msbrokerlog.log",1024*1024*1024,3,1):
    print "logger get instance failure"   

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            url_info_dic = self.__parse_uri()
            if None == url_info_dic:
                raise Exception()
            
            tStart = time.time()

            result_string = self.__execute_module(url_info_dic)
            if None == result_string:
                print "executing module returns incorrect results"
                msbroker_log.write("executing module returns incorrect results")
                msbroker_log.flush()
                raise Exception()

            tEnd = time.time()
            self.__print_execute_module_cost_time(tStart,tEnd)

            self.__send_message_to_client(result_string)

        except:
            print "Handler: do_GET error"
            print traceback.format_exc()
            msbroker_log.write("Handler: do_GET error")
            msbroker_log.write(traceback.format_exc())
            msbroker_log.flush()
            self.send_error(404)
            
        finally:
            return

    ''' **********parse url***********'''    
    def __parse_uri(self):
        result_flag = 0
        try:
            url_info_dic = {}

            parsed_uri = urlparse.urlparse(self.path)

            url_info_dic["module_path"] = self.__divide_module_path(parsed_uri.path)
            if None == url_info_dic["module_path"]:
                raise Exception()

            url_info_dic["args"] = self.__divide_args(parsed_uri.query)
            if None == url_info_dic["args"]:
                raise Exception()

        except:
            result_flag = -1
            print "Handler: __parse_uri error"
            print traceback.format_exc()
            msbroker_log.write("Handler: __parse_uri error")
            msbroker_log.write(traceback.format_exc())
            msbroker_log.flush()
        finally:
            if result_flag == 0:
                return url_info_dic
            else:
                return None

    def __divide_module_path(self,module_path_string):
        result_flag = 0
        try:
            module_path_list = module_path_string.strip("/").split("/")


        except:
            result_flag = -1
            print "Handler: __divide_module_path error"
            print traceback.format_exc()
            msbroker_log.write("Handler: __divide_module_path error")
            msbroker_log.write(traceback.format_exc())
            msbroker_log.flush()
        finally:
            if result_flag == 0:
                return module_path_list
            else:
                return None


    def __divide_args(self,args_string):
        result_flag = 0
        try:
            args_dic = {}

            parameter_string_list = args_string.split('&')
            if 0!=len(parameter_string_list):
                for i in range(0,len(parameter_string_list)):
                    each_parameter_info = parameter_string_list[i].split('=')
                    if 1<len(each_parameter_info):
                        if each_parameter_info[0] in args_dic: #one parameter has multi value
                            args_dic[each_parameter_info[0]].append(each_parameter_info[1])
                        else:
                            args_dic[each_parameter_info[0]] = [each_parameter_info[1]]
                            

        except:
            result_flag = -1
            print "Handler: __divide_args error"
            print traceback.format_exc()
            msbroker_log.write("Handler: __divide_args error")
            msbroker_log.write(traceback.format_exc())
            msbroker_log.flush()
        finally:
            if result_flag == 0:
                return args_dic
            else:
                return None


    ''' **********load module and execute_module***********'''  
    def __execute_module(self,url_info_dic):
        result_flag = 0
        try:
            complete_module_path = 'module'
            for path_i in url_info_dic["module_path"]:
                complete_module_path = complete_module_path + "." + path_i

            print "*****************************************"
            print "***** Load '%s.py' "%complete_module_path
            print "*****************************************"
            msbroker_log.write("*****************************************")
            msbroker_log.write("***** Load '%s.py' "%complete_module_path)
            msbroker_log.write("*****************************************")
            msbroker_log.flush()

            
            if complete_module_path in sys.modules:
                del sys.modules[complete_module_path]

            complete_module = __import__(complete_module_path)

            graded_module_object = []
            for i in range(0,len(url_info_dic["module_path"])):
                if 0 == i:
                    graded_module_object.append(getattr(complete_module,url_info_dic["module_path"][i]))
                else:
                    graded_module_object.append(getattr(graded_module_object[i-1],url_info_dic["module_path"][i]))

            Module_Class_obj = getattr(graded_module_object[i],url_info_dic["module_path"][i])()
            
            '''execute_module'''
            input_dic = url_info_dic["args"]
            (module_result_flag,module_result_string) = Module_Class_obj.start(input_dic)
            if 0!= module_result_flag:
                print "Module_Class_obj.start error"
                msbroker_log.write("Module_Class_obj.start error")
                msbroker_log.flush()
                raise Exception()

        except:
            result_flag = -1
            print "Handler: __execute_module error"
            print traceback.format_exc()
            msbroker_log.write("Handler: __execute_module error")
            msbroker_log.write(traceback.format_exc())
            msbroker_log.flush()
        finally:
            if result_flag == 0:
                return module_result_string
            else:
                return None
    

    ''' **********send message to client***********''' 
    def __send_message_to_client(self,result_string):

        self.send_response(200)
        #self.send_header("Content-type", "text/plain")
        self.send_header("Content-length",str(len(result_string)))
        self.end_headers()
        self.wfile.write(result_string)


    ''' **********print cost time***********''' 
    def __print_execute_module_cost_time(self,tStart,tEnd):
        t_cost_sec = tEnd - tStart
        t_cost_min = t_cost_sec/60
        print "----------------------------------------------"
        print "The Module cost %f seconds,"%(t_cost_sec)
        print "that is %f minutes."%(t_cost_min)
        print "----------------------------------------------"
        msbroker_log.write("----------------------------------------------")
        msbroker_log.write("The Module cost %f seconds,"%(t_cost_sec))
        msbroker_log.write("that is %f minutes."%(t_cost_min))
        msbroker_log.write("----------------------------------------------")
        msbroker_log.flush()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class PreTreatment:
    def __init__(self):
        self.localIP = ''
    
    def get_localIP(self):
        result_flag = 0
        try:
            if sys.platform.startswith('win'):
                self.localIP = socket.gethostbyname(socket.gethostname())
            elif sys.platform.startswith('linux'):
                import fcntl
                import struct
                self.localIP = __get_linux_ip_address("eth0")
            else:
                raise Exception()
        except:
            result_flag = -1
            print "PreTreatment: get_localIP error"
            print traceback.format_exc()
            msbroker_log.write("PreTreatment: get_localIP error")
            msbroker_log.write(traceback.format_exc())
            msbroker_log.flush()
        finally:
            return

    def __get_linux_ip_address(self,ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

if __name__ == '__main__':
    try:
          
        pre_treatment = PreTreatment()
        pre_treatment.get_localIP

        server = ThreadedHTTPServer((pre_treatment.localIP, 11000), Handler)
        print 'Starting server, use <Ctrl-C> to stop'
        server.serve_forever()

    except:
        print traceback.format_exc()
   
