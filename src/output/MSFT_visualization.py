 To visualize the historical financial data, I'll use the plotly library in Python, which offers a wide range of chart types and customization options. I'll also use pandas, a popular data analysis library, to handle the data and the python-financial library to calculate financial metrics.

Here is the Python code:
```python
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from python_future import future_builtins

def get_data():
    revenue_data = {
        '2000': np.array([35317960, 33885121, 31653882, 29621563, 27789647, 26067735]),
        '2001': np.array([27546868, 24269286, 21092403, 18018720, 15553746, 13098789]),
        '2002': np.array([19267857, 16517689, 14197822, 12171340, 10428282, 8999241]),
        '2003': np.array([8614135, 7661573, 6719084, 5786616, 4905332, 4079667]),
        '2004': np.array([4328775, 3798488, 3322362, 2878304, 2471226, 2115053]),
        '2005': np.array([1948933, 1691541, 1464618, 1269434, 1094980, 931985]),
        '2006': np.array([1311644, 1153961, 999763, 851654, 708479, 569372]),
        '2007': np.array([850787, 717415, 609213, 513938, 422684, 334838]),
        '2008': np.array([488657, 409641, 336816, 272639, 217735, 168092]),
        '2009': np.array([168092, 140690, 115134, 90740, 66900, 43733]),
        '2010': np.array([191905, 164660, 139225, 115874, 93623, 72713]),
        '2011': np.array([181994, 156499, 132970, 112061, 90154, 68515]),
        '2012': np.array([170073, 147913, 125328, 107784, 89179, 70570]),
        '2013': np.array([131043, 109729, 93534, 78286, 63890, 49521]),
        '2014': np.array([78286, 63890, 49521, 72619, 66900, 53424]),
        '2015': np.array([66900, 53424, 43733, 336816, 272639, 217735], dtype='int'),
                    }
    ## Replace the dictionary with your actual revenue data
    midcap_rev = pd.DataFrame(revenue_data, index=[2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015])
    midcap_rev = midcap_rev.astype(float) / 1e6  ## Convert to millions
    return midcap_rev

def get_retrieve_data(type_data, years):
    if (type_data == 'dynamics' or type_data == 'Azure'):
        if (years == '1-year'):