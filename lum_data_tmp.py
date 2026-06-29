import pandas as pd

class Data_tmp():
    """Placeholder class to develop import window"""

    def __init__(self):
        self.data = pd.DataFrame()

    def __str__(self):
        return self.data.__str__()
    
    def add_data(self, other):
        '''Replaces empty databse with a full one, or appends new columns'''
        if self.data.empty:
            self.data = other
        else:
            for column in list(other.columns.values):
                if column not in list(self.data.columns.values):
                    self.data[column] = other[column]
        return self.data
    
    def replace_data(self, other):
        '''Adds data while replacing duplicated columns'''
        for column in list(other.columns.values):
            self.data[column] = other[column]
        return self.data
