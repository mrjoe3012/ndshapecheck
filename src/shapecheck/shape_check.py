"""
"""
from __future__ import annotations
from shapecheck.shape_rule import ShapeRule

__all__ = ["ShapeCheck"]

class ShapeCheck:
    def __call__(self, shape_str: str) -> ShapeRule:
        return ShapeRule(self, shape_str)
