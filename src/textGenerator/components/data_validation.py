from textGenerator.config.configuration import DataValidationConfig

import os 
import pandas as pd


class DataValidation:
    def __init__(self, config: DataValidationConfig, feature: str = "text"):
        '''
        creates an instance for Data Validation class
        it validates the structure of the input data for the model 
        before processing
        
        params:
            config: DataValidationConfig - configuration for the data validation 
            feature: str - name of the feature for the input
        '''
        self.config = config
        self.feature = feature
        
    def validate_data(self) -> bool:
        '''
        checks for the validation of the input data structure and 
        ordering, before transformation
        
        returns:
            bool: True if it validates else False
        '''
        try:
            validation_status = True 
            
            if not os.path.isfile(self.config.required_file):
                validation_status = False 
                with open(self.config.status_file, 'w') as file:
                    file.write(f"Validation status: {validation_status} due to file {self.config.required_file} not found")
            else:    
                dataset = pd.read_csv(self.config.required_file)
                
                if self.feature not in dataset.columns:
                    validation_status = False 
                    with open(self.config.status_file, 'w') as file:
                        file.write(f"Validation status: {validation_status} due to feature {self.feature} not found")
                        
                
            if validation_status:
                with open(self.config.status_file, 'w') as file:
                    file.write(f"Validation status: {validation_status}")
                    
            return validation_status
        
        except Exception as e:
            raise e