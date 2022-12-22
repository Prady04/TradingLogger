
import time
import os
import pandas as pd

import requests
from datetime  import datetime
import sqlite3

class ImportPatterns:
    def __init__(self,conn) -> None:
      
      
      self.scanner_names = []
      self.path_to_downloads = self._get_download_path()
      self.path_to_scans = os.path.join(self.path_to_downloads, 'Scans')
      self.db = conn
    
    
     
    def _get_download_path(self):
        """Returns the default downloads path for linux or windows"""
        if os.name == 'nt':
            import winreg
            sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'downloads')

    def _read_new_files(self):
        import datetime as dt
        import os.path, time

       
        
        #telegram_url = 'https://api.telegram.org/bot'+conf.telegram_bot_api_id+'/sendMessage?chat_id='+ conf.telegram_chat_id+'&text=Candlestick patterns '+ #datetime.now().strftime('%d/%m/%Y')
        #requests.post(telegram_url)
        download_path = self._get_download_path()
        
        files = [f for f in os.listdir(download_path) if 'Technical Analysis Scanner' in f]
      
        for file in files:
            lct = time.ctime(os.path.getctime(os.path.join(download_path, file)))
            file_date = datetime.strptime(lct, "%a %b %d %H:%M:%S %Y")
            print(file_date.strftime('%Y-%m-%d %H:%M:%S'))
            
           
            data = pd.read_excel(os.path.join(download_path, file), skiprows=[0])
            data = data.replace('&', '_', regex=True)
            symbols = data['Symbol'].to_list()
            
            #data['Symbol']+= ','
            name = file.split(',')[0]
            dato = file_date
            for symbol in symbols:                
                self.db.execute('insert into patterns(stock,pattern,pattern_date) values(?,?,?)',[symbol,name,dato])
        self.db.commit()
    
    
