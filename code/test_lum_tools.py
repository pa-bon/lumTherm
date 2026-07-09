from lum_tools import (
    phriser, 
    phriser_list,
    phriser_range
)

def test_phriser():
    '''Test phriser function'''
    assert phriser('1,2,3,4') == (True, [1,2,3,4])
    assert phriser('1, 2-4') == (True, [1,2,3,4])
    assert phriser('1')
    assert not phriser('1, s2-4')[0]
    assert not phriser('1, s2-4')[1]
    assert not phriser(12)[0]
    assert not phriser(12)[1]
    assert phriser('')[0]
    assert not phriser('')[1]

def test_phriser_list():
    '''Test phriser_list function'''
    assert phriser_list('1,2,3,4') == [1,2,3,4]
    assert phriser_list('1.1, 1.2, 1.3') == [1.1,1.2,1.3]
    assert phriser_list('1')
    assert not phriser_list('1, 2-4')
    assert not phriser_list(12)

def test_phriser_range():
    '''Test phriser range function'''
    assert phriser_range('100,200,50') == [100,150,200]
    assert phriser_range('1,2,0.5') == [1.,1.5,2.0]
    assert phriser_range('1,2,0.2') == [1.,1.2,1.4,1.6,1.8,2.]
    assert not phriser_range('1')
    assert not phriser_range('w')
    assert not phriser_range('1,2,0.3')