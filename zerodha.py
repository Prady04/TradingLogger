from jugaad_trader import Zerodha


class Zbroker():
  
  def __init__(self, username, pwd,twofa):        
   self.username = username
   self.pwd = pwd 
   self.twofa = twofa
   self.client = Zerodha(username, pwd, twofa)
   #print(self.client)
   
   
  def login(self):
     return self.client.login()
   
  def holdings(self):
     return self.client.holdings()
   
  def positions(self):
    return self.client.positions()
   
  def margin(self):
     return self.client.margin()['cash']