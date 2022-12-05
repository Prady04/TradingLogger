
class User:
    def __init__(self, user_id, username, password):
        self.phonenumber = user_id
        self.username = username
        self.password = password

class Entry:
    def __init__(self, entry_id, user, symbol, date,ordertype,qty, notes,sl,price):
        self.entry_id = entry_id
        self.phonenumber = user.phonenumber
        self.symbol = symbol
        self.date = date
        self.transaction_type = ordertype
        self.quantity = qty
        self.notes = notes
        self.SL =sl
        self.price = price
     