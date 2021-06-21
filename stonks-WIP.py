import yfinance as yf
import pandas as pd
#pd.set_option('display.max_columns', None)
stonk_file="stonks.csv"
nasdaq_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
other_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt"
DATA = [] #pd.read_csv(filepath_or_buffer=stonk_file)
SYM=[]

'''
new_columns = DATA.columns.values
new_columns[0] = 'S'
DATA.columns = new_columns
DATA= DATA.set_index('S')
then refill the ticker 
'''
def rebuild_data():
    global DATA, SYM
    Nasdaq_SN = pd.read_csv(nasdaq_url, sep="|")
    Nasdaq_SN = Nasdaq_SN.drop(len(Nasdaq_SN)-1).drop(labels=["Market Category","Test Issue","Financial Status","Round Lot Size","ETF","NextShares"], axis=1)
    print(Nasdaq_SN)
    NYSE_SN = pd.read_csv(other_url, sep='|')
    NYSE_SN = NYSE_SN.drop(len(NYSE_SN)-1).drop(labels=["ACT Symbol","Exchange","CQS Symbol","ETF","Round Lot Size","Test Issue"], axis=1)
    print(NYSE_SN)
    new_columns = NYSE_SN.columns.values
    new_columns[1] = 'Symbol'
    NYSE_SN.columns = new_columns
    
    All_Stonk_Names = pd.concat([NYSE_SN, Nasdaq_SN],
        axis=0,
        join="outer",
        ignore_index=False,
        keys=None,
        levels=None,
        names=None,
        verify_integrity=False,
        copy=True,
    )
    
    SYM = All_Stonk_Names['Symbol']
    '''
    ticks = [{'SYM':x, 'Symbol': x, 'Ticker': yf.Ticker(x)} for x in SYM]
    ticks = pd.DataFrame (ticks,columns=['SYM','Symbol','Ticker'])
    DATA = pd.concat([All_Stonk_Names.set_index('Symbol'), ticks.set_index('SYM')],
        axis=1,
        join="outer",
        ignore_index=False,
        keys=None,
        levels=None,
        names=None,
        verify_integrity=False,
        copy=True,
    )
    DATA.to_csv(path_or_buf="stonks.csv")
    '''
    
def stock_history(stk, pd='5y'):
    return DATA.loc[stk].iloc[-1].history(period=pd)

rebuild_data()
'''
data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = list(SYM),

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "ytd",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = "1m",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )
'''
