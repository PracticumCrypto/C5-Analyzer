import pandas as pd


def getNET(largeCapSample: pd.DataFrame):
    """This Method Returns Net Factor. The network factor (NET) is constructed by splitting the coins of the Core Sample into 3 groups due to the limitation of available coins. Particularly, each week we split the cryptocurrencies into three [30% 40% 30%] groups by the growth rate in total addresses with balance. The network factor (NET) is the return difference between the top and the bottom network portfolios.

    Args:
        largeCapSample (pd.DataFrame): Large Cap Sample

    Returns:
        NET (pd.DataFrame): Contains Net Factor
    """
    import numpy as np
    
    # Get Address Growth
    Address = largeCapSample.query("ActiveAddress > 0").loc[:, ['Date', 'ActiveAddress', 'Asset']] \
        .pivot(index='Date',
               columns='Asset',
               values='ActiveAddress')\
        .reset_index() \
        .rename_axis(None,
                     axis=1)

    copy1 = Address.copy()
    copy2 = copy1.shift()

    Growth = copy1.copy()

    cols = largeCapSample.Asset.unique().tolist()

    for i in cols:
        Growth[i] = np.log(copy1[i]) - np.log(copy2[i])

    Growth['20Percentile'] = Growth[cols].quantile(q=0.2,
                                                   numeric_only=True,
                                                   axis=1)
    Growth['80Percentile'] = Growth[cols].quantile(q=0.8,
                                                   numeric_only=True,
                                                   axis=1)
    # Construct Network factor
    Return = largeCapSample.loc[:, ['Date',
                                    'Return',
                                    'Asset']].pivot(index='Date',
                                                    columns='Asset',
                                                    values='Return').reset_index().rename_axis(None,
                                                                                               axis=1)

    NET = pd.DataFrame({'Date': []})
    NET['Date'] = Return.Date
    NET['long'] = Return[Growth[cols].apply(lambda x: x >= Growth['80Percentile'])].mean(axis=1,
                                                                                         numeric_only=True)
    NET['short'] = Return[Growth[cols].apply(lambda x: x <= Growth['20Percentile'])].mean(axis=1,
                                                                                          numeric_only=True)
    NET.fillna(value=0, 
               inplace=True)
    NET['NET'] = NET['long'] - NET['short']
    return NET.drop(columns=['short', 'long'])
