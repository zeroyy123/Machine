#coding=utf-8
import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fund_acq as fa
##import cvxopt as opt
##from cvxopt import blas, solvers

def MV_calculate(code):
    df = ts.get_hist_data(code)
    df.to_csv(code+'.csv')

    df = pd.read_csv(code+'.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    df = df.sort_index()

    df = df[['close','volume']]

    df['change'] = 100*(df['close']/(df['close'].shift(1)) - 1)
    df = df.dropna()
    return df




def data_gen():
    L = 700
    for i in range(len(code)):
        df = pd.read_csv(code[i]+'.csv')
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.sort_index()
        df['change'] = 100*(df['close']/df['close'].shift(1) - 1)
        df = df.dropna()
        if i == 0:
            ary = [(df['change'].values)[0:L]]

        else:
            ary = np.append(ary,[(df['change'].values)[0:L]],axis=0)

##    ary = np.asmatrix(ary)
    return ary

def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.rand(n)
    return k / sum(k)

def random_portfolio(returns):
    ''' 
    Returns the mean and standard deviation of returns for a random portfolio
    '''
    p = np.asmatrix(np.mean(returns, axis=1))
    w = np.asmatrix(rand_weights(returns.shape[0]))
    C = np.asmatrix(np.cov(returns))
    
    mu = np.float(w * p.T)
    sigma = np.float(np.sqrt(w * C * w.T))
    
    # This recursion reduces outliers to keep plots pretty
    if sigma > 1.9:
        return random_portfolio(returns)
    return mu, sigma, w


fa.get_fund_hist('233012')


code = ['sh','sz','hs300','sz50','zxb','cyb']
result = pd.DataFrame({'code':[],'mean':[],'var':[],'sharp':[]})
for i in range(len(code)):
    df = MV_calculate(code[i])
    out = pd.DataFrame({'code':[code[i]],'mean':[df['change'].mean()],'var':[df['change'].var()],'sharp':[df['change'].mean()/df['change'].var()]})
    result = result.append(out)


result = result.sort_values(by='mean',ascending=False)


return_vec = data_gen()
Mean = np.asmatrix(np.mean(return_vec, axis=1))
Var = np.asmatrix(np.cov(return_vec))
print Mean
print Var

n_portfolios = 1000  # 随机点数
means = []
stds = []
w_std_min = []
std_min = 2
for i in range(n_portfolios):
    r_m, r_s, w = random_portfolio(return_vec)
    means.append(r_m)
    stds.append(r_s)
    if r_s < std_min:  #最小值计算
        std_min = r_s
        w_std_min = w

print std_min
print np.float64(w_std_min)

plt.figure()
plt.plot(stds, means, 'o', markersize=5)
plt.grid(1)
plt.xlabel('std')
plt.ylabel('mean')
plt.title('Mean and standard deviation of returns of randomly generated portfolios')
plt.show()

