# -*- coding: UTF-8  -*-

import os, time



class Cookies:
    
    response = 0
    
    
    # cookie live time
    expires = 900 # 15 minut
    
    
    
    def __init__(self, responseObj):
        self.response = responseObj
    
    collection = {}
   
    # set cookie 
    # @param name cookie name
    # @param value cookie value    
    # @return  self
    def set(self, name, value):
        future = time.time()
        expires = time.strftime("%A, %d-%m-%Y %H:%M:%S %Z", time.gmtime(future + self.expires))
        self.response.setHeader("Set-Cookie:"+(name)+"="+(value)+";Expires="+(expires)+";Path=/")
       
        return self
        
    # get value from cookie
    # @param name cookie name
    # @return cookie value or empty string if cookie does not exist
    def get(self, name):
    
        if os.environ.has_key('HTTP_COOKIE'):
            for cookie in os.environ['HTTP_COOKIE'].split(';'):   
                cookie = cookie.strip(' \t\n\r/')
                cookie = cookie.split('=')
                if name == cookie[0]:
                    return cookie[1]
        return ''
        
        
    
     
    
        