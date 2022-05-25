import pandas as pd


def getMKT(largeCapSample: pd.DataFrame):
    """This Method Returns Market Factor

    Args:
        largeCapSample (pd.DataFrame): Large Cap Sample

    Returns:
        MKT_f (pd.DataFrame): Contains Market Factor
    """
    mktport = largeCapSample[largeCapSample['Price'].notna()]
    marketport = mktport.groupby('Date')['MarketCap'].sum().reset_index(name='TotalMarketCap')

    marketInd = mktport.copy()
    marketInd['weights'] = marketInd['Return'] * marketInd['MarketCap']
    recomp = marketInd.groupby('Date')['weights'].sum().reset_index(name='TotalMarketReturn')
    marketport['MarketIndexReturn'] = recomp['TotalMarketReturn']/ marketport['TotalMarketCap']
    
    riskfree = mktport.groupby('Date')['RiskFree'].mean().reset_index()
    marketport = marketport.merge(riskfree, on='Date')
    marketport['MKT'] = marketport['MarketIndexReturn'] - marketport['RiskFree']
    MKT_f = marketport[['Date','MKT']]
    return MKT_f
