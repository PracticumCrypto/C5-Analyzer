import pandas as pd
import numpy as np

def AddReturn(sample: pd.DataFrame):
    """This Method Add Return Column to Pulled Raw Data

    Args:
        sample (pd.DataFrame): The Raw Pulled Data without a Return Column

    Returns:
        fullFrame (pd.DataFrame): DataFrame with a Return Column
    """
    fullFrame = pd.DataFrame(columns=list(sample.columns))
    
    ### replace 0 values in active address to 1
    new = sample.copy()
    new.drop(['ActiveAddress'], axis = 1)
    new['ActiveAddress'] = sample['ActiveAddress'].replace({0.0:1.0})
    
    ###
    
    for index in sample['Asset'].unique().tolist():
        syntax = f"Asset == '{index}'"
        segment = new.query(syntax)
        segment = segment.assign(Return = segment.Price.rolling(2).apply(lambda x: (x.iloc[-1]-x.iloc[0])/x.iloc[0]).copy())
        segment = segment.assign(week2_return = segment.Price.rolling(4).apply(lambda x: (x.iloc[-2]-x.iloc[0])/x.iloc[0]))
        segment = segment.assign(Npast52_return = segment.Price.rolling(53).apply(lambda x: (x.iloc[-2]-x.iloc[0])/x.iloc[0]))
        segment = segment.assign(GrowthRate = segment.ActiveAddress.rolling(3).apply(lambda x: np.log(x.iloc[-2])-np.log(x.iloc[0])
                                                                                     if ((x.iloc[0]>0 and x.iloc[-2]>0)) else np.nan ))                                                                                                                                                                                                                                                                                                    
        segment = segment.assign(lagCap = segment.MarketCap.shift())
                                 
        #############remove stable currency ########### 
        stdvar = segment.Return.std()
    
        ##################                         
        if stdvar > 0.005:
            segment = segment[-52:].reset_index(drop=True)
            fullFrame = pd.concat([fullFrame, segment],
                                         ignore_index=True)
            fullFrame["ExcessReturn"] = fullFrame["Return"] - fullFrame["RiskFree"]

    return fullFrame


def StoppedTrading(sample: pd.DataFrame):
    """This Method will remove crypto currencies stopped trading.

    Args:
        sample (pd.DataFrame): The Pulled Data 

    Returns:
        fullFrame (pd.DataFrame): A DataFrame with all cryptocurrencies stopped trading removed.
    """
    # Initialization
    validFrame = pd.DataFrame(columns=list(sample.columns))

    originalCols = list(sample.columns)
    originalCols.remove('RiskFree')
    
    

    for index in sample['Asset'].unique().tolist():
        syntax = f"Asset == '{index}'"
        segment = sample.query(syntax)
         
        if (segment['Price'][-4:].isnull().sum() < 4):
            temp = pd.DataFrame()
            temp[originalCols] = segment[originalCols]
            temp['RiskFree'] = segment[['RiskFree']].interpolate(
                method='linear', limit_direction='forward', axis=0)
            validFrame = pd.concat([validFrame, temp], ignore_index=True)

    return validFrame