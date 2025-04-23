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

def __parse_shape_str(shape_str: str) -> tuple[list[Optional[str]], list[Optional[int]]]:
    """
    :param shape_str: A shape string consisting of symbols and literals seperated
    by commas.
    :returns: Tuple containing the symbols and literals. The lists are parallel and if
    symbols[i] is None then literals[i] is not None.
    """
    symbols: list[Optional[str]] = []
    literals: list[Optional[int]] = []
    
    elem_re = r'[a-zA-Z0-9_]+[+*?]?'
    shape_str_re = fr'\b*{elem_re}(?:,{elem_re})*'
    valid_m = re.fullmatch(shape_str_re, shape_str)
    if valid_m is None:
        raise ValueError(f"Invalid shape string '{shape_str}'")
    elements = re.findall(elem_re, shape_str) 
    for elem in elements:
        num = None
        try:
            num = int(elem)
        except ValueError:
            pass
        if num is None:
            symbols.append(elem)
            literals.append(None)
        else:
            symbols.append(None)
            literals.append(num)
    return symbols, literals

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
        raise NotImplementedError()
        return False
