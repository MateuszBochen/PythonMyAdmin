# -*- coding: UTF-8  -*-

import os,string
from System.Templating import airspeed


class Templating:
    
    viewReady = ''
    
    mainFile = 'index.html'
    
    app = 0
    
    def __init__(self, app):
        self.app = app
    
    def setMainFile(self, fileName):
        self.mainFile = fileName+'.html'
    
    
    def render(self, template, data):
        
        content = ''
        
        partFile = 'index'
        if(template !=''):
            partFile = template
        
        fw = self.app.framework   
        successNoticcess = ''
        errorNoticcess = ''
        errorSecondary = ''
        
        myPath = os.environ["PY_PATH"].replace(os.path.dirname(os.environ["SCRIPT_NAME"]), '')
        
       
        
        # część szablonu
        if(myPath == ''):
            partPath = self.app.config['TEMPLATE_DIRECTORY'] +'/'+self.app.config['TEMPLATE_DIR']+'/'+self.app.config['TEMPLATE_NAME']+'/Apps/'+self.app.appName+'/'+self.app.controller+'/'+partFile+'.html'
            mainPath = self.app.config['TEMPLATE_DIRECTORY'] +'/'+self.app.config['TEMPLATE_DIR']+'/'+self.app.config['TEMPLATE_NAME']+'/'+self.mainFile
        else:
            partPath = myPath+'/'+self.app.config['TEMPLATE_DIRECTORY'] +'/'+self.app.config['TEMPLATE_DIR']+'/'+self.app.config['TEMPLATE_NAME']+'/Apps/'+self.app.appName+'/'+self.app.controller+'/'+partFile+'.html'
            mainPath = myPath+'/'+self.app.config['TEMPLATE_DIRECTORY'] +'/'+self.app.config['TEMPLATE_DIR']+'/'+self.app.config['TEMPLATE_NAME']+'/'+self.mainFile
        
        if(os.path.isfile(partPath)):
            size = os.path.getsize(partPath)
            templateString = open(partPath).read(size)
            t = airspeed.Template(templateString)
            content = t.merge(locals())
        else:
            content = 'Taki widok nie istnieje <b>'+partPath+'</b>'
        
        # pobieranie noticów
        session = fw.module('System.Http.Session')
        notices = session.getNotices()
        session.clearNotices()       
        
        if(type(notices).__name__ == 'list'):
            for notice in notices:
                
                if(notice[0] == 'alert'):
                    errorNoticcess += '<p>'+notice[1]+'</p>'
                elif(notice[0] == 'success'):
                    successNoticcess += '<p>'+notice[1]+'</p>'
                else:
                    errorSecondary += '<p>'+notice[1]+'</p>'
        
        # główny plik szablonu
        if(os.path.isfile(mainPath)):
           size = os.path.getsize(mainPath)
           templateString = open(mainPath).read(size)
           
           t = airspeed.Template(templateString)
           
           self.viewReady = t.merge(locals())
            
        else:
            self.viewReady = 'Taki szablom nie istnieje '+mainPath
    
    def display(self):
        print self.viewReady
        
        
    #def extract(self, data):
        
        
    