import pandas as pd

"""
HDDSStapCer
HDDSStapRoot
HDDSPulse
HDDSDairy
HDDSPrMeatF
HDDSPrMeatO
HDDSPrFish
HDDSPrEggs
HDDSVeg
HDDSFruit
HDDSFat
HDDSSugar
HDDSCond


(HDDSStapCer
HDDSStapRoot) --> FCSStap
HDDSPulse -> FCSPulse
HDDSDairy -> FCSDairy
(HDDSPrMeatF
HDDSPrMeatO
HDDSPrFish
HDDSPrEggs) --> FCSPr
HDDSVeg -> FCSVeg
HDDSFruit -> FCSFruit
HDDSFat --> FCSFat
HDDSSugar -> FCSSugar
HDDSCond -> FCSCond
"""

def check_hdds(df):
    # if household has consumped staples for 0 days in FCS but has not consummed staples in the last 24hrs
    if df["FCSStap"] == 7 and (df["HDDSStapCer"] == 0 or df["HDDSStapRoot"] == 0):
        df["Flag_HHDStap"] = True
    # if household has consumped pulse for 0 days in FCS but has not consummed pulse in the last 24hrs
    if df["HDDSPulse"] == 0 and df["FCSPulse"] == 7:
        df["Flag_HHDPulse"] = True
    # check dairy
    if df["HDDSDairy"] == 0 and df["FCSDairy"] == 7:
        df["Flag_HDDSDairy"] = True
    # check animal proteins
    if (df["HDDSPrMeatF"] == 0 or df["HDDSPrMeatO"] == 0 or df["HDDSPrFish"] == 0 or df["HDDSPrEggs"] == 0) and df["FCSPr"] == 7:
        df["Flag_HDDSPr"] = True
    # check vegetables
    if df["HDDSVeg"] == 0 and df["FCSVeg"] == 7:
        df["Flag_HDDSVeg"] = True
    # check fruit
    if df["HDDSFruit"] == 0 and df["FCSFruit"] == 7:
        df["Flag_HDDSFruit"] = True
    # check fat
    if df["HDDSFat"] == 0 and df["FCSFat"] == 7:
        df["Flag_HDDSFat"] = True
    # check sugar
    if df["HDDSSugar"] == 0 and df["FCSSugar"] == 7:
        df["Flag_HDDSSugar"] = True
    # check condiments
    if df["HHDSCond"] == 0 and df["FCSCond"] == 7:
        df["Flag_HDDSSugar"] = True

    return  df
