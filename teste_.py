import os
import traceback
import pandas as pd
# with open('./2019-01-01-1546308539-https_get_443_certs/xaa','r') as f:
#     for l in f:
#         print(l.split(",")[1])

df = pd.read_csv('PublicAllIntermediateCertsWithPEMReport.csv',dtype={'PEM Info':str})
# df = pd.read_csv('MozillaIntermediateCerts.csv',dtype='str')
print(df.dtypes)
print(df['PEM Info'][0])
# print(df['PEM'][0])

