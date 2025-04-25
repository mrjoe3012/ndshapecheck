"""
Contains code for checking a shape rule which is expressed as a string of symbols
and literals.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional, overload
from shapecheck.has_shape import HasShape
import re

__all__ = ["ShapeRule"]
if TYPE_CHECKING:
    from shapecheck.shape_check import ShapeCheck

def _parse_shape_str(shape_str: str) -> tuple[list[str], list[Optional[int]]]:
    """
    :param shape_str: A shape string consisting of symbols and literals seperated
    by commas.
    :returns: Tuple containing the symbols and literals.
    """
    symbols: list[str] = []
    literals: list[Optional[int]] = []
    
    elem_re = r'[a-zA-Z0-9_]+[+*?]?'
    shape_str_re = fr'\s*{elem_re}(?:\s*,\s*{elem_re})*\s*'
    valid_m = re.fullmatch(shape_str_re, shape_str)
    if valid_m is None:
        raise ValueError(f"Invalid shape string '{shape_str}'")
    elements = re.findall(elem_re, shape_str) 
    for elem in elements:
        num = None
        try:
            if elem[-1] in '?*+':
                num = int(elem[:-1])
            else:
                num = int(elem)
        except ValueError:
            num = None
        symbols.append(elem)
        literals.append(num)
    return symbols, literals

def _construct_rule_regex(symbols: list[str], literals: list[Optional[int]]) -> str:
    """
    :param symbols: Symbols from __parse_shape_str
    :param literals: Literal values from __parse_shape_str
    :returns: The regex pattern validating the rule.
    """
    n = len(symbols) # == len(literals)
    regex_parts: list[str] = []
    for i in range(n):
        modifier = ''
        if symbols[i][-1] in '*+':
            modifier = f'{symbols[i][-1]}?'
        elif symbols[i][-1] == '?':
            modifier = symbols[i][-1]
        if literals[i] is not None:
            element = str(literals[i])
        else:
            element = '[1-9][0-9]*'
        regex_parts.append(f'((?:{element},?){modifier})')
    regex_pattern = "".join(regex_parts)
    return regex_pattern

class ShapeRule:
    """
    Encapsulates a rule for a multidimensional array's shape expressed as symbols and literals.
    """
    def __init__(self, context: ShapeCheck, shape_str: str) -> None:
        """
        :param context: The ShapeCheck which is used as a context to enforce consistency
        wiht symbols involved in checking other arrays.
        :param shape_str: The string describing the rule.
        """
        self._context = context
        self._shape_str = shape_str
        self._symbols, self._literals = _parse_shape_str(self._shape_str)
        self._pattern = _construct_rule_regex(self._symbols, self._literals)

    @overload
    def check(self, shape: HasShape) -> bool: ...
    @overload
    def check(self, shape: tuple[int, ...]) -> bool: ...
    def check(self, shape):
        """
        Has side-effects upon the context passed to the __init__ constructor by assigning
        shape values to provided symbols.
        :param shape: A multidimensional array's shape as a tuple
        of integers.
        :returns: True if the provided shape matches the rule.
        """
        if isinstance(shape, HasShape):
            return self.check(shape.shape)
        elif not isinstance(shape, tuple):
            raise ValueError("shape must be a tuple of integers.")
        shape = tuple(int(x) for x in shape)
        shape_str = ','.join(map(str, shape))
        match = re.fullmatch(self._pattern, shape_str)
        return match is not None
