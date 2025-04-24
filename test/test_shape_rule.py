from shapecheck.shape_rule import __parse_shape_str, __construct_rule_regex
import re

def test_parse_shape_str() -> None:
    symbols, literals = __parse_shape_str('1, 1?, 15')
    assert symbols == ['1', '1?', '15']
    assert literals == [1, 1, 15]
    symbols, literals = __parse_shape_str('N?, A, myname_is_joe*, joe_is12_my_NAME+, B')
    assert symbols == ['N?', 'A', 'myname_is_joe*', 'joe_is12_my_NAME+', 'B']
    assert literals == [None, None, None, None, None]
    symbols, literals = __parse_shape_str('N?, 1, 2, joe_is_MY_name, 3')
    assert symbols == ['N?', '1', '2', 'joe_is_MY_name', '3']
    assert literals == [None, 1, 2, None, 3]

def test_construct_rule_regex() -> None:
    symbols = ['N+', '3']
    literals = [None, 3]
    regex = __construct_rule_regex(symbols, literals)
    assert re.fullmatch(regex, '1,2,3') is not None
    assert re.fullmatch(regex, '1,3') is not None
    assert re.fullmatch(regex, '3') is None
    assert re.fullmatch(regex, '3, 2') is None
