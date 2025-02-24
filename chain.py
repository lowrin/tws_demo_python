from ib_async import *

import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("expand_frame_repr", False)

from pprint import pprint


def remove_tz_from_dataframe(df_in):
    df = df_in.copy()
    col_times = [
        col for col in df.columns if any([isinstance(x, pd.Timestamp) for x in df[col]])
    ]
    for col in col_times:
        df[col] = pd.to_datetime(df[col])
        df[col] = df[col].dt.tz_localize(None)
    return df


util.startLoop()

# quelle: https://nbviewer.org/github/ib-api-reloaded/ib_async/blob/main/notebooks/option_chain.ipynb


ib = IB()
ib.connect("127.0.0.1", 7497, clientId=12)

spx = Index("SPX", "CBOE")
ib.qualifyContracts(spx)

pprint(spx)

pprint("--------------------------")

ib.reqMarketDataType(4)

[ticker] = ib.reqTickers(spx)
pprint(ticker)

pprint("--------------------------")


spxValue = ticker.close
print("price: " + str(spxValue))

pprint("--------------------------")


chains = ib.reqSecDefOptParams(spx.symbol, "", spx.secType, spx.conId)

chains_df = util.df(chains)
pprint("chains")
pprint(chains_df)
pprint("--------------------------")

chain = next(c for c in chains if c.tradingClass == "SPXW" and c.exchange == "SMART")

strikes = [
    strike
    for strike in chain.strikes
    if strike % 5 == 0 and spxValue - 5 < strike < spxValue + 5
]
expirations = sorted(exp for exp in chain.expirations)[:3]
rights = ["P", "C"]

contracts = [
    Option("SPX", expiration, strike, right, "SMART", tradingClass="SPXW")
    for right in rights
    for expiration in expirations
    for strike in strikes
]

contracts = ib.qualifyContracts(*contracts)

print("contracts: " + str(len(contracts)))
pprint("--------------------------")

tickers = ib.reqTickers(*contracts)

print(tickers[0].modelGreeks)
pprint("--------------------------")

tickers_df = util.df(tickers)

tickers_df = remove_tz_from_dataframe(tickers_df)

tickers_df.to_excel("chain.xlsx")

ib.disconnect()
