import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter

class Data_tmp():
    """Placeholder class to develop import window"""

    def __init__(self):
        self.data = pd.DataFrame()
        self.ratios = np.array([])
        self.sensitivity = np.array([])

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
        return 'Data added sucessfully'
    
    def replace_data(self, other):
        self.data = other

        #'''Adds data while replacing duplicated columns'''
        #for column in list(other.columns.values):
        #    self.data[column] = other[column]
        #return 'Data replaced sucessfully'
    
    def calculate_ratios(self):
        intesities = self.data.to_numpy(dtype='float32')

        A = intesities[:,None,:]

        B = (1/intesities)[None,:,:]

        self.ratios = A * B

        return self.ratios
    
    def calculate_sensitivity(self):
        self.calculate_ratios()
        derivative = np.gradient(self.ratios, self.data.columns, axis=2).__abs__()
        crude_sensitivity = derivative.__abs__() / self.ratios
        self.sensitivity = gaussian_filter(crude_sensitivity, sigma=0.5, axes=(0,1), radius=(5,5))
        return self.sensitivity


if __name__ == '__main__':

    data = Data_tmp()

    input = pd.DataFrame([[1,2], [1,2], [1,2]])
    print(input)

    data.add_data(input)

    data.calculate_ratios()

    data.calculate_sensitivity()

    print(data.sensitivity)


        
