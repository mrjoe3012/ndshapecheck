# Copyright (c) 2025 Joseph Agrane
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
"""
Contains code for checking a shape rule which is expressed as a string of symbols
and literals.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional, overload, Sequence
from ndshapecheck.has_shape import HasShape
import re

__all__ = ["ShapeRule"]
if TYPE_CHECKING:
    from ndshapecheck.shape_check import ShapeCheck

def _parse_shape_str(shape_str: str) -> tuple[list[str], list[Optional[str]], list[int | None]]:
    """
    :param shape_str: A shape string consisting of symbols and literals seperated
        by commas.
    :returns: Tuple containing the symbols, modifiers and literals.
    """
    symbols: list[str] = []
    modifiers: list[Optional[str]] = []
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
            if elem[-1] in tuple('?*+'):
                num = int(elem[:-1])
            else:
                num = int(elem)
        except ValueError:
            num = None
        symbols.append(elem)
        literals.append(num)
        if elem[-1] in tuple('?*+'):
            modifiers.append(elem[-1])
        else:
            modifiers.append(None)
    return symbols, modifiers, literals

def _construct_rule_regex(symbols: list[str], modifiers: list[Optional[str]],
                          literals: Sequence[int | str | None]) -> str:
    """
    :param symbols: Symbols from __parse_shape_str
    :param modifiers: The modifiers which are one of * ? + or None.
    :param literals: Literal values from __parse_shape_str
    :returns: The regex pattern validating the rule.
    """
    n = len(symbols) # == len(literals)
    regex_parts: list[str] = []
    for i in range(n):
        modifier: str = modifiers[i] or ''
        if modifier in ['*', '+']:
            modifier += '?'
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
            with symbols involved in checking other arrays.
        :param shape_str: The string describing the rule.
        """
        self._context = context
        self._shape_str = shape_str
        self._symbols, self._modifiers, self._literals = _parse_shape_str(self._shape_str)

    def __get_pattern(self) -> str:
        """
        Fill the literals with values from context before
            constructing the regex pattern.
        :returns: Regex that can be used to match shape strings.
        """
        literals: list[str | int | None] = list(self._literals)
        modifiers: list[Optional[str]] = list(self._modifiers)
        for i, symbol in enumerate(self._symbols):
            if symbol in self._context._vars:
                literals[i] = ','.join(map(str, self._context._vars[symbol]))
                modifiers[i] = None
        return _construct_rule_regex(self._symbols, modifiers, literals)

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
        pattern = self.__get_pattern()
        match = re.fullmatch(pattern, shape_str)
        if match is None:
            # construct shape string with context values added in
            sub_shape_str = ','.join(
                [symbol + (f'={self._context._vars[symbol]}'
                    if symbol in self._context._vars else '') for symbol in self._symbols]
            )
            self._context._why = f"The shape {shape} does not match the rule '{sub_shape_str}'."
            return False
        for i, group_str in enumerate(match.groups()):
            # dont' enforce consistency for literals
            if self._literals[i] is not None:
                continue
            group_tuple = tuple(map(int, filter(bool, group_str.split(','))))
            self._context._vars[self._symbols[i]] = group_tuple
        return True
