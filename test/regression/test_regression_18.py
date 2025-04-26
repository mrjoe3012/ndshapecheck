# Copyright (c) 2025 Joseph Agrane
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# https://github.com/mrjoe3012/ndshapecheck/issues/18
from ndshapecheck.shape_check import ShapeCheck

def test_regression_18() -> None:
    sc = ShapeCheck()
    assert sc('N,1?').check((3,))
    assert sc('N,1?').check((3,1))
