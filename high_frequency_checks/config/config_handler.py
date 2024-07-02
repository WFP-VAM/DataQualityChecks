# config_handler.py
import yaml
import os
import high_frequency_checks as hfc_module

class ConfigHandler:
    def __init__(self, base_dir='high_frequency_checks/config'):
        self.base_dir = base_dir

    def read_yaml(self, file_path):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data

    def get_base_config(self):
        base_config_path = os.path.join(self.base_dir, 'configurable', 'base_indicator.yaml')
        base_config = self.read_yaml(base_config_path)
        base_cols = list(base_config.get('base_cols', []))
        review_cols = list(base_config.get('review_cols', []))
        return base_cols, review_cols

    def get_indicator_config(self, config_file):
        standard_config_dir = os.path.join(self.base_dir, 'standard')
        configurable_config_dir = os.path.join(self.base_dir, 'configurable')
        
        standard_config_path = os.path.join(standard_config_dir, config_file)
        configurable_config_path = os.path.join(configurable_config_dir, config_file)
        
        standard_config = self.read_yaml(standard_config_path)
        configurable_config = self.read_yaml(configurable_config_path)
        
        return standard_config, configurable_config
    
    def get_indicators(self):
        main_config_path = os.path.join(self.base_dir, 'main_config.yaml')
        main_config = self.read_yaml(main_config_path)
        
        enabled_indicators = [key for key, value in main_config['Indicators'].items() if value]
        mappings = main_config['Mappings']
        
        indicators = []
        for indicator_name in enabled_indicators:
            indicator_class = getattr(hfc_module, mappings[indicator_name]["class_name"])
            config_file = mappings[indicator_name]["config_file"]
            indicators.append((indicator_class, config_file))
        
        return indicators
