# Copyright (c) 2025 Joseph Agrane
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
from ndshapecheck.shape_rule import _parse_shape_str, _construct_rule_regex
import re

def test_parse_shape_str() -> None:
    symbols, modifiers, literals = _parse_shape_str('1, 1?, 15')
    assert symbols == ['1', '1?', '15']
    assert literals == [1, 1, 15]
    assert modifiers == [None, '?', None]
    symbols, modifiers, literals = _parse_shape_str('N?, A, myname_is_joe*, joe_is12_my_NAME+, B')
    assert symbols == ['N?', 'A', 'myname_is_joe*', 'joe_is12_my_NAME+', 'B']
    assert literals == [None, None, None, None, None]
    assert modifiers == ['?', None, '*', '+', None]
    symbols, modifiers, literals = _parse_shape_str('N?, 1, 2, joe_is_MY_name, 3')
    assert symbols == ['N?', '1', '2', 'joe_is_MY_name', '3']
    assert literals == [None, 1, 2, None, 3]
    assert modifiers == ['?', None, None, None, None]

def test_construct_rule_regex() -> None:
    symbols = ['N+', '3']
    literals = [None, 3]
    modifiers = ['+', None]
    regex = _construct_rule_regex(symbols, modifiers, literals)
    assert re.fullmatch(regex, '1,2,3') is not None
    assert re.fullmatch(regex, '1,3') is not None
    assert re.fullmatch(regex, '3') is None
    assert re.fullmatch(regex, '3,2') is None
    symbols = ['1', 'N*', '1']
    literals = [1, None, 1]
    modifiers = [None, '*', None]
    regex = _construct_rule_regex(symbols, modifiers, literals)
    assert re.fullmatch(regex, '1,1') is not None
    assert re.fullmatch(regex, '1,1,1') is not None
    assert re.fullmatch(regex,'2,1,1') is None
    assert re.fullmatch(regex,'2,1,2,3,2') is None
    assert re.fullmatch(regex,'1,4,3,3,4,2') is None
    assert re.fullmatch(regex,'1,4,3,3,4,1') is not None
    symbols = ['1?', 'N', 'M?']
    literals = [1,None,None]
    modifiers = ['?', None, '?']
    regex = _construct_rule_regex(symbols, modifiers, literals)
    assert re.fullmatch(regex,'1,2') is not None
    assert re.fullmatch(regex,'2') is not None
    assert re.fullmatch(regex,'2,4') is not None
    assert re.fullmatch(regex,'1,2,3,3') is None
    assert re.fullmatch(regex,'2,3,3') is None
