#coding=utf-8
import urllib
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class fund_acq():
    # def __init__(self):


    def getHtml(self,url):
        page = urllib.urlopen(url)
        html = page.read()
        return html

    def get_fund_hist(self,symbol):
        html = self.getHtml("http://stockjs.finance.qq.com/fundUnitNavAll/data/year_all/"+symbol+".js")
        html = html.split('":')
        html = html[2].split(', "n')
        html = html[0].replace('"','')
        html = html.replace(',',' ')
        html = html.replace('[[','[')
        html = html.replace(']  [',']aaaa[')
        html = html.split('aaaa')
        for i in range(len(html)):
            html[i] = html[i].replace('[','')
            html[i] = html[i].replace(']','')
            html[i] = html[i].split('  ')
            for j in range(len(html[i])):
                if j == 0:
                    if i == 0:
                        html[i][j] = (html[i][j])[1:5]+'-'+(html[i][j])[5:7]+'-'+(html[i][j])[7:9]
                    else:
                        html[i][j] = (html[i][j])[0:4]+'-'+(html[i][j])[4:6]+'-'+(html[i][j])[6:8]
                else:
                    html[i][j] = html[i][j]
            # print html[i]

        a = np.array(html)

        data = pd.DataFrame({'date':a[:,0],'value':np.float64(a[:,1]),'hist_value':np.float64(a[:,2])})
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date')
        # data.index = data['date'].values
        data['change'] = (data['hist_value']/data['hist_value'].shift(1)-1)
        data = data.dropna()
        return data


    def get_fund_index(self):
        html = self.getHtml("http://stock.finance.qq.com/fund/jzzx/kfs.js")
        html = html.decode('GBK')
        html = html.replace('[[','aaaa[[')
        html = html.replace(']]',']]aaaa')
        html = html.split('aaaa')
        html = html[1].replace('[[','[')
        html = html.replace(']]',']')
        html = html.replace('],[',']aaaa[')
        html = html.split('aaaa')
        html = html

        df = []
        for i in range(len(html)):
            temp = html[i].replace('"','')
            temp = temp.replace('[','')
            temp = temp.replace(']','')
            temp = temp.split(',')

            if i == 0:
                df = pd.DataFrame({'code':[temp[0]],'name':[temp[1]],'value':[temp[2]],'change_value':[temp[3]],
                                   'p_change':[temp[4]],'value_hist':[temp[5]],'date':[temp[6]],'buy':[temp[7]],'sell':[temp[8]],
                                   'master':[temp[9]]})
            else:
                df = df.append(pd.DataFrame({'code':[temp[0]],'name':[temp[1]],'value':[temp[2]],'change_value':[temp[3]],
                                   'p_change':[temp[4]],'value_hist':[temp[5]],'date':[temp[6]],'buy':[temp[7]],'sell':[temp[8]],
                                   'master':[temp[9]]}))

        df.set_index('code',inplace=True)
        df.to_csv('data/fund_index.csv',encoding='utf-8')
        return df

    def get_weeks_hist(self,symbol):
        df = self.get_fund_hist(symbol)
        df = df.resample( 'W-FRI' )
        df['change'] = np.log(df['hist_value']/(df['hist_value'].shift(1)))
        df = df.fillna(method='pad')
        df = df.dropna()

        df_mean = df['change'].mean()
        df_mean = (1+df_mean)**56-1
        df_var = df['change'].var()
        df_var = (1+df_var)**56-1
        return [df,df_mean,df_var]

    # def get_fund_mean_std(symbol):
    #     L_thld = 750
    #     L_year = 250
    #     df = pd.DataFrame(columns = ['Symbol','Mean_Y','Std_Y','Delta'])
    #     for i in range(len(symbol)):
    #         try:
    #             df_temp = get_fund_hist(symbol[i])
    #             if len(df_temp) > L_thld:
    #                 df_temp = df_temp[-L_thld:-1]
    #                 Mean = (1 + df_temp['change'].mean())**L_year
    #                 Std  = df_temp['change'].std()*(L_year**0.5)
    #                 M_Delta = Mean - Std - 1
    #                 df = df.append(pd.DataFrame({'Symbol':[symbol[i]],'Mean_Y':[Mean],'Std_Y':[Std],'Delta':[M_Delta]}))
    #                 print i,symbol[i],Mean,Std,M_Delta
    #             else:
    #                 print i,symbol[i],'too short'
    #         except:
    #             print i,symbol[i],'error'
    #     return df

