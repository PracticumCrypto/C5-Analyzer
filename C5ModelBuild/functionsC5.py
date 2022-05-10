import pandas as pd
def ModelBuild(fullSample: pd.DataFrame,
               factorList: list):
    from sklearn.linear_model import LinearRegression

    largeCapSample = fullSample.query("MarketCap > 1000000").groupby(['Date']).apply(
        lambda x: x.nlargest(100, ['MarketCap'])).reset_index(drop=True)

    performance = {}

    ## find the top 100 crypto currencies at the last week

    latest = largeCapSample.Date.max()
    latestLarge = largeCapSample.query("Date == @latest")

    # factors = factors.merge(MOM_f, on = 'Date', how ='outer')
    from functools import reduce
    factors = reduce(lambda left, right:
                     pd.merge(left,
                              right,
                              on='Date',
                              how='outer'),
                     factorList)

    features = factors.columns.tolist()
    features.remove('Date')
    target = "ExcessReturn"

    for index in latestLarge['Asset'].tolist():
        syntax = f"Asset == '{index}'"
        segment = fullSample.query(syntax)

        reg = segment[['Date', 'ExcessReturn']].merge(
            factors, 
            on='Date',
            how='outer')
        y = reg[target].copy()
        x = reg[features].copy()
        model = LinearRegression()
        model.fit(x, y)
        alpha = model.intercept_
        performance[index] = alpha
    alp_sig = pd.DataFrame(list(performance.items()),
                           columns=['Asset', 'Alpha'])
    alp_sig = alp_sig.sort_values(by = ['Alpha'],
                                  ascending = False).reset_index(drop = True)
    return alp_sig
