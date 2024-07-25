import os
import yaml
import pandas as pd
import logging

class ConfigGenerator:
    def __init__(self, csv_file=None, output_dir=None):
        self.csv_file = csv_file or 'high_frequency_checks/config/config.csv'
        self.output_dir = output_dir or 'high_frequency_checks/config/configurable'
        self.df = None
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def setup(cls):
        csv_file = 'high_frequency_checks/config/config.csv'
        output_dir = 'high_frequency_checks/config/configurable'
        
        logger = logging.getLogger(cls.__name__)
        logger.debug(f"Setting up the output directory: {output_dir}")
        
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                logger.debug(f"Created directory: {output_dir}")
            except Exception as e:
                logger.error(f"Failed to create directory: {output_dir}, error: {e}")
        
        return cls(csv_file, output_dir)
    
    def load_csv(self):
        try:
            self.df = pd.read_csv(self.csv_file)
            self.logger.debug(f"Loaded CSV file: {self.csv_file}")
        except FileNotFoundError:
            self.logger.error(f"CSV file '{self.csv_file}' not found.")
            raise
    
    def identify_modules(self):
        modules = []
        if self.df is not None:
            for column in self.df.columns:
                if column.startswith('general/modules/') and self.df[column].iloc[0] == True:
                    module_name = column.split('/')[-1]
                    modules.append(module_name)
        return modules
    
    def parse_config_settings(self, module):
        config = {}
        if self.df is not None:
            for column in self.df.columns:
                if column.startswith(f'{module}/'):
                    config_key = column  # Get everything after 'module_name/'
                    module_name, rest = config_key.split('/', 1)
                    if rest.count('/') == 1:  # List indicator
                        parent_key, list_key = rest.split('/')
                        parent_key = parent_key.replace(module_name+'_', '')
                        if parent_key not in config:
                            config[parent_key] = []
                        if self.df[column].iloc[0] == True:
                            config[parent_key].append(list_key)
                    else:  # Single value
                        config_value = pd.to_numeric(self.df[column], errors='coerce').fillna(self.df[column]).tolist()
                        if len(config_value) == 1:  # Convert to single value instead of list
                            config_value = config_value[0]
                        config_key = config_key.replace(module_name+'_', '')
                        config[config_key] = config_value

            # Add hardcoded time_thresholds for the timing module
            if module == "timing":
                config['time_thresholds'] = {
                    'early_morning': {
                        'start': "0",
                        'end': "7"
                    },
                    'morning': {
                        'start': "7",
                        'end': "12"
                    },
                    'afternoon': {
                        'start': "12",
                        'end': "19"
                    },
                    'evening': {
                        'start': "19",
                        'end': "21"
                    },
                    'night': {
                        'start': "21",
                        'end': "24"
                    }
                }
        return config

    def create_base_indicator_yaml(self):
        yaml_content = {
            'base_cols': [
                '_uuid',
                'EnuName',
                'EnuSupervisorName',
                'ADMIN1Name',
                'ADMIN2Name',
                'ADMIN3Name',
                'ADMIN4Name'
            ]
        }
        yaml_filename = os.path.join(self.output_dir, 'base_indicator.yaml')
        
        # Ensure the directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        try:
            with open(yaml_filename, 'w') as yaml_file:
                yaml.dump(yaml_content, yaml_file, default_flow_style=False)
            self.logger.debug(f'Created {yaml_filename}')
        except Exception as e:
            self.logger.error(f"Failed to create YAML file '{yaml_filename}', error: {e}")
    
    def generate_configs(self):
        self.load_csv()
        self.create_base_indicator_yaml()
        modules = self.identify_modules()
        
        # Ensure the directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        for module in modules:
            config = self.parse_config_settings(module)
            clean_config = {}
            
            for key, value in config.items():
                if isinstance(value, list):
                    # Flatten lists
                    clean_config[key] = value
                else:
                    clean_key = key.split('/', 2)[-1].split('/')[-1]  # Remove module and parent keys
                    clean_config[clean_key] = value
            
            yaml_filename = os.path.join(self.output_dir, f'{module}.yaml')
            try:
                with open(yaml_filename, 'w') as yaml_file:
                    yaml.dump(clean_config, yaml_file, default_flow_style=False)
                self.logger.debug(f'Created {yaml_filename}')
            except Exception as e:
                self.logger.error(f"Failed to create YAML file '{yaml_filename}', error: {e}")
