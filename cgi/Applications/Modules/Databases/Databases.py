# -*- coding: UTF-8  -*-




class Databases:
    
    
    def run(self, app):
       
        
        database = app.module('System.Database.MySql');
        
        databases = database.query("SHOW DATABASES")
        
        ret = '<form action="'+(app.path('Homepage/Controller/changeBase'))+'" method="post" >'
        ret += '<fieldset><div class="row" ><div class="columns nine" >'
            
        
        ret += '<select name="database" id="database" onchange="submit();" ><option value="" >Select a database</option>'
        
        baseName = app.module('System.Http.Session').get('mysqlDatabase') 
        
        if(len(databases) > 0):
            for(base) in databases:
                ret += '<option value="'+str(base[0])+'" '+('selected="selected"' if(baseName == str(base[0])) else '' )+' >'+str(base[0])+'</option>'
        ret += '</select></div></div>'
        ret += '</fieldset></form>'
        return ret