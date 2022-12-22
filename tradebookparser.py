import pandas as pd
import numpy as np 
import math
import openpyxl 


df = pd.read_excel('pnl-DP2275.xlsx',sheet_name='Equity',header=36)
print(df[['Symbol','Realized P&L']])
print(df['Realized P&L'].sum())
exit()
data = pd.read_csv('tradebook-DP2275-EQ.csv')
data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
data['trade_type'] =  data['trade_type'].replace('buy','BUY')
data['trade_type'] =  data['trade_type'].replace('sell','SELL')

groupby_symbol = data.groupby('symbol')
INDEX = 0
ALL_DICT = {}
for symbol in groupby_symbol.groups:
    ALL_DICT[INDEX] = {}
    ALL_DICT[INDEX]['SYMBOL'] = symbol
    symbol_df = groupby_symbol.get_group(symbol)
    
    
    groupby_symbol_transct = symbol_df.groupby('trade_type')
    
      
    
    buy = 0
    sell = 0
    try:
      symbol_sell_df = groupby_symbol_transct.get_group('SELL')
    except Exception as e:
      sell = -1
      sell_avg = 0
      sell_quantity =0
      continue
    try:
      symbol_buy_df = groupby_symbol_transct.get_group('BUY')
    except Exception as e:
      buy = -1
      buy_avg=0
      buy_quantity=0
      continue
    
    
    ###
    if buy != -1:
      buy_quantity = symbol_buy_df['quantity'].sum()
      buy_sum = (symbol_buy_df['price'] * symbol_buy_df['quantity']).sum()
      buy_avg = np.round(buy_sum/buy_quantity,0)
    ALL_DICT[INDEX]['BUY_QUANTITY'] = buy_quantity
    ALL_DICT[INDEX]['BUY_AVG'] = buy_avg
     
    
    if sell != -1:
      sell_quantity = symbol_sell_df['quantity'].sum()
      sell_sum = (symbol_sell_df['price'] * symbol_sell_df['quantity']).sum()
      sell_avg = np.round(sell_sum/sell_quantity,0)
    ALL_DICT[INDEX]['SELL_QUANTITY'] = sell_quantity
    ALL_DICT[INDEX]['SELL_AVG'] = sell_avg
    ALL_DICT[INDEX]['PROFIT'] = sell_avg *sell_quantity - buy_avg * buy_quantity
    
    INDEX+=1

df = pd.DataFrame.from_dict(ALL_DICT,orient='index')
print(df[df['BUY_QUANTITY'] != df['SELL_QUANTITY']]) # Open Positions
print(df[df['BUY_QUANTITY'] == df['SELL_QUANTITY']]) # Closed Positions)

closed_pos = df[df['BUY_QUANTITY'] == df['SELL_QUANTITY']]
buy_amt = (df['BUY_QUANTITY']*df['BUY_AVG']).sum()
sell_amt = (df['SELL_QUANTITY']*df['SELL_AVG']).sum()
a= (sell_amt - buy_amt)/buy_amt*100
print("{:.2f}%".format(a))
pd.DataFrame.to_csv(df,'trades.csv')


