"""
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shapecheck.shape_check import ShapeCheck

class ShapeRule:
    def __init__(self, context: ShapeCheck, shape_str: str) -> None:
        self._context = context
        self._shape_str = shape_str

    def __eq__(self, other: tuple[int, ...]) -> bool:
        if not isinstance(other, tuple):
            raise ValueError("ShapeRule can only be compared with tuple[int, ...].")
        other = tuple(
            int(x) for x in other 
        )
        return False
