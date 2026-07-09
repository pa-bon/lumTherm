'''
A collection of various functions usefull in many parts of the program. 
'''
import numpy as np

def phriser(text: str):
    '''Converts strings to list of integers.
    
    String may contain numbers and ranges (eq. 1-5) seperated by commas.

    Examples:   '1,2,3,4'   '1, 2-4'    '' <- empty list
    
    Invalid inputs return empty list
    '''
    results = []
    if text == '':      #handels empty string
        return True, []
    else:
        try:
            contents = [i.replace(' ','') for i in text.split(',')]
            for item in contents:
                if '-' in item:
                    [start, stop] = item.split('-')
                    results += list(range(int(start), int(stop)+1))     #stop included
                else:
                    results.append(int(item))
            return True, results
        except:        #any error
            return False, []

def phriser_range(text: str):
    '''Converts strings to list of floats.
    
    String must contain tree integers corresponding to `start`, `stop` and `step`, seperated by commas.
    Expresion `(start - stop)` must be devisible by `step`.
    Absolute value of 'step' must be at least 0.001.

    Examples: '1,4,1' '1.0, 2.0, 0.1', '10,0,-2'
    
    Invalid inputs return empty list
    '''
    results = []
    try:
        [start, stop, step] = [float(i.replace(' ','')) for i in  text.split(',')]
        num = ((stop-start)/step) + 1
        assert abs(num-int(num)) < 0.0001 #int() rounds to the nearest integer, this allows only for true integers
        results = [round(float(n), 4) for n in np.linspace(start, stop, int(num))]
        assert results[-1] == stop
        return results
    except:
        return []

def phriser_list(text: str):
    '''Converts strings to list of floats.
    
    String must contain numbers seperated by commas.

    Examples:   '1,2,3,4'   '1.0, 1.1, 1.2'
    
    Invalid inputs return empty list
    '''
    results = []
    try:
        contents = [i.replace(' ','') for i in text.split(',')]
        for item in contents:
            results.append(float(item))
        return results
    except:
        return []


def mark_text_edit_error(widget, condition):
    '''Changes the background of TextEdit widget to red when condition is false'''
    if condition:
        widget.setStyleSheet("""
                             QLineEdit { background-color: rgb(255, 255, 255)}
                             QPlainTextEdit { background-color: rgb(255, 255, 255)}
                             QTextEdit { background-color: rgb(255, 255, 255)}
                             """)
    else:
        widget.setStyleSheet("""
                             QLineEdit { background-color: rgb(255, 200, 200)}
                             QPlainTextEdit { background-color: rgb(255, 200, 200)}
                             QTextEdit { background-color: rgb(255, 200, 200)}
                             """)