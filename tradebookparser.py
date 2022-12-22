import openpyxl


listofStocks ={}
listofCNCtransactions = {}
totalpnl = 0



# define a Trade class to store the buy and sell details for each trade
class Trade:
  def __init__(self, buy_price, buy_quantity, sell_price, sell_quantity,product):
    self.buy_price = buy_price
    self.buy_quantity = buy_quantity
    self.sell_price = sell_price
    self.sell_quantity = sell_quantity
    self.product = product


    
  

# define a Stock class to store the trades and PnL for each stock
class Stock:
  def __init__(self, name):      
    self.name = name
    self.trades = []
    self.pnl = 0
    self.cncPnl = 0
    listofStocks[self.name]=self
  
  def add_trade(self, trade):
    self.trades.append(trade)
  
  def calculate_pnl(self):  
    for trade in self.trades:
      if trade.product == "CNC":
        self.cncPnl += (trade.sell_price - trade.buy_price) * trade.sell_quantity
      else:
        self.pnl += (trade.sell_price - trade.buy_price) * trade.sell_quantity
    return self.pnl
# define a TradeBook class to store the stocks and their PnL
class TradeBook:
  def __init__(self):
    self.stocks = {}
    self.totalpnl =0
    self.winningtrades = 0
    self.losingtrades = 0
    self.winamount = 0
    self.lossamount = 0
    self.averageWinSize = 0
    self.averageLossSize = 0
    self.totalTrades = 0
    self.largestWinner = 0
    self. largestLoser = 0
    
  
  def add_stock(self, stock):
    if stock in self.stocks.keys():
      return
    else:
      self.stocks[stock] = stock
  
  def calculate_pnl(self):
    
    for stock in self.stocks.values():
      stockpnl = stock.calculate_pnl()
      self.totalTrades += 1
      self.totalpnl += stockpnl
      if (stockpnl)> 0: 
        self.winningtrades +=1
        self.winamount +=stockpnl 
        if stockpnl> self.largestWinner:
          self.largestWinner = stockpnl
      else:
        self.losingtrades +=1
        self.lossamount +=stockpnl
        if stockpnl< self.largestLoser:
          self.largestLoser = stockpnl
    self.averageLossSize = self.lossamount/self.losingtrades
    self.averageWinSize = self.winamount/self.winningtrades
        
    

# Open the Excel file
wb = openpyxl.load_workbook('trades.xlsx')

# Get the sheet with the trade data
ws = wb['trades']
# Extract the data from the sheet
perstock = {}
trades = []
buyPrice =  0
sellPrice = 0
tradebook = TradeBook()
for row in ws.iter_rows(min_row=2):  # Skip the first row with the column titles
    date = row[1].value
    quantity = int(row[5].value)
    price = int(row[6].value)
    fees = 20
    stock= row[3].value
    bs = row[2].value
    product = row[4].value
    if bs=='SELL':
      buyPrice = 0
      sellPrice = price
    else: 
      sellPrice = 0
      buyPrice = price
    if stock in listofStocks.keys():
      stk = listofStocks[stock]
    else:
      stk = Stock(stock)
    trade = Trade(buyPrice,quantity,sellPrice,quantity,product)
    stk.add_trade(trade)
    tradebook.add_stock(stk)
    
tradebook.calculate_pnl()

# print the PnL for each stock
for stock in tradebook.stocks.values():
  if(stock.pnl!=0):
    print(f"{stock.name}: {stock.pnl:,}")
    
  else:
    print(f"{stock.name}(D): {stock.cncPnl:,}")
print(f"Today's total PNL: {tradebook.totalpnl:,}")
print(f"Total Trades : {tradebook.totalTrades}")
print(f"# of Winning Trades: {tradebook.winningtrades}")
print(f"# of Losing trades : {tradebook.losingtrades}")
print(f"Average Win Per Trade : {tradebook.averageWinSize:,}")
print(f"Average Loss Per Trade : {tradebook.averageLossSize:,}")
print(f"Batting Average :{tradebook.totalpnl/tradebook.totalTrades:,}")
print(f'Strike Rate: {tradebook.averageWinSize/-tradebook.averageLossSize:,}R')


#TODO
#connect to DB
    
