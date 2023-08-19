from textSummarizer.config.configuration import DataValidationConfig

import os 


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        '''
        creates an instance for Data Validation class 
        it validates the structure of the input data for the model
        
        params:
            config: DataValidationConfig - configuration for the data validation
        '''
        self.config = config
        
    def validate_all_files(self) -> bool:
        '''
        checks for the validation of the input data structure and 
        ordering for the model
        
        returns:
            bool: True if it validates otherwise False
        '''
        try:
            validation_status = True
            
            all_files = os.listdir(self.config.data_path)
            for file in self.config.ALL_REQUIRED_FILES:
                if file not in all_files:
                    validation_status = False 
                    with open(self.config.STATUS_FILE, 'w') as file:
                        file.write(f"Validation status: {validation_status} due to file: {file}")
            
            if validation_status:
                with open(self.config.STATUS_FILE, 'w') as file:
                    file.write(f"Validation status: {validation_status}")
            
            return validation_status

        except Exception as e:
            raise e 
            