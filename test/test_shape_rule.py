from shapecheck.shape_rule import __parse_shape_str

def test_parse_shape_str() -> None:
    symbols, literals = __parse_shape_str('1, 1, 15')
    assert symbols == [None, None, None]
    assert literals == [1, 1, 15]
    symbols, literals = __parse_shape_str('N?, A, myname_is_joe*, joe_is12_my_NAME+, B')
    assert symbols == ['N?', 'A', 'myname_is_joe*', 'joe_is12_my_NAME+', 'B']
    assert literals == [None, None, None, None, None]
    symbols, literals = __parse_shape_str('N?, 1, 2, joe_is_MY_name, 3')
    assert symbols == ['N?', None, None, 'joe_is_MY_name', None]
    assert literals == [None, 1, 2, None, 3]
