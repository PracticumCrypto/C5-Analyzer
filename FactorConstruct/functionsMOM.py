import pandas as pd


def getMomFactor(largeCapSample: pd.DataFrame):
    """This Method Returns Momentum Factor

    Args:
        largeCapSample (pd.DataFrame): Large Cap Sample

    Returns:
        momFactor (pd.DataFrame): Contains Momentum Factor
    """
    # Pivot largeCapSample to Get Return Matrix
    returnAll = largeCapSample.pivot(index="Date",
                                     columns=["Asset"],
                                     values='Return').reset_index().rename_axis(None,
                                                                                axis=1).sort_values('Date')

    # Pivot largeCapSample to Get Momentum Matrix(Past 2-Week Returns)
    momMatrix = largeCapSample.pivot(index="Date",
                                     columns=["Asset"],
                                     values='week2_return').reset_index().rename_axis(None,
                                                                                      axis=1).sort_values('Date')

    # Calculate the Momentum Percentile
    col = sorted(largeCapSample.Asset.unique())

    momPt = pd.DataFrame(columns=['MOM20p',
                                  'MOM80p'])

    momPt['MOM20p'] = momMatrix[col].quantile(.2, axis=1)
    momPt['MOM80p'] = momMatrix[col].quantile(.8, axis=1)

    # Calculate MOM Factor
    MOM = pd.DataFrame({'Date': []})
    MOM['Date'] = returnAll.Date
    MOM['HighMomentum'] = returnAll.drop("Date", axis=1)[momMatrix[sorted(largeCapSample.Asset.unique())].apply(
        lambda x: x >= momPt['MOM80p'])].mean(axis=1, numeric_only=True)
    MOM['LowMomentum'] = returnAll.drop("Date", axis=1)[momMatrix[sorted(largeCapSample.Asset.unique())].apply(
        lambda x: x <= momPt['MOM20p'])].mean(axis=1, numeric_only=True)
    MOM['MOM'] = MOM.HighMomentum - MOM.LowMomentum
    momFactor = MOM.drop(columns=['HighMomentum', 'LowMomentum'])
    return momFactor

