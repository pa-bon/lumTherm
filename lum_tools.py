import numpy as np

def phriser(text: str):
    '''Converts strings to list of integers.
    
    String may contain numbers and ranges (eq. 1-5) seperated by commas.

    Examples:   '1,2,3,4'   '1, 2-4'    '' <- empty list
    
    Invalid inputs return empty list
    '''
    results = []
    if text == '':      #handels empty string
        return True, results
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

#testing
if __name__ == '__main__':
    
    print('Testing phriser()...')
    assert phriser('1,2,3,4') == [1,2,3,4]
    assert phriser('1, 2-4') == [1,2,3,4]
    assert phriser('1')
    assert not phriser('1, s2-4')
    assert not phriser(12)
    print('...tests pased')


def phriser_range(text: str):
    '''Converts strings to list of floats.
    
    String must contain tree integers corresponding to `start`, `stop` and `step`, seperated by commas.
    Expresion `(start - stop)` must be devisible by `step`.
    
    Invalid inputs return empty list
    '''
    results = []
    try:
        [start, stop, step] = [float(i.replace(' ','')) for i in  text.split(',')]
        results += [float(n) for n in np.arange(start, stop+step, step)]
        assert results[-1] == stop
        return results
    except:
        return []

#testing
if __name__ == '__main__':
    
    print('Testing phriser_range()...')
    assert phriser_range('100,200,50') == [100,150,200]
    assert phriser_range('1,2,0.5') == [1.,1.5,2.]
    assert not phriser_range('1')
    assert not phriser_range('w')
    assert not phriser_range('1,2,0.3')
    print('...tests pased')

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

#testing
if __name__ == '__main__':
    
    print('Testing phriser_list()...')
    assert phriser_list('1,2,3,4') == [1,2,3,4]
    assert phriser_list('1.1, 1.2, 1.3') == [1.1,1.2,1.3]
    assert phriser_list('1')
    assert not phriser_list('1, 2-4')
    assert not phriser_list(12)
    print('...tests pased')