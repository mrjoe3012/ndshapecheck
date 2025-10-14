# Copyright (c) 2025 Joseph Agrane
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# https://github.com/mrjoe3012/ndshapecheck/issues/46
from ndshapecheck.shape_check import ShapeCheck

def test_regression_46() -> None:
    sc = ShapeCheck()
    assert sc('N,2').check((0, 2))
