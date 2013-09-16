#!../tools/python27/bin/python
#-*- coding:utf-8 -*-
import string
import commands

class disks:
    response = ''
    
    CMD_1 = "df -a | grep /media" 
        
    #def start(self, request):
    def start(self, input_dic):
        result = 0
        detail = 0
        self.response = ''
                
        '''
        if 'detail' in input_dic:
            if(len(input_dic['detail']) > 0):
                try:
                    detail = string.atoi(input_dic['detail'][0])
                except:
                    self.response += 'unsupport detail: [%s], only num [0, 1], default detail=0\n' % (input_dic['detail'][0])      
                    detail = 0
        if(detail <0) or (detail > 1):
            self.response += 'detail out of range: [%d], only [0, 1], default detail=0\n' % (detail)
            detail = 0
        '''   
        
        (status, output) = commands.getstatusoutput(self.CMD_1)
        if(status != 0):
            result = -1
            self.response += 'internal error!'
        else:
            result = 0
            self.response += output
        
    
        #request.write(self.response)
        if 0==result:
            return (result, self.response)
        else:
            return (result, None)