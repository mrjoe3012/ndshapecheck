"""
https://github.com/mrjoe3012/shapecheck/issues/18
"""
from shapecheck.shape_check import ShapeCheck

def test_regression_18() -> None:
    sc = ShapeCheck()
    assert sc('N,1?').check((3,))
    assert sc('N,1?').check((3,1))
