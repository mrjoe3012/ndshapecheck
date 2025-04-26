# Copyright (c) 2025 Joseph Agrane
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
from ndshapecheck.shape_check import ShapeCheck

def test_single_shape_h1() -> None:
    def f(a, b):
        sc = ShapeCheck()
        return sc(a).check(b)
    assert f('1,2,3', (1,2,3))
    assert f('1', (1,))
    assert f('N,M', (5,5))
    assert f('N,1,M', (3, 1, 4))
    assert f('M?,1,2', (1,2))
    assert f('M?,1,2', (1,1,2))
    assert f('M+,3', (1, 3))
    assert f('M+,3', (1, 2, 3, 2, 1, 2, 3, 3))
    assert f('M*,1,2', (1, 2, 3, 4, 1, 2))
    assert f('M*,1,2', (1, 2))

def test_single_shape_s1() -> None:
    sc = ShapeCheck()
    def f(a, b):
        return sc(a).check(b)
    assert not f('1,2', (1,1))
    assert not f('A,B', (1,))
    assert not f('1,A*', (2,1))
    assert not f('1,A*', (2,))
    assert not f('A+', tuple())
    assert not f('3,A+,3', (3,3,3,3,2))

def test_context_h1() -> None:
    sc = ShapeCheck()
    assert sc('A, B, C').check((1920, 1080, 3))
    assert sc('A').check((1920,))
    assert sc('A,D?').check((1920, 5))
    assert sc('B,D?').check((1080, 5 ))
    sc = ShapeCheck()
    assert sc('N*,2').check((1, 2, 3, 2))
    assert sc('N*').check((1, 2, 3))
    assert sc('N*,B?,2').check((1, 2, 3, 2))
    assert sc('B?').check(tuple())

def test_context_s1() -> None:
    sc = ShapeCheck()
    assert sc('A, B, C, 2').check((1, 2, 3, 2))
    assert not sc('A,N?').check((2,))
    sc = ShapeCheck()
    assert sc('2,N+').check((2, 3, 2))
    assert not sc('A,N+').check((2, 3, 3, 2))
    sc = ShapeCheck()
    assert sc('A*,2,B?').check((1, 2, 3, 2, 4))
    assert not sc('C,B?').check((1,))

def test_why() -> None:
    def generate_error_msg(shape_string: str, shape: tuple[int, ...]) -> str:
        return f"The shape {shape} does not match the rule '{shape_string}'."
    sc = ShapeCheck()
    sc('1,2,3').check((1, 2, 3))
    assert sc.why == ''
    sc('N?,2').check((2,))
    assert sc.why == ''
    sc('N?,3').check((1, 3))
    assert sc.why == generate_error_msg('N?=(),3', (1, 3))
    sc = ShapeCheck()
    sc('2,A+').check((2, 2, 3))
    sc('2,A+').check((2, 2, 3, 4))
    assert sc.why == generate_error_msg('2,A+=(2, 3)', (2, 2, 3, 4))
    sc = ShapeCheck()
    sc('dims,N*').check((3, 56, 54))
    sc('dims,N*').check((4, 56, 54))
    assert sc.why == generate_error_msg('dims=(3,),N*=(56, 54)', (4, 56, 54))
    sc = ShapeCheck()
    sc('dims,N*').check((3, 56, 54))
    sc('dims,N*').check((3, 54, 56))
    assert sc.why == generate_error_msg('dims=(3,),N*=(56, 54)', (3, 54, 56))
    sc = ShapeCheck()
    sc('N,2').check((2, 3))
    assert sc.why == generate_error_msg('N,2', (2, 3))
