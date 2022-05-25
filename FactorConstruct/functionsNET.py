import pandas as pd


def getNET(largeCapSample: pd.DataFrame):
    """This Method Returns Net Factor. The network factor (NET) is constructed by splitting the coins of the Core Sample into 3 groups due to the limitation of available coins. Particularly, each week we split the cryptocurrencies into three [30% 40% 30%] groups by the growth rate in total addresses with balance. The network factor (NET) is the return difference between the top and the bottom network portfolios.

    Args:
        largeCapSample (pd.DataFrame): Large Cap Sample

    Returns:
        NET (pd.DataFrame): Contains Net Factor
    """
    import numpy as np
    
    Growth = largeCapSample.pivot(index='Date',
                              columns='Asset',
                              values='GrowthRate').reset_index().rename_axis(None,
                                                                             axis=1)
    cols = largeCapSample.Asset.unique().tolist()

    Growth['20Percentile'] = Growth[cols].quantile(q=0.2,
                                                numeric_only=True,
                                                axis=1)
    Growth['80Percentile'] = Growth[cols].quantile(q=0.8,
                                                numeric_only=True,
                                                axis=1)
    
    Return = largeCapSample.pivot(index='Date',
                              columns='Asset',
                              values='Return').reset_index().rename_axis(None,
                                                                         axis=1)

    NET = pd.DataFrame({'Date': []})
    NET['Date'] = Return.Date

    # Lambda function disordered the columns, added additional step to sort columns in alphabetical order
    long = Growth[cols].apply(lambda x: x >= Growth['80Percentile'])
    long = long.reindex(sorted(long.columns), 
                        axis=1)
    NET['long'] = Return[long].mean(axis=1,
                                    numeric_only=True)

    short = Growth[cols].apply(lambda x: x <= Growth['20Percentile'])
    short = short.reindex(sorted(short.columns), 
                        axis=1)
    NET['short'] = Return[short].mean(axis=1, 
                                    numeric_only=True)

    NET['NET'] = NET['long'] - NET['short']
    NET.drop(columns=['short', 'long'])
    NET = NET[['Date', 'NET']]

    return NET
