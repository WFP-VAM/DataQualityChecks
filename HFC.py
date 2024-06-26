import pandas as pd
from indicators.fcs import FCS
from indicators.rcsi import rCSI
from indicators.demographics import Demo
from indicators.hdds import HDDS
from config import (high_fcs, 
                    low_fcs,
                    fcs_high_erroneous,
                    fcs_low_erroneous,
                    high_sugar_oil_consumption,
                    high_rcsi,
                    rcsi_high_erroneous,
                    rcsi_low_erroneous,
                    demo_low_erroneous,
                    demo_high_erroneous,
                    high_hhsize,
                    hdds_low_erroneous,
                    hdds_high_erroneous)

if __name__ == "__main__":
    df = pd.read_csv('congo.csv')

    # Initialize FCS instance and calculate indicators
    fcs_instance = FCS(df.copy(), 
                       low_fcs=low_fcs,
                       high_fcs=high_fcs,
                       low_erroneous=fcs_low_erroneous,
                       high_erroneous=fcs_high_erroneous,
                       high_sugar_oil_consumption=high_sugar_oil_consumption)
    fcs_instance.calculate_fcs()
    fcs_instance.calculate_fcg()
    fcs_instance.generate_flags()
    
    # Initialize rCSI instance and calculate indicators
    rcsi_instance = rCSI(fcs_instance.df.copy(),
                         high_rcsi=high_rcsi,
                         low_erroneous=rcsi_low_erroneous,
                         high_erroneous=rcsi_high_erroneous,
                         high_sugar_oil_consumption=high_sugar_oil_consumption)
    rcsi_instance.calculate_rCSI()
    rcsi_instance.generate_flags()
    
    # Initialize Demographics instance and calculate indicators
    demo_instance = Demo(rcsi_instance.df.copy(), 
                         low_erroneous=demo_low_erroneous,
                         high_erroneous=demo_high_erroneous,
                         high_hhsize=high_hhsize)
    demo_instance.calculate_indicators()
    demo_instance.generate_flags()
    
    # Initialize HDDS instance and calculate indicators
    hdds_instance = HDDS(demo_instance.copy(), 
                         low_erroneous=hdds_low_erroneous,
                         high_erroneous=hdds_high_erroneous)
    hdds_instance.calculate_hdds()
    hdds_instance.generate_flags()
    
    # Output directory for reports
    output_dir = './Reports'
    fcs_instance.generate_report(output_dir)
    rcsi_instance.generate_report(output_dir)
    demo_instance.generate_report(output_dir)
    hdds_instance.generate_report(output_dir)
