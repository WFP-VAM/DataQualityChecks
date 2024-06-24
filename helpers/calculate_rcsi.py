# Function to calculate rCSI
def calculate_rcsi(df):
    df['rCSI'] = (df['rCSILessQlty'] + 
                  (df['rCSIBorrow'] * 2) + 
                  df['rCSIMealNb'] + 
                  df['rCSIMealSize'] + 
                  (df['rCSIMealAdult'] * 3))
    return df