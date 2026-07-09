import pytest
import pandas as pd
import numpy as np
from lum_data import DataHolder

@pytest.fixture
def holder():
    '''Instance of class tested'''
    return DataHolder()

@pytest.fixture
def input_1():
    '''Typical, valid dataframe'''
    return pd.DataFrame([[1,2], [1,2], [1,2]])

@pytest.fixture
def input_2():
    '''Dataframe with text headings convertible to numbers'''
    input_2 = pd.DataFrame([[1,2], [1,2], [1,2]])
    input_2.index = [0,1,2]
    input_2.columns = ["0","1"]
    return input_2

@pytest.fixture
def input_3():
    '''Dataframe with headings not convertible to numbers (invalid)'''
    input_3 = pd.DataFrame([[1,2], [1,2], [1,2]])
    input_3.index = ['1', '2', '3']
    input_3.columns = ['one', 'two']
    return input_3

@pytest.fixture
def ratios_1():
    '''Results of intensity ratio calculations for `input_1`'''
    return np.array([[[1,1],[1,1],[1,1]],
                     [[1,1],[1,1],[1,1]],
                     [[1,1],[1,1],[1,1]]], 
                     dtype='float32')

@pytest.fixture
def sensitivity_1():
    '''Results of sensitivity calculations for `input_1`'''
    return np.array([[[0,0],[0,0],[0,0]],
                     [[0,0],[0,0],[0,0]],
                     [[0,0],[0,0],[0,0]]], 
                     dtype='float32')

def test_inicialization(holder):
    '''Tests the `__init__` block'''
    assert holder.raw_data.equals(pd.DataFrame())
    assert np.array_equal(holder.ratios, np.array([]))
    assert np.array_equal(holder.sensitivity, np.array([]))

def test_set_raw_data_1(holder, input_1):
    '''Tests handling of typical data'''
    holder.set_raw_data(input_1)
    assert holder.raw_data.equals(input_1)

def test_set_raw_data_2(holder, input_2, input_1):
    '''Tests handling of data with procesable text for index/headings'''
    holder.set_raw_data(input_2)
    assert holder.raw_data.equals(input_1)

def test_set_raw_data_3(holder, input_3):
    '''Tests handling of invalid data'''
    holder.set_raw_data(input_3)
    assert holder.raw_data.empty

def test_set_raw_data_4(holder, input_1, input_3):
    '''Test for not overwriting good data with bad data'''
    holder.set_raw_data(input_1)
    assert holder.raw_data.equals(input_1)
    holder.set_raw_data(input_3)
    assert holder.raw_data.equals(input_1)

def test_raw_data_property_1(holder, input_2, input_1):
    '''Tests `setter` for raw_data''' 
    holder.raw_data = input_2
    assert holder.raw_data.equals(input_1)

def test_raw_data_property_2(holder, input_1):
    '''Tests `deleter` for raw_data'''
    holder.set_raw_data(input_1)
    assert holder.raw_data.equals(input_1)
    del holder.raw_data
    assert holder.raw_data.empty

def test_ratios(holder, input_1, ratios_1):
    '''Test intsnsity ratio calculation'''
    holder.raw_data = input_1
    assert np.array_equal(holder.calculate_ratios(), ratios_1)
    assert np.array_equal(holder.ratios, ratios_1)

def test_sensitivity(holder, input_1, sensitivity_1):
    '''Test sensitivity calculation'''
    holder.raw_data = input_1
    assert np.array_equal(holder.calculate_sensitivity(), sensitivity_1)
    assert np.array_equal(holder.sensitivity, sensitivity_1)

def test_get_xvalues(holder, input_1):
    '''Test get_xvalues'''
    holder.raw_data = input_1
    assert holder.get_xvalues() == [0,1,2]

def test_get_zvalues(holder, input_1):
    '''Test get_zvalues'''
    holder.raw_data = input_1
    assert holder.get_zvalues() == [0,1]

def test_get_ratios(holder, input_1, ratios_1):
    '''Test get_ratios'''
    holder.raw_data = input_1
    holder.calculate_ratios()
    assert np.array_equal(holder.get_ratios(), ratios_1)

def test_get_sesnitivity(holder, input_1, sensitivity_1):
    '''Test get_sensitivity'''
    holder.raw_data = input_1
    holder.calculate_sensitivity()
    assert np.array_equal(holder.get_sensitivity(), sensitivity_1)

def test_get_raw_data_array(holder, input_1):
    '''Test get_raw_data_array'''
    holder.raw_data = input_1
    assert np.array_equal(holder.get_raw_data_array(), np.array([[1,2], [1,2], [1,2]]))






