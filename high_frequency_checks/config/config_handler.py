import yaml
import os
import logging
import high_frequency_checks as hfc_module

class ConfigHandler:
    def __init__(self, base_dir='high_frequency_checks/config'):
        """
        Initialize the ConfigHandler with a base directory for config files.

        Args:
            base_dir (str): The base directory for configuration files.
        """
        self.base_dir = base_dir
        self.logger = logging.getLogger(__name__)
    
    def read_yaml(self, file_path):
        """
        Read and parse a YAML file.

        Args:
        file_path (str): The path to the YAML file.

        Returns:
        dict: The parsed YAML data.

        Raises:
        FileNotFoundError: If the file is not found.
        """
        self.logger.info(f"Reading YAML file: {file_path}")
        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
            self.logger.info(f"Successfully read YAML file: {file_path}")
            return data
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing YAML file: {file_path}. Error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error reading file: {file_path}. Error: {e}")
            raise

    def get_base_config(self):
    """
    Retrieve the base configuration.

    Returns:
        tuple: A tuple containing base_cols and review_cols lists.
    """
        self.logger.info("Getting base config")
        try:
            base_config_path = os.path.join(self.base_dir, 'configurable', 'base_indicator.yaml')
            self.logger.info(f"Base config path: {base_config_path}")
            base_config = self.read_yaml(base_config_path)
            base_cols = list(base_config.get('base_cols', []))
            review_cols = list(base_config.get('review_cols', []))
            self.logger.info("Successfully retrieved base config")
            return base_cols, review_cols
        except Exception as e:
            self.logger.error(f"Error getting base config: {e}")
            raise

    def get_indicator_config(self, config_file):
        """
        Retrieve the configuration for a specific indicator.

        Args:
            config_file (str): The name of the configuration file.

        Returns:
            tuple: A tuple containing standard_config and configurable_config dictionaries.
        """
        self.logger.info(f"Getting indicator config for file: {config_file}")
        try:
            standard_config_dir = os.path.join(self.base_dir, 'standard')
            configurable_config_dir = os.path.join(self.base_dir, 'configurable')
            
            standard_config_path = os.path.join(standard_config_dir, config_file)
            configurable_config_path = os.path.join(configurable_config_dir, config_file)
            
            self.logger.info(f"Standard config path: {standard_config_path}")
            self.logger.info(f"Configurable config path: {configurable_config_path}")
            
            standard_config = self.read_yaml(standard_config_path)
            configurable_config = self.read_yaml(configurable_config_path)
            
            self.logger.info(f"Successfully retrieved indicator config for file: {config_file}")
            return standard_config, configurable_config
        except Exception as e:
            self.logger.error(f"Error getting indicator config for {config_file}: {e}")
            raise
    
    def get_indicators(self):
        """
        Retrieve all enabled indicators from the main configuration.

        Returns:
            list: A list of tuples containing (indicator_class, config_file) for each enabled indicator.
        """
        self.logger.info("Getting indicators from main config")
        try:
            main_config_path = os.path.join(self.base_dir, 'main_config.yaml')
            self.logger.info(f"Main config path: {main_config_path}")
            main_config = self.read_yaml(main_config_path)
            
            enabled_indicators = [key for key, value in main_config['Indicators'].items() if value]
            mappings = main_config['Mappings']
            
            indicators = []
            for indicator_name in enabled_indicators:
                self.logger.info(f"Processing indicator: {indicator_name}")
                indicator_class = getattr(hfc_module, mappings[indicator_name]["class_name"])
                config_file = mappings[indicator_name]["config_file"]
                indicators.append((indicator_class, config_file))
                self.logger.info(f"Added indicator: {indicator_name} with config file: {config_file}")
            
            self.logger.info("Successfully retrieved all indicators")
            return indicators
        except AttributeError as e:
            self.logger.error(f"Error accessing attribute: {e}")
            raise
        except KeyError as e:
            self.logger.error(f"Key error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error getting indicators: {e}")
            raise
