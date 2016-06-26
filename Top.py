#coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import fund_acq as fa

fa1 = fa.fund_acq()

symbol = ['233009','233005']



[df1,mean1,var1] = fa1.get_weeks_hist(symbol[0])
[df2,mean2,var2] = fa1.get_weeks_hist(symbol[1])

datas = [df1['change'].values,df2['change'].values]

L_min = 1000
for data in datas:
    if len(data) < L_min:
        L_min = len(data)

for i in range(len(datas)):
    datas[i] = datas[i][len(datas[i])-L_min:len(datas[i])]
    print len(datas[i])

d_cov = np.cov(datas)*56

print d_cov

plt.figure()
plt.hist(df1['change'].values,bins=50)
plt.grid(1)


plt.figure()
plt.hist(df2['change'].values,bins=50)
plt.grid(1)
plt.show()


