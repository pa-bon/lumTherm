import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter

class DataHolder():
    """Class for data prosessing and storage"""

    def __init__(self):
        
        #data as imported from file
        self._raw_data = pd.DataFrame()
        
        #3D numpy array with intensity ratios
        self.ratios = np.array([])
        
        #3D numpy array with relative sensitivity
        self.sensitivity = np.array([])

    def __str__(self):
        return 'DataHolder containig the imported dataframe, the intensity ratois and the relative sensitivity'
    
    @property
    def raw_data(self):
        '''The raw_data property'''
        return self._raw_data
    
    @raw_data.setter
    def raw_data(self, new_data):
        '''Function used when substituing raw data with a simple `a = b` command'''
        self.set_raw_data(new_data)

    @raw_data.deleter
    def raw_data(self):
        '''Function used when deleiting the object with `del`.
        
        Deletion of raw data delets also derived data to avoid confusion'''
        self._raw_data = pd.DataFrame()
        self.ratios = np.array([])
        self.sensitivity = np.array([])
        
    def set_raw_data(self, new_data):
        '''Replace old raw (as imported) data with the new one
        
        Data must be a `pd.DataFrame`, indexes and headings must be numbers.'''

        try:
            #data must be pd.DataFrame
            assert isinstance(new_data, pd.DataFrame)

            #indexes and headings must be numbers
            assert 1 + new_data.index[0] + new_data.columns[0]

            self._raw_data = new_data

            return 'Message: Data replaced.'
        
        except AssertionError: #not a dataframe
            return 'Error: Raw data must be in form of Pandas DataFrame.'
        
        except TypeError: #index/headings not a number
            try:
                #convert index and headings to number
                new_data.columns  = [float(heading) for heading in new_data.columns]
                new_data.index = [float(index) for index in new_data.index]
                self._raw_data = new_data
                return 'Message: Data replaced after text to number conversion.'
            except:
                #unsucessfull conversion
                return 'Error: Both indexes and headings must be (convertable) to numbers.'
        
        except: #any other error
            return 'Error: Unknown error. Data replacement failed.'

    def get_xvalues(self):
        '''Returns x xalues (indexes) of the imported dataframe'''
        return list(self._raw_data.index)
    
    def get_zvalues(self):
        '''Returns z xalues (headings) of the imported dataframe'''
        return list(self._raw_data.columns)
    
    def get_raw_data_array(self):
        '''Return np.array with raw data'''
        return self._raw_data.to_numpy()

    def calculate_ratios(self):
        '''Calculates intensity ratios'''

        intesities = self._raw_data.to_numpy(dtype='float32')

        #a row-like matrix of intensities
        A = intesities[None,:,:]

        # a column-like matrix of inversed intensities
        B = (1/intesities)[:,None,:]

        #a true matrix product
        self.ratios = A * B

        return self.ratios
    
    def get_ratios(self):
        '''Return intensity ratios'''
        return self.ratios
    
    def calculate_sensitivity(self):
        '''Calculate relative sensitivity in %/K'''
        
        self.calculate_ratios()
        
        #derivative over temperature ('z' axis)
        derivative = np.gradient(self.ratios, self._raw_data.columns, axis=2).__abs__()
        
        #smoothing to even-out noise
        smoothed_derivative = gaussian_filter(derivative, sigma=1, axes=(0,1))
        
        #relative sensitivity in %/K
        self.sensitivity = smoothed_derivative * 100 / self.ratios
        
        return self.sensitivity
    
    def get_sensitivity(self):
        '''Return relative sensitivity'''
        return self.sensitivity

#testing
if __name__ == '__main__':

    print('Testing...')
    #set up 
    holder = DataHolder()

    input_1 = pd.DataFrame([[1,2], [1,2], [1,2]])
    ratios_1 = np.array([[[1,1],[1,1]],[[1,1],[1,1]],[[1,1],[1,1]]])
    sensitivity_1 = ratios_1 = np.array([[[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]]])
    
    input_2 = pd.DataFrame([[1,2], [1,2], [1,2]])
    input_2.index = [0,1,2]
    input_2.columns = ["0","1"]
    
    input_3 = pd.DataFrame([[1,2], [1,2], [1,2]])
    input_3.index = ['1', '2', '3']
    input_3.columns = ['one', 'two']

    holder.set_raw_data(input_1)
    
    assert holder._raw_data.equals(input_1)
    assert holder.raw_data.equals(input_1)
    assert np.array_equal(holder.get_raw_data_array(), np.array([[1,2], [1,2], [1,2]]))
    assert holder.get_xvalues() == [0,1,2]
    assert holder.get_zvalues() == [0,1]

    holder.raw_data = input_2
    input_2a = pd.DataFrame([[1,2], [1,2], [1,2]])
    input_2a.index = [0,1,2]
    input_2a.columns = ["0","1"]

    assert not holder.raw_data.equals(input_2a)
    assert holder.raw_data.equals(input_1)

    del holder.raw_data

    assert holder.raw_data.empty

    print(holder.set_raw_data(input_3))

    assert not holder.raw_data.equals(input_3)
    assert holder.raw_data.equals(pd.DataFrame([]))

    holder.raw_data = input_1

    print(holder.calculate_ratios())
    
    assert np.array_equal(holder.calculate_ratios(), ratios_1)
    assert np.array_equal(holder.get_ratios() == ratios_1)

    assert holder.calculate_sensitivity() == sensitivity_1
    assert holder.get_sensitivity() == sensitivity_1

    print('Tests passed')


        
