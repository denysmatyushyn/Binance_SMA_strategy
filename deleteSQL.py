from sqlalchemy import create_engine
engine = create_engine('sqlite:///sma5min.bd')
engine.execute('DROP table IF EXISTS ETHUSDT')