from ib_async import *

import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("expand_frame_repr", False)

util.startLoop()

# quelle: https://nbviewer.org/github/ib-api-reloaded/ib_async/blob/main/notebooks/ordering.ipynb


ib = IB()
ib.connect("127.0.0.1", 7497, clientId=12)







ib.disconnect()
