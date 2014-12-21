import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

plt.rcdefaults()
odf = pd.read_csv("farequote_metrics.csv", dialect="excel", encoding="ISO-8859-1")
metric_names = odf.columns[1:]

training_size = 288

def fit_gm(samples):
    mu = np.average(samples)
    sig = np.std(samples)
    return [mu, sig]

def score(samples, model):
    mu = model[0]
    sig = model[1]
    p = []
    for s in samples:
        p.append((np.e ** -(((s-mu)**2)/(2*(sig**2))))/(np.sqrt(2*np.pi)*sig))
    return p

for i in range(0, len(s)):
    print(odf['avg_response_time'][i].astype('str') + "," + str(s[i]))