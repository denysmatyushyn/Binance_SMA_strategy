from sqlalchemy import create_engine
engine = create_engine('sqlite:///sma5min.bd')
TableCurrency = engine.execute('SELECT * FROM ETHUSDT')
for row in TableCurrency:
    print(row)
