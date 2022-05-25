import pandas as pd


def getSMB(largeCapSample: pd.DataFrame):
    """This Method Returns Size Factor

    Args:
        largeCapSample (pd.DataFrame): Large Cap Sample

    Returns:
        SMB_f (pd.DataFrame): Contains Market Factor
    """
    # Using quantile method to get the dynamic portfolios for top cap 20%, and bottom cap 20%
    largeCap = largeCapSample.groupby(['Date']).apply(lambda 
                                                    x: x.nlargest(math.ceil(0.2*len(x)),
                                                                ['MarketCap'])).reset_index(drop=True)

    smallCap = largeCapSample.groupby(['Date']).apply(lambda 
                                                    x: x.nsmallest(math.ceil(0.2*len(x)),
                                                                ['MarketCap'])).reset_index(drop=True)

    # Using equal-weighted average method to get the SMB
    largeport = largeCap.groupby('Date')['Return'].mean().reset_index(name='LargePortReturn')
    smallport = smallCap.groupby('Date')['Return'].mean().reset_index(name='SmallPortReturn')
    smallport['SMB'] = smallport['SmallPortReturn'] - largeport['LargePortReturn']
    SMB_f = smallport[['Date','SMB']]
    return SMB_f
