# -*- coding: UTF-8  -*-

import sys


class Autoloader:
    
    collections = {}
    kernelObj = 0
    
    additionalServices = {
        'System.Http.Header.Cookies': ['System.Http.Response'],
        'System.Database.MySql': ['System.Http.Session'],
        'System.Http.Session': ['System.Http.Header.Cookies']
    }
    
    def __init__(self, kernel):
         self.kernelObj = kernel
   
    
    def load(self, name, asNew = False, addKernel = False):
        
        if(name in self.collections and asNew == False):           
            return self.collections[name]       
        
        
        self.collections[name] = self.kernelObj.imortLib.import_module(name)
        services = []
        if(addKernel):
            services.append(self.kernelObj)
            
        if(name in self.additionalServices):                
            for service in self.additionalServices[name]:                    
                services.append(self.load(service))
            
        if(asNew):
            return getattr(self.collections[name], name.split('.')[-1])(*services)
        self.collections[name] = getattr(self.collections[name], name.split('.')[-1])(*services)
        
        return self.collections[name]
        
        
       
            
    def moduleExists(self, moduleName):     
        return True
        moduleName = moduleName.replace('.', '/')       
        return self.kernelObj.kernelOS.path.isfile(self.kernelObj.kernelOS.environ["PY_PATH"] +'/'+moduleName+'.py')
        
           