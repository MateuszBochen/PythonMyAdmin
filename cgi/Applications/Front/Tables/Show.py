# -*- coding: UTF-8  -*-




class Show:
    
    framework = 0
    
    def __init__(self, kernel):        
        self.framework = kernel
    
    def structRun(self):
        
        
        session = self.framework.module('System.Http.Session')
        activeTable = self.framework.module('System.Http.URL').getSegment(3);
        
        
        
        columns = self.framework.module('System.Database.MySql').query("SHOW FULL COLUMNS FROM "+activeTable)
        
        #session.setNotice('success', str(columns))
        
        session.set('mysqlActiveTable', activeTable)
        
        if(not type(columns).__name__ in ('list', 'tuple')):
            columns = []
        
        return self.framework.render('', {'columns': columns, 'activeTable': activeTable})
        
    def browseRun(self):
        
        
        session = self.framework.module('System.Http.Session')
        activeTable = self.framework.module('System.Http.URL').getSegment(3);
        
        database = self.framework.module('System.Database.MySql')
        
        columns = database.query("SHOW COLUMNS FROM "+activeTable)
        records = database.query("SELECT * FROM `"+activeTable+"`")
        
        #session.setNotice('success', str(columns))
        
        session.set('mysqlActiveTable', activeTable)
        
        if(not type(columns).__name__ in ('list', 'tuple')):
            columns = []
            
        if(not type(records).__name__ in ('list', 'tuple')):
            records = []
        
        return self.framework.render('browse', {'columns': columns, 'activeTable': activeTable, 'records': records})