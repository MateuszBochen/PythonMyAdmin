# -*- coding: UTF-8  -*-

import cgi

import os, sys

class Post:
        
   
    
    postArray = []
    
    def __init__(self):
        
        os.getenv("QUERY_STRING")      
        queryString = self.addslashes(sys.stdin.read())
        self.postArray = cgi.parse_qs(queryString, True)
    
    def get(self, name, returnAlwaysAsArray = False):
        indexes = name.split('.')
        
        #print "Content-type: text/html;  charset: UTF-8; \n\n"
        
        #print self.postArray
        #print indexes
        return self.getFromArray(indexes, 0, returnAlwaysAsArray)
    
    
    def getListByIndex(self, name, index, returnAlwaysAsArray = False):
        list = self.get(name, returnAlwaysAsArray)
        if(type(list).__name__ == 'list' and len(list) > index):
            return self.addslashes(list[index])
        elif(list != ''):                
            return list
        else:
            return ''
    
        
    def debug(self):
        return self.postArray
        
    def addslashes(self, s):
        if(s is None):
            return None
        l = ["\\", '"', "'", "\0", ]
        for i in l:
            if i in s:
                s = s.replace(i, '\\'+i)
        return s
        
    def getFromArray(self, index, nbi = 0, returnAlwaysAsArray = False):
       
        if index[nbi] in self.postArray:
            
            if(type(self.postArray[index[nbi]]).__name__ == 'list' and (nbi+1 in index)):
                return  self.getFromArray(self.postArray[index[nbi]], index, nbi+1, returnAlwaysAsArray);
            else:
                if(returnAlwaysAsArray == False and len(self.postArray[index[nbi]]) == 1):
                    return self.postArray[index[nbi]][0]
                else:
                    return self.postArray[index[nbi]]

        return '';
