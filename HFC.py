import pandas as pd
from indicators.fcs import FCS
from indicators.rcsi import rCSI
from config import (high_fcs, 
                    low_fcs,
                    fcs_high_erroneous,
                    fcs_low_erroneous,
                    high_sugar_oil_consumption,
                    rcsi_high_erroneous,
                    rcsi_low_erroneous)

if __name__ == "__main__":
    df = pd.read_csv('data/congo.csv')

    # Initialize FCS instance and calculate indicators
    fcs_instance = FCS(df.copy(), low_fcs, high_fcs, fcs_low_erroneous, fcs_high_erroneous, high_sugar_oil_consumption)
    fcs_instance.calculate_fcs()
    fcs_instance.calculate_fcg()
    fcs_instance.generate_flags()
    
    # Initialize rCSI instance and calculate indicators
    rcsi_instance = rCSI(df.copy(), rcsi_low_erroneous, rcsi_high_erroneous)
    rcsi_instance.calculate_rCSI()
    rcsi_instance.generate_flags()
    
    # Output directory for reports
    output_dir = './Reports'
    fcs_instance.generate_report(output_dir)
    rcsi_instance.generate_report(output_dir)
