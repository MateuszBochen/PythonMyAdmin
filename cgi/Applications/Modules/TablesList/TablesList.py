# -*- coding: UTF-8  -*-




class TablesList:
        
    def run(self, app):
        
        session = app.module('System.Http.Session')
        
        baseName = session.get('mysqlDatabase') 
        currentTable = session.get('mysqlActiveTable') 
        
        database = app.module('System.Database.MySql');
        
        ret = '';
        
        if(baseName != ''):
            tables = database.query("SHOW TABLES")
            
            ret = '<ul class="tabs vertical">'
            
            if(type(tables).__name__ in ('list', 'tuple')):
                for tableNames in tables:
                    ret += '<li class="'+('active' if(currentTable == tableNames[0]) else '' )+'"><a href="'+app.path('Tables/Show/struct/'+tableNames[0])+'">'+tableNames[0]+'</a></li>'
            
            ret += '</ul>'
            
        return ret