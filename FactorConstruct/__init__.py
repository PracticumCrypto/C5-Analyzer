import logging
from rich.logging import RichHandler

cons_handler = RichHandler(rich_tracebacks=True)
cons_handler.setFormatter(logging.Formatter("%(funcName)s: %(message)s"))
cons_handler.setLevel(logging.DEBUG) 
log = logging.getLogger("C")
log.addHandler(cons_handler)
log.setLevel(logging.DEBUG)

from . import functionsMOM as MOM
log.info("Functions for Momentum (MOM) Loaded", 
         extra={"markup": True})

from . import functionsMKT as MKT
log.info("Functions for Market (MKT) Loaded", 
         extra={"markup": True})

from . import functionsNET as NET
log.info("Functions for Network (NET) Loaded", 
         extra={"markup": True})


from . import functionsSMB as SMB
log.info("Functions for Size (SMB) Loaded", 
         extra={"markup": True})

from . import functionsVAL as VAL
log.info("Functions for Value (VAL) Loaded", 
         extra={"markup": True})

