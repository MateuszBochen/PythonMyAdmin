# -*- coding: UTF-8  -*-




class Controller:
    
    kernelObj = 0
    
    def __init__(self, kernel):        
        self.kernelObj = kernel
    
    def defaultRun(self):
        
        user = session.get('User');
        token = session.get('Token');
        baseName = session.get('BaseName');
        
        
        
        # pobieranie sesji
        session = self.kernelObj.autoloader.load('System.Http.Session');
        
        session.set('User', 'backen').set('Token', 'hwdp')
        
        
        
        return session.get('User')