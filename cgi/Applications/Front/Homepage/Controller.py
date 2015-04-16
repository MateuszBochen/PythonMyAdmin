# -*- coding: UTF-8  -*-




class Controller:
    
    framework = 0
    
    def __init__(self, kernel):        
        self.framework = kernel
    
    def defaultRun(self):
        # pobieranie sesji
        session = self.framework.module('System.Http.Session')
        
        mysqlUser = session.get('mysqlUser');        
        mysqlPassword = session.get('mysqlPassword')
        
        
        
       
        session.set('mysqlUser', mysqlUser);
        session.set('mysqlPassword', mysqlPassword);
            
        return self.framework.render('', {'message': session.get('mysqlUser')})
            
    def changeBaseRun(self):
        form = self.framework.module('System.Http.Header.Post')
        base = form.get('database')
        if(base != ''):
            session = self.framework.module('System.Http.Session')
            databases = self.framework.module('System.Database.MySql').query("SHOW DATABASES")
            if(len(databases) > 0):
                for bd in databases:
                    if(bd[0] == base):
                        session.set('mysqlDatabase', base)
                        session.setNotice('success', 'Database was changed')
                        break
                
        return self.framework.redirect(self.framework.path('Database/Show/tables'))