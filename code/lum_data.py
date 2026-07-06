import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter

class DataHolder():
    """Class for data prosessing and storage"""

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
        '''Replaces old data with new data'''
        self.data = other
        return 'Data updated'
    
    def calculate_ratios(self):
        '''Calculate intensity ratios'''

        intesities = self.data.to_numpy(dtype='float32')

        A = intesities[None,:,:]

        B = (1/intesities)[:,None,:]

        self.ratios = A * B

        return self.ratios
    
    def calculate_sensitivity(self):
        '''Calculate relative sensitivity'''
        
        self.calculate_ratios()
        derivative = np.gradient(self.ratios, self.data.columns, axis=2).__abs__()
        
        #smoothing to even-out noise
        smoothed_derivative = gaussian_filter(derivative, sigma=1, axes=(0,1))
        
        self.sensitivity = smoothed_derivative.__abs__() * 100 / self.ratios
        return self.sensitivity
        

if __name__ == '__main__':

    data = DataHolder()

    input = pd.DataFrame([[1,2], [1,2], [1,2]])
    print(input)

    data.add_data(input)

    data.calculate_ratios()

    data.calculate_sensitivity()

    print(data.sensitivity)


        
