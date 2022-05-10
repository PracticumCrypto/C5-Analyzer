import pandas as pd


def getVAL(largeCapSample: pd.DataFrame):
    """This Method Returns Value Factor

    Args:
        largeCapSample (pd.DataFrame): Large Cap Sample

    Returns:
        valueFactor (pd.DataFrame): Contains Value Factor
    """
    #Reshape to get two tables with: Npast52_return, Return(weekly)
    npast52 = largeCapSample.loc[:, ['Date',
                                     'Npast52_return',
                                     'Asset']].pivot(index="Date",
                                                     columns=["Asset"],
                                                     values='Npast52_return').reset_index().rename_axis(None,
                                                                                                        axis=1).sort_values('Date')

    value_return = largeCapSample.loc[:, ['Date',
                                          'Asset',
                                          'Return']].pivot(index='Date',
                                                           columns=['Asset'],
                                                           values='Return').reset_index().rename_axis(None,
                                                                                                      axis=1).sort_values('Date')

    cols = list(largeCapSample.Asset.unique())

    npast52['top20'] = npast52[cols].quantile(q=0.8,
                                              axis=1,
                                              numeric_only=True,
                                              interpolation='linear')
    npast52['low20'] = npast52[cols].quantile(q=0.2,
                                              axis=1,
                                              numeric_only=True,
                                              interpolation='linear')

    # check whether Npast52 of a coin in a day is in low20 or top20, then calculate the weekly return mean of low20 and top20 , respectively
    VAL_low = (npast52[cols].apply(lambda x: x < npast52['low20'])
               * value_return[cols]).mean(axis=1,
                                          numeric_only=True)
    VAL_top = (npast52[cols].apply(lambda x: x > npast52['top20'])
               * value_return[cols]).mean(axis=1,
                                          numeric_only=True)

    # calculate Value factor using long-short method
    valueFactor = pd.DataFrame(columns=['Date', 'VAL'])
    valueFactor['Date'] = value_return['Date']
    valueFactor['VAL'] = VAL_top - VAL_low

    return valueFactor
