"""
"""
from __future__ import annotations
from typing import TYPE_CHECKING

__all__ = ["ShapeCheck"]
if TYPE_CHECKING:
    from shapecheck.shape_rule import ShapeRule

class ShapeCheck:
    def __call__(self, shape_str: str) -> ShapeRule:
        return ShapeRule(self, shape_str)
