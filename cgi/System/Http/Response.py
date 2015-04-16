# -*- coding: UTF-8  -*-

import sys, os

class Response:
        
    
    headersCollection = []
    
    
    def httpResponse(self):
        for x in self.headersCollection:
            print x
        print "Content-type: text/html;  charset: UTF-8; \n\n"
        
        
        
    def redirect(self, url):
        
        print "Location: http://"+os.environ['SERVER_NAME']+url+"\n"
        print "Connection: close\n"
        sys.exit(1)
        return False
        
    def setHeader(self, header):
        self.headersCollection.append(header)
        return self
    
    def redirectToLastUrl(self):
        #print "Content-type: text/html;  charset: UTF-8; \n\n"
        print "Location: "+os.environ['HTTP_REFERER']+"\n"
        print "Connection: close\n"
        sys.exit(1)
        return False
        
    def getLastUrl(self):
        #print "Content-type: text/html;  charset: UTF-8; \n\n"
        if('HTTP_REFERER' in os.environ):
            return os.environ['HTTP_REFERER']
        else:
            return ""
        