import pandas as pd
from . import constants as cons
import aiohttp
import asyncio



async def Get(coin, Risk_free_rate):
    dataList = []
    for feature, url in cons.endPoints.items():
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.glassnode.com{url}?a={coin}&i=1w&api_key=1vGb0FOsg2hEIGrEhpueLCcWd1Y') as response:
                res = await response.text()
                data_raw = pd.read_json(res, convert_dates=['t'])

                # Rename column "v" according to features
                data = data_raw.rename(columns={"v": feature,
                                                't': 'Date'})
                dataList.append(data)

    from functools import reduce
    rawSingleCoin = (reduce(lambda left, right: 
        pd.merge(left, right, 
                 on='Date',
                 how='outer'),
        dataList).merge(Risk_free_rate, 
                        on="Date",
                        how="left").sort_values(by=['Date']))
    rawSingleCoin['Asset'] = coin
    return rawSingleCoin
    
async def main(loop):
    
    from rich.console import Console
    console = Console()
    console.print("Pulling [bold magenta]Fred[/bold magenta] Data...", justify='center')
    
    from fredapi import Fred
    fred = Fred(api_key=cons.FRED_API_KEY)
    risk_free_rate = fred.get_series('DGS1MO').to_frame().reset_index().rename(columns={'index': 'Date',
                                                                                        0: 'RiskFree'})
    risk_free_rate['RiskFree'] = risk_free_rate['RiskFree'] / 100
    
    tasks = [loop.create_task(Get(coin, risk_free_rate)) for coin in cons.symbolList]
    finished, unfinished = await asyncio.wait(tasks)
    all_results = [r.result() for r in finished]    
    return all_results


def PullStart():
    loop = asyncio.get_event_loop()
    all = loop.run_until_complete(main(loop))

    colName = ["Date"]
    for key in cons.endPoints.keys():
        colName.append(key)
    fullFrame = pd.DataFrame(columns=colName.append("Asset"))

    for frame in all:
        fullFrame = pd.concat([fullFrame, frame],ignore_index=True)

    return fullFrame
