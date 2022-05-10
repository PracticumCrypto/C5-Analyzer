import pandas as pd


def getMKT(largeCapSample: pd.DataFrame):
    """This Method Returns Market Factor

    Args:
        largeCapSample (pd.DataFrame): Large Cap Sample

    Returns:
        MKT_f (pd.DataFrame): Contains Market Factor
    """
    marketport = largeCapSample.groupby(
        'Date')['MarketCap'].sum().reset_index(name='TotalMarketCap')

    marketInd = largeCapSample.copy()
    marketInd['weights'] = marketInd['Return'] * marketInd['MarketCap']
    recomp = marketInd.groupby('Date')['weights'].sum(
    ).reset_index(name='TotalMarketReturn')
    marketport['MarketIndexReturn'] = recomp['TotalMarketReturn'] / \
        marketport['TotalMarketCap']

    riskfree = largeCapSample.groupby('Date')['RiskFree'].mean().reset_index()
    marketport = marketport.merge(riskfree, on='Date')
    marketport['MKT'] = marketport['MarketIndexReturn'] - \
        marketport['RiskFree']
    MKT_f = marketport[['Date', 'MKT']]
    return MKT_f
