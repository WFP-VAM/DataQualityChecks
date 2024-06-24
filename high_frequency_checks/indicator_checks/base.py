class IndicatorChecks:
    def __init__(self, df):
        self.df = df

    def run_checks(self):
        raise NotImplementedError("run_checks method must be implemented in subclass")

    def write_to_excel(self, output_file, sheet_name):
        # Code to write the summary dataframes to Excel
        pass

    @staticmethod
    def read_data(file_path):
        # Code to read data from a file
        pass