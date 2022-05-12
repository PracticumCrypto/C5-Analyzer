import pandas as pd
from rich.table import Table
from rich.console import Console
console = Console()
import os
import logging
from rich.logging import RichHandler
from datetime import datetime

# Check If There Is A Save Destination for Log
if not os.path.isdir('./Log'):
    os.makedirs('./Log', exist_ok=True)

# Formatting Log Filename
file_handler = logging.FileHandler(
    f"./Log/log{datetime.now():%Y%m%d%H%M%S}.log"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s'))

cons_handler = RichHandler(rich_tracebacks=True)
cons_handler.setFormatter(logging.Formatter("%(funcName)s: %(message)s"))
cons_handler.setLevel(logging.DEBUG)

# Instantiate A Log Object for Console Outputting
logC = logging.getLogger("Console")
logC.addHandler(cons_handler)
logC.setLevel(logging.DEBUG)


# Instantiate Another Log Object for Writing Log File
logF = logging.getLogger("File")
logF.addHandler(file_handler)
logF.addHandler(cons_handler)
logF.setLevel(logging.DEBUG)


# Pre-Loading Packages
console.rule("[bold red]Pre Load")
logC.info("[bold magenta]Initializing... Please Be Patient...[/bold magenta]\n",
          extra={"markup": True})

# Import DataPull
try:
    logC.info("Loading [bold magenta]DataPull[/bold magenta] Functions...",
              extra={"markup": True})
    import DataPull.constants as cons
    import DataPull.functions as pullFuc
except:
    logF.exception(
        "Failed Loading DataPull Functions. Please Check Source Code")
else:
    logF.debug("DataPull Functions Loaded Successfully\n")

# Import DataProcess
try:
    logC.info("Loading [bold magenta]DataProcess[/bold magenta] Functions...",
              extra={"markup": True})
    import DataProcess
except:
    logF.exception(
        "Failed Loading DataProcess Functions. Please Check Source Code")
else:
    logF.debug("DataProcess Functions Loaded Successfully\n")

# Import FactorConstruct
try:
    logC.info("Loading [bold magenta]FactorConstruct[/bold magenta] Functions...",
              extra={"markup": True})
    import FactorConstruct
except:
    logF.exception(
        "Failed Loading FactorConstruct Functions. Please Check Source Code")
else:
    logF.debug("FactorConstruct Functions Loaded Successfully\n")

# Import C5ModelBuild
try:
    logC.info("Loading [bold magenta]C5ModelBuild[/bold magenta] Functions...",
              extra={"markup": True})
    import C5ModelBuild
except:
    logF.exception(
        "Failed Loading C5ModelBuild Functions. Please Check Source Code")
else:
    logF.debug("C5ModelBuild Functions Loaded Successfully\n")

### Init
# Get Full Sample
import DataPull.asyncPull as ap
console.rule("[bold red]Data Pull & Parse")
try:
    fullSample_raw = ap.PullStart()
except:
    logF.exception(
        "Failed Pulling Data. Please Check Source Code in 'DataPull' File")
else:
    logF.debug("Raw Full Sample Pulled Successfully\n")

# Impute missing value using interploration method
try:
    imputedfullSample = DataProcess.processFun.InterpolationImpute(
        fullSample_raw)
except:
    logF.exception("Failed Imputing Data. Please Check 'InterpolationImpute' Source Code in 'DataProcess' File\n Or Check Whether You Get 'Raw Full Sample' Properly?")
else:
    logF.debug("Raw Full Sample Imputed Successfully\n")

# Add Return to fullSample
try:
    fullSample = DataProcess.processFun.AddReturn(imputedfullSample)
except:
    logF.exception(
        "Failed Parsing Data. Please Check 'AddReturn' Source Code in 'DataProcess' File\n Or Check Whether You Get 'Imputed Full Sample' Properly?")
else:
    logF.debug("Full Sample Parsed Successfully\n")

# Use (market cap > 1m and top 100) to set up the dynamic portfolio for each week, we would use this dynamic portfolio for our factors calculation.
try:
    largeCapport = fullSample.query("MarketCap > 1000000")
    largeCapSample = largeCapport.groupby(['Date']).apply(lambda x: x.nlargest(100,
                                                                               ['MarketCap'])).reset_index(drop=True)
except:
    logF.exception(
        "Failed Parsing Data. Please Check Whether You Get 'Full Sample' Properly?")
else:
    logF.debug("Large Cap Sample Transformed Successfully\n")

console.rule("[bold red]Factors Construct")
# MOM
try:
    MOM_f = FactorConstruct.MOM.getMomFactor(largeCapSample)
except:
    logF.exception("Failed Calculating Momentum Factor. Please Check 'functionsMOM' Source Code in 'FactorConstruct'\n Or Check Whether You Get 'LargeCap Sample' Properly?")
else:
    logF.debug("Momentum Factor Calculated Successfully\n")

# SMB
try:
    SMB_f = FactorConstruct.SMB.getSMB(largeCapSample)
except:
    logF.exception("Failed Calculating Size Factor. Please Check 'functionsSMB' Source Code in 'FactorConstruct'\n Or Check Whether You Get 'LargeCap Sample' Properly?")
else:
    logF.debug("Size Factor Calculated Successfully\n")

# MKT
try:
    MKT_f = FactorConstruct.MKT.getMKT(largeCapSample)
except:
    logF.exception("Failed Calculating Market Factor. Please Check 'functionsMKT' Source Code in 'FactorConstruct'\n Or Check Whether You Get 'LargeCap Sample' Properly?")
else:
    logF.debug("MKT Factor Calculated Successfully\n")

# NET
try:
    NET_f = FactorConstruct.NET.getNET(largeCapSample)
except:
    logF.exception("Failed Calculating Network Factor. Please Check 'functionsSMB' Source Code in 'FactorConstruct'\n Or Check Whether You Get 'LargeCap Sample' Properly?")
else:
    logF.debug("Network Factor Calculated Successfully\n")

# VAL
try:
    VAL_f = FactorConstruct.VAL.getVAL(largeCapSample)
except:
    logF.exception("Failed Calculating Value Factor. Please Check 'functionsVAL' Source Code in 'FactorConstruct'\n Or Check Whether You Get 'LargeCap Sample' Properly?")
else:
    logF.debug("Value Factor Calculated Successfully\n")

# Model Building
console.rule("[bold red]C5 Model Build")
try:
    logC.info("Constructing [bold magenta]C5 Model[/bold magenta] for Alphas..\n",
              extra={"markup": True})
    factorList = [MKT_f, SMB_f, MOM_f, NET_f, VAL_f]
    Alphas = C5ModelBuild.C5.ModelBuild(fullSample, factorList)
except:
    logF.exception(
        "Failed Building C5 Model. Please Check 'functionsC5' Source Code in 'C5ModelBuild'\n Or Check Whether You Get 'All C5 Factors' Properly?")
else:
    logF.debug("Extracted Alphas from C5 Model Successfully\n")

tableB = Table(title="Bottom 10 Alphas")

tableT = Table(title="Top 10 Alphas")


def df_to_table(
    pandas_dataframe: pd.DataFrame,
    rich_table: Table,
    show_index: bool = True,
    index_name: str = None,
) -> Table:
    """Convert a pandas.DataFrame obj into a rich.Table obj.
    Args:
        pandas_dataframe (DataFrame): A Pandas DataFrame to be converted to a rich Table.
        rich_table (Table): A rich Table that should be populated by the DataFrame values.
        show_index (bool): Add a column with a row count to the table. Defaults to True.
        index_name (str, optional): The column name to give to the index column. Defaults to None, showing no value.
    Returns:
        Table: The rich Table instance passed, populated with the DataFrame values."""
    if show_index:
        index_name = str(index_name) if index_name else ""
        rich_table.add_column(index_name)

    for column in pandas_dataframe.columns:
        rich_table.add_column(str(column))

    for index, value_list in enumerate(pandas_dataframe.values.tolist()):
        row = [str(index)] if show_index else []
        row += [str(x) for x in value_list]
        rich_table.add_row(*row)

    return rich_table


topTable = df_to_table(Alphas.head(10), tableT, show_index=False)

tailTable = df_to_table(Alphas.tail(10), tableB, show_index=False)

console.print(tailTable, justify="center")

console.print(topTable, justify="center")

#Prevent Program Window from Immediately Exit
isThisQ = ""
while isThisQ != "q":
    isThisQ = console.input(
        "Done! Please Type [bold green]\"q\"[/bold green] and Then Press [bold green]Enter[/bold green] to Exit:  ")
    if isThisQ == "q":
        break
console.print("Bye")
