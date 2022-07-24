'''
defmakedf.py
'''

def mdfmake(x, y, m):
    
    import numpy as np
    import pandas as pd
    import pandas_datareader as data 
    import datetime as datetime


    stcode = x+".JP"
    dt_now = datetime.datetime.now()
    ly = dt_now.year
    lm = dt_now.month
    ld = dt_now.day
    
    stock = data.DataReader(stcode,'stooq',start=datetime.date(y, m, 1),end=datetime.date(ly,lm,ld))
    #datetime.datetime(ly,lm,ld))

    stock = stock.sort_values(by='Date')

    #%Y-%m の形にそろえる列ｙｍを作成し、リスト化
    stock['ym'] = stock.index.strftime("%Y-%m")

    listym = list(stock['ym'])

    #ym の重複をなくす
    mlist = stock['ym'].unique()
    

    #DateのMultiindexを解除
    stock = stock.reset_index()

    sclist = []
    mnths = []

    #毎月の株価を格納するリストを作成
    for i in range(len(mlist)-2):
        sc = stock['Close'][stock['ym']==mlist[i]]
        listedsc = list(sc)
        sclist.append(listedsc)
        mn = str(x)+"JP"+str(mlist[i])
        mnths.append(mn)
        
    print('make'+str(x)+'df end')

    listedml = list(mnths)

    #リストをdf化し、転地して列と行を調整
    scdf = pd.DataFrame(sclist).T
    scdf.columns = listedml
    #scdf.index = scdf['days']
    return scdf
    

    
#madedf = mdfmake("1306.JP",2009)
#madedf

################################

def mdfreturn(x, y, m):
    
    import numpy as np
    import pandas as pd
    import pandas_datareader as data 
    import datetime as datetime


    stcode = x+".JP"
    dt_now = datetime.datetime.now()
    ly = dt_now.year
    lm = dt_now.month
    ld = dt_now.day
    
    stock = data.DataReader(stcode,'stooq',start=datetime.date(y, m, 1),end=datetime.date(ly,lm-1,ld))
    #datetime.datetime(ly,lm,ld))

    stock = stock.sort_values(by='Date')

    #%Y-%m の形にそろえる列ｙｍを作成し、リスト化
    stock['ym'] = stock.index.strftime("%Y-%m")

    listym = list(stock['ym'])

    #ym の重複をなくす
    mlist = stock['ym'].unique()
    

    #DateのMultiindexを解除
    stock = stock.reset_index()

    sclist = []
    mnths = []

    #毎月の株価を格納するリストを作成
    for i in range(len(mlist)):
        sc = stock['Close'][stock['ym']==mlist[i]]
        listedsc = list(sc)
        sclist.append(listedsc)
        mn = str(x)+"JP"+str(mlist[i])
        mnths.append(mn)
        
    print('return '+str(x)+' df end')

    listedml = list(mnths)

    #リストをdf化し、転地して列と行を調整
    scdf = pd.DataFrame(sclist).T
    scdf.columns = listedml
    #scdf.index = scdf['days']
    return scdf

#####################

def rdf(returndf):
    import pandas as pd
    mname = []
    mnum = []
    stmonth = []
    nxrt1a = []
    nxrt  =  []

# from 0 to 156   #200903-202204
    for i in range(1,len(returndf.columns)):
        month = returndf.columns[i-1] + ">" + returndf.columns[i]
        startmonth = returndf.columns[i-1] 
        premonthdays = len(returndf[returndf.columns[i-1]].dropna())-1
        postmonthdays = len(returndf[returndf.columns[i]].dropna())-1
        prelastprice = returndf[returndf.columns[i-1]][premonthdays]
        postlastprice = returndf[returndf.columns[i]][postmonthdays]
        retans = (postlastprice/prelastprice)-1



        mname.append(month)
        mnum.append(i-1)
        stmonth.append(startmonth)
        nxrt.append(retans*100)

    returns = pd.DataFrame()
    returns["mname"] = stmonth
    returns["mnum"] = mnum
    returns["nxrt"] = nxrt
    return returns
    
def plusper(madedf,returns,target):
    import pandas as pd
    #madfdfgat = pd.DataFrame()
    plus  = returns[returns["nxrt"]>target]

    mnames = list(plus["mnum"])
    madegat = madedf.iloc[:, mnames]
    #madedfgat = pd.concat([madedfgat, madedf], axis=1)
    return madegat

#########################
def presentstock(x):
    import numpy as np
    import pandas as pd
    import pandas_datareader as data 
    import datetime as datetime


    stcode = x+".JP"
    dt_now = datetime.datetime.now()
    ly = dt_now.year
    lm = dt_now.month
    ld = dt_now.day
    
    stock = data.DataReader(stcode,'stooq',start=datetime.date(ly, lm-1, 1),end=datetime.date(ly,lm,ld))
    #datetime.datetime(ly,lm,ld))

    stock = stock.sort_values(by='Date')

    #%Y-%m の形にそろえる列ｙｍを作成し、リスト化
    stock['ym'] = stock.index.strftime("%Y-%m")

    listym = list(stock['ym'])

    #ym の重複をなくす
    mlist = stock['ym'].unique()
    latm = mlist[0]
    

    #DateのMultiindexを解除
    stock = stock.reset_index()

    sclist = []
    mnths = []

    #毎月の株価を格納するリストを作成
    sc = stock['Close'][stock['ym']==mlist[0]]
    listedsc = list(sc)
    mn = str(x)+"JP"+str(mlist[0])
    listedmn = list(mn)
        
    print('return '+str(x)+' df end')

    #リストをdf化し、転地して列と行を調整
    #scdf = pd.DataFrame(data = listedsc, columns=listedmn)
    #scdf.columns = list(mn)
    #scdf.index = scdf['days']
    scdf = pd.DataFrame(listedsc, columns=[mn])
    return scdf

    