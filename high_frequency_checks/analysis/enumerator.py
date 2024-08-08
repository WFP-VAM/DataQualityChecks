import pandas as pd
import logging
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from data_bridges_config import DATA_BRIDGES_CONFIG

# Configure logging
logging.basicConfig(filename='enumerator_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EnumeratorFlagsReport:
    def __init__(self, file_directory):
        self.file_directory = file_directory
        self.logger = logging.getLogger(__name__)
        self.common_columns = ['_uuid', 'EnuName', 'EnuSupervisorName', 'ADMIN1Name', 'ADMIN2Name',
                               'ADMIN3Name', 'ADMIN4Name', 'today']

    def read_excel_sheet(self, sheet_name):
        try:
            sheet = pd.read_excel(self.file_directory, sheet_name)
            self.logger.info(f'Done reading sheet: {sheet_name}')
            return sheet
        except Exception as e:
            self.logger.error(f"Error reading sheet {sheet_name}: {e}")
            return None

    def create_flag_column(self, df, condition, new_col_name):
        df[new_col_name] = condition.astype(int)
        return df

    def filter_dataframe(self, df, flag_column):
        return df[df[flag_column] == 1]

    def create_summary_table(self, df, col):
        return df.groupby('EnuName').agg({col: 'sum'}).reset_index()

    def add_error_percentage(self, df, flag_col, count_col='Count'):
        df[f'{flag_col}_Err_%'] = (df[flag_col] / df[count_col])
        return df.sort_values(by=[f'{flag_col}_Err_%', count_col], ascending=[False, False])

    def merge_and_sort_summaries(self, summary_counts, summary_flag, flag_col):
        merged_summary = pd.merge(summary_counts, summary_flag, on='EnuName', how='left').fillna(0)
        return self.add_error_percentage(merged_summary, flag_col)

    def generate_report(self):
        try:
            dataframes = self.read_and_preprocess_data()
            summary_counts = self.create_summary_counts(dataframes['HHEXPNF_6M'])
            
            flagged_dataframes = self.create_flags(dataframes)
            merged_df = self.merge_filtered_data(flagged_dataframes)
            
            summary_reports = self.generate_summary_reports(merged_df, summary_counts)
            final_report = self.create_final_report(summary_counts, summary_reports)
            
            self.save_report(final_report)
            return final_report
        except Exception as e:
            self.logger.error(f"Error generating enumerator flags report: {e}")
            return None

    def read_and_preprocess_data(self):
        sheets = ['Timing', 'FCS', 'rCSI', 'HHEXPNF_6M']
        dataframes = {sheet: self.read_excel_sheet(sheet) for sheet in sheets}
        
        incomplete_uuids = dataframes['rCSI'][dataframes['rCSI']['Flag_rCSI_Missing'] == 1]['_uuid'].tolist()
        dataframes['HHEXPNF_6M'] = dataframes['HHEXPNF_6M'][~dataframes['HHEXPNF_6M']['_uuid'].isin(incomplete_uuids)]
        
        return dataframes

    def create_summary_counts(self, df):
        return df.groupby('EnuName').size().reset_index(name='Count')

    def create_flags(self, dataframes):
        dataframes['Timing'] = self.create_flag_column(
            dataframes['Timing'], 
            (dataframes['Timing']['Flag_Timing_Invalid_Duration'] == 1) | 
            (dataframes['Timing']['Flag_Timing_Short_Duration'] == 1) | 
            (dataframes['Timing']['Flag_Timing_Abnormal_Start_Period'] == 1), 
            'Flag_Timing_NoLongDuration'
        )
        dataframes['FCS'] = self.create_flag_column(
            dataframes['FCS'], 
            (dataframes['FCS']['Flag_FCS_Overall'] == 1) & 
            (dataframes['FCS']['Flag_FCS_Missing'] == 0), 
            'FCS_Flag_NoMissing'
        )
        dataframes['rCSI'] = self.create_flag_column(
            dataframes['rCSI'], 
            (dataframes['rCSI']['Flag_rCSI_Overall'] == 1) & 
            (dataframes['rCSI']['Flag_rCSI_Missing'] == 0), 
            'rCSI_Flag_NoMissing'
        )
        return dataframes

    def merge_filtered_data(self, dataframes):
        filtered_dfs = {
            'Timing': self.filter_dataframe(dataframes['Timing'], 'Flag_Timing_NoLongDuration'),
            'FCS': self.filter_dataframe(dataframes['FCS'], 'FCS_Flag_NoMissing'),
            'rCSI': self.filter_dataframe(dataframes['rCSI'], 'rCSI_Flag_NoMissing')
        }
        
        merged_df = pd.merge(filtered_dfs['Timing'], filtered_dfs['FCS'], on=self.common_columns, how='outer', suffixes=(None, None))
        merged_df = pd.merge(merged_df, filtered_dfs['rCSI'], on=self.common_columns, how='outer', suffixes=(None, None))
        
        merged_df['Flag_Final'] = ((merged_df['Flag_Timing_NoLongDuration'] == 1) |
                                (merged_df['FCS_Flag_NoMissing'] == 1) |
                                (merged_df['rCSI_Flag_NoMissing'] == 1)).astype(int)
        
        return merged_df

    def generate_summary_reports(self, merged_df, summary_counts):
        flag_columns = ['Flag_Final', 'Flag_Timing_NoLongDuration', 'FCS_Flag_NoMissing', 'rCSI_Flag_NoMissing']
        summary_reports = {}
        
        for flag in flag_columns:
            summary = self.create_summary_table(merged_df, flag)
            summary_reports[flag] = self.merge_and_sort_summaries(summary_counts, summary, flag)
        
        return summary_reports

    def create_final_report(self, summary_counts, summary_reports):
        final_report = summary_counts.copy()
        
        for flag, report in summary_reports.items():
            columns_to_merge = ['EnuName', flag, f'{flag}_Err_%']
            final_report = pd.merge(final_report, report[columns_to_merge], on='EnuName', how='left')
        
        column_renames = {
            'Flag_Timing_NoLongDuration_Err_%': 'Timing_Err_%',
            'FCS_Flag_NoMissing_Err_%': 'FCS_Err_%',
            'rCSI_Flag_NoMissing_Err_%': 'rCSI_Err_%',
            'Flag_Final_Err_%': 'Overall_Err_%',
            'Flag_Timing_NoLongDuration': 'Timing_Flag',
            'FCS_Flag_NoMissing': 'FCS_Flag',
            'rCSI_Flag_NoMissing': 'rCSI_Flag'
        }
        final_report = final_report.rename(columns=column_renames)
        
        return final_report.sort_values(by=['Overall_Err_%', 'Count'], ascending=[False, False])

    def save_report(self, final_report):
        output_path = f"reports/{DATA_BRIDGES_CONFIG['country_name']}_Enumerator_Flags_Report.xlsx"
        final_report.to_excel(output_path, index=False)
        self.logger.info(f"Final report generated and saved to {output_path}")

if __name__ == "__main__":
    file_directory = 'reports/DRC_HFC_All_Indicators_Report.xlsx'
    enumerator_report = EnumeratorFlagsReport(file_directory)
    report = enumerator_report.generate_report()
    if report is not None:
        print("Report generated successfully")
    else:
        print("Failed to generate report")
