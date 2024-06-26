import pandas as pd
from indicators.fcs import FCS
from indicators.rcsi import rCSI
from indicators.demographics import Demo
from indicators.hdds import HDDS
from indicators.fexp_7d import FEXP_7D
from indicators.nfexp_1m import NFEXP_1M
from indicators.nfexp_6m import NFEXP_6M
from indicators.fcs import fcs_cols, fcs_flags
from indicators.rcsi import rcsi_cols, rcsi_flags
from indicators.demographics import male_cols, female_cols, demo_flags
from indicators.fexp_7d import fexp_7d_cols, fexp_7d_flags
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
                    hdds_high_erroneous,
                    HHExpF_7D_low_erroneous, 
                    HHExpF_7D_high_erroneous,
                    HHExpNF_1M_low_erroneous,
                    HHExpNF_1M_high_erroneous,
                    HHExpNF_6M_low_erroneous,
                    HHExpNF_6M_high_erroneous)

if __name__ == "__main__":
    df = pd.read_csv('data/congo.csv')
    output_dir = './Reports'
    
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
    fcs_instance.generate_report(output_dir)
    
    # Initialize rCSI instance and calculate indicators
    rcsi_instance = rCSI(fcs_instance.df.copy(),
                         high_rcsi=high_rcsi,
                         low_erroneous=rcsi_low_erroneous,
                         high_erroneous=rcsi_high_erroneous,
                         high_sugar_oil_consumption=high_sugar_oil_consumption)
    rcsi_instance.calculate_rCSI()
    rcsi_instance.generate_flags()
    rcsi_instance.generate_report(output_dir)
    
    # Initialize Demographics instance and calculate indicators
    demo_instance = Demo(rcsi_instance.df.copy(), 
                         low_erroneous=demo_low_erroneous,
                         high_erroneous=demo_high_erroneous,
                         high_hhsize=high_hhsize)
    demo_instance.calculate_indicators()
    demo_instance.generate_flags()
    demo_instance.generate_report(output_dir)
        
    # Initialize HDDS instance and calculate indicators
    hdds_instance = HDDS(demo_instance.df.copy(), 
                         low_erroneous=hdds_low_erroneous,
                         high_erroneous=hdds_high_erroneous)
    hdds_instance.calculate_hdds()
    hdds_instance.generate_flags()
    hdds_instance.generate_report(output_dir)
    
    # Initialize FEXP_7D instance and calculate indicators
    fexp_7d_instance = FEXP_7D(hdds_instance.df.copy(), 
                                low_erroneous=HHExpF_7D_low_erroneous,
                                high_erroneous=HHExpF_7D_high_erroneous)
    fexp_7d_instance.calculate_indicators()
    fexp_7d_instance.generate_flags()
    fexp_7d_instance.generate_report(output_dir)
        
    # Initialize NFEXP_1M instance and calculate indicators
    nfexp_1m_instance = NFEXP_1M(fexp_7d_instance.df.copy(), 
                                low_erroneous=HHExpNF_1M_low_erroneous,
                                high_erroneous=HHExpNF_1M_high_erroneous)
    nfexp_1m_instance.calculate_indicators()
    nfexp_1m_instance.generate_flags()
    nfexp_1m_instance.generate_report(output_dir)
    
    # Initialize NFEXP_6M instance and calculate indicators
    nfexp_6m_instance = NFEXP_6M(nfexp_1m_instance.df.copy(), 
                                low_erroneous=HHExpNF_6M_low_erroneous,
                                high_erroneous=HHExpNF_6M_high_erroneous)
    nfexp_6m_instance.calculate_indicators()
    nfexp_6m_instance.generate_flags()
    nfexp_6m_instance.generate_report(output_dir)
    