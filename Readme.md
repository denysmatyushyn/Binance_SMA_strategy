**The simple SMA strategy.**

The strategy shows the simple principle of algorithmic trading. 
Two SMA lines with periods 7 and 25 are used. Assets are sold when the fast line crosses the slow line from up to down. And reverse signal make a purchase of asset.
You can use different types of assets like BTC, ETH, etc.
Technical stack:
Python, Binance API, SQL, Websockets.
Do not forget to input your API KEY and API SECRET of your Binance account.

**NOTICE: The strategy shows only principles of algorithmic trading and did not be tested for getting profit.**  

To run this:
- `pip3 install -r requirements.txt`

To use it:  
- Example of running `python BinanceSMAstrategy.py`