import pandas as pd

class DataFrameCustomizer:
    def __init__(self, df):
        self.df = df

    def rename_columns(self):
        """
        Renames columns in the DataFrame according to the given mapping.
        
        Returns:
        pd.DataFrame: The DataFrame with renamed columns.
        """
        column_mapping = {
            'ID01': 'ADMIN1Name',
            'ID02': 'ADMIN2Name',
            'ID03': 'ADMIN3Name',
            'ID04LABEL': 'ADMIN4Name',
            'ID05': 'ADMIN5Name',
        }
        
        self.df = self.df.rename(columns=column_mapping)
        return self.df

    def create_urban_rural(self):
        """
        Creates 2 columns in the DataFrame "Urban" and "Rural".
        
        Returns:
        pd.DataFrame: The DataFrame with new columns "Urban" and "Rural".
        """
        self.df['Urban'] = self.df['ID06'].apply(lambda x: '1' if x == '1' else '0')
        self.df['Rural'] = self.df['ID06'].apply(lambda x: '1' if x == '2' else '0')
        
        # Optionally, you can drop the original ID06 column if needed
        # self.df.drop('ID06', axis=1, inplace=True)
        
        return self.df
