from ib_async import *

import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("expand_frame_repr", False)

util.startLoop()

# quelle: https://nbviewer.org/github/ib-api-reloaded/ib_async/blob/main/notebooks/ordering.ipynb


ib = IB()
ib.connect("127.0.0.1", 7497, clientId=12)


contract = Stock("MSFT", "SMART", "USD")

cds = ib.reqContractDetails(contract)

print(cds)


# action, quantity, price
order = LimitOrder("BUY", 100, 10.0)

limitTrade = ib.placeOrder(contract, order)

print(limitTrade)

# wait 15 seconds
ib.sleep(15)

print(limitTrade.log)


ib.disconnect()
