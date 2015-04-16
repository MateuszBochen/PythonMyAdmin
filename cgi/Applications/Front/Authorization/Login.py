# -*- coding: UTF-8  -*-


class Login:
        
    
    framework = 0
    
    def __init__(self, app):        
        self.framework = app
        
    def defaultRun(self):
        
        message = ''
        type = 'alert'
        
        form = self.framework.module('System.Http.Header.Post');
        database = self.framework.module('System.Database.MySql');
        
        session = self.framework.module('System.Http.Session');
        
        
        
        user = form.get('login')
        password = form.get('password')    
        host = self.framework.config('MYSQL_HOST')
        port = self.framework.config('MYSQL_PORT')
        
        if(user and password and host and port):
            if(database.connect(host, user, password, port)):
                message = 'Zostałeś połączony z bazą'
                type = 'success'
                session.set('mysqlUser', user)
                session.set('mysqlPassword', password)
                
                return self.framework.redirect(self.framework.path(''))
                
            else:
                message = 'Unable to connect to mysql database'
                    
        #return self.framework.render('', {'message': session.debug(), 'type': type}, 'clear')
        return self.framework.render('', {'message': message, 'type': type}, 'clear')