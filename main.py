from rich.console import Console
console = Console()
console.print("\n[bold magenta]Initializing, Please Be Patient...[/bold magenta]")
import DataPull.constants as cons
console.print("\nLoading [bold magenta]DataPull[/bold magenta] Functions...")
import DataPull.functions as pullFuc
console.print("\nLoading [bold magenta]DataProcess[/bold magenta] Functions...")
import DataProcess
console.print("\nLoading [bold magenta]FactorConstruct[/bold magenta] Functions...\n")
import FactorConstruct
console.print("\nLoading [bold magenta]C5ModelBuild[/bold magenta] Functions...\n")
import C5ModelBuild

### Init
# Get Full Sample
fullSample_raw = pullFuc.PullStart(cons.symbolList)
# Impute missing value using interploration method
imputedfullSample = DataProcess.processFun.InterpolationImpute(fullSample_raw)
# Add Return to fullSample
fullSample = DataProcess.processFun.AddReturn(imputedfullSample)
# Use (market cap > 1m and top 100) to set up the dynamic portfolio for each week, we would use this dynamic portfolio for our factors calculation.
largeCapport = fullSample.query("MarketCap > 1000000")
largeCapSample = largeCapport.groupby(['Date']).apply(lambda x: x.nlargest(100,
                                                                           ['MarketCap'])).reset_index(drop=True)

# MOM
MOM_f = FactorConstruct.MOM.getMomFactor(largeCapSample)

# SMB
SMB_f = FactorConstruct.SMB.getSMB(largeCapSample)

# MKT
MKT_f = FactorConstruct.MKT.getMKT(largeCapSample)

# NET
NET_f = FactorConstruct.NET.getNET(largeCapSample)

# VAL
VAL_f = FactorConstruct.VAL.getVAL(largeCapSample)

# Model Building
console.print("\nConstructing [bold magenta]C5 Model[/bold magenta] for Alphas..\n")
factorList = [MKT_f, SMB_f, MOM_f, NET_f, VAL_f]
Alphas = C5ModelBuild.C5.ModelBuild(fullSample, factorList)
console.print(Alphas.head(10))

#Prevent Program Window from Immediately Exit
isThisQ = ""
while isThisQ != "q":
    isThisQ = console.input("Done! Please Type [bold green]\"q\"[/bold green] and Then Press [bold green]Enter[/bold green] to Exit:  ")
    if isThisQ == "q":
        break
print("Bye")
