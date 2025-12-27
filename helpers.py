import pandas as pd

# NEED TO RE-WRITE TO WORK WITH SQL

# Function that takes a list of institution UKPRNs, and a list of theme IDs, 
# and returns a dictionary containing info filtered to that.
def inst(NSS, UKPRN, THEME_IDs):
    NSS_filtered = NSS[(NSS["UKPRN"].isin(UKPRN)) & (NSS["THEME_ID"].isin(THEME_IDs))]
    NSS_filtered['CAH_CODE'].fillna("N/A", inplace=True)
    NSS_filtered['CAH_NAME'].fillna("N/A", inplace=True)
    return to_dict(NSS_filtered)

