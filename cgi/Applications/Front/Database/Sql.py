# -*- coding: UTF-8  -*-




class Sql:
    
    framework = 0
    
    def __init__(self, kernel):        
        self.framework = kernel
    
    def defaultRun(self):
        
        return self.framework.render('makeSql', {})