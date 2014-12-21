import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import time
import datetime
import math
plt.rcdefaults()
import influxdb_conn

df = pd.read_csv("farequote.csv", dialect="excel", encoding="ISO-8859-1")
df['ts'] = df['time'].apply(lambda t:  datetime.datetime.fromtimestamp(math.floor(time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%SZ"))/300)*300))

def percentile(n):
    def percentile_(x):
        return np.percentile(x, n)
    percentile_.__name__ = 'percentile_%s' % n
    return percentile_

#global metrics
mdf = df.groupby('ts').agg({'responsetime':{np.min, np.max, np.mean, percentile(50), percentile(95), 'count'}})

df1 = pd.DataFrame(data=list(range(30)),index=pd.date_range(start='2014-11-16', periods=30, freq='H'))
influxdb_conn.init()
client = influxdb_conn.get_df_client()
client.write_points({'responsetime':mdf['responsetime']})
