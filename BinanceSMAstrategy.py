import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from binance.client import Client
import unicorn_binance_websocket_api as unicorn


def GetHistoricalData(symbol, interval, lookback):
    HistoricalFrame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback +' day ago UTC'))
    HistoricalFrame = HistoricalFrame.iloc[:,:5]
    HistoricalFrame.columns = ['Time', 'Open', 'High', 'Low', 'Close']
    HistoricalFrame.Time = pd.to_datetime(HistoricalFrame.Time, unit='ms')
    HistoricalFrame = HistoricalFrame.astype({col: float for col in HistoricalFrame.columns[1:]})
    return HistoricalFrame


def GetRealTimeData(RealTimeData):
    if RealTimeData['kline']['is_closed']:
        Time = pd.to_datetime(RealTimeData['event_time'], unit='ms')
        OpenPrice = float(RealTimeData['kline']['open_price'])
        HighPrice = float(RealTimeData['kline']['high_price'])
        LowPrice = float(RealTimeData['kline']['low_price'])
        ClosePrice = float(RealTimeData['kline']['close_price'])
        RealTimeFrame = pd.DataFrame({'Time': Time, 'Open': OpenPrice, 'High': HighPrice, 'Low': LowPrice,
                                      'Close': ClosePrice}, index=[0])
        RealTimeFrame.to_sql(TypeCurrency, engine, index=False, if_exists='append')


def main():
    while True:
        OnlineData = ubwa.pop_stream_data_from_stream_buffer()
        if OnlineData and len(OnlineData) > 3:
            GetRealTimeData(OnlineData)
            DataForCalculation = pd.read_sql(TypeCurrency, engine)
            DataForCalculation['SMA1'] = DataForCalculation['Close'].rolling(window=7, min_periods=1).mean()
            DataForCalculation['SMA2'] = DataForCalculation['Close'].rolling(window=25, min_periods=1).mean()
            DataForCalculation['Rules'] = np.where(DataForCalculation['SMA1'] > DataForCalculation['SMA2'], 1, 0)
            DataForCalculation['Diff'] = DataForCalculation.Rules.diff().fillna(0).astype(int)
            if DataForCalculation['Diff'].iloc[-1] == 1:
                try:
                    order = client.order_market_buy(symbol=TypeCurrency, quantity=0.0085)
                except:
                    print('Error 2010')
                    continue
            elif DataForCalculation['Diff'].iloc[-1] == -1:
                try:
                    order = client.order_market_sell(symbol=TypeCurrency, quantity=0.0085)
                except:
                    print('Error 2010')
                    continue


if __name__ == "__main__":
    API_KEY = 'Your_API_KEY'
    API_SECRET = 'Your_API_SECRET'
    TypeCurrency = 'ETHUSDT'
    TimeInterval = Client.KLINE_INTERVAL_5MINUTE
    HistoryFrame = '1'
    TimeForLiveInterval = 'kline_5m'

    client = Client(API_KEY, API_SECRET)
    engine = create_engine('sqlite:///sma5min.bd')
    HistoryForSQL = GetHistoricalData(TypeCurrency, TimeInterval, HistoryFrame)
    HistoryForSQL.to_sql(TypeCurrency, engine, index=False, if_exists='append')

    ubwa = unicorn.BinanceWebSocketApiManager(exchange='binance.com')
    ubwa.create_stream(TimeForLiveInterval, TypeCurrency, output='UnicornFy')

    main()
