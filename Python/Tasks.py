import csv
import pandas as pd
from polygon import RESTClient
client = RESTClient("uwl4mYiRMIv6nKMuB69hdzC6bLElul2U")

aggs = client.list_aggs(
    ticker="AAPL",
    multiplier=1,
    timespan="minute",
    from_="2025-01-01",
    to="2025-01-31"
)

data = []

for a in aggs:
    data.append({
        "open": a.open,
        "high": a.high,
        "low": a.low,
        "close": a.close,
        "volume": a.volume,
        "vwap": a.vwap,
        "timestamp": a.timestamp,
        "transactions": a.transactions
    })

df = pd.DataFrame(data)

df.to_csv("aapl_daily.csv", index=False)

print(df)