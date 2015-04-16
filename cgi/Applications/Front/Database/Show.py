# -*- coding: UTF-8  -*-




class Show:
    
    framework = 0
    
    def __init__(self, kernel):        
        self.framework = kernel
    
    def tablesRun(self):
        
        database = self.framework.module('System.Database.MySql');
        
        tables = database.query("SHOW TABLE STATUS")
       
        
        if(not type(tables).__name__ in ('list', 'tuple')):
            tables = []
                
        return self.framework.render('tables', {'tables': tables})