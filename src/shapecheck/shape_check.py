from __future__ import annotations
from shapecheck.shape_rule import ShapeRule

__all__ = ["ShapeCheck"]

class ShapeCheck:
    """
    Contains a context for maintaining consistency of symbols between
    subsequent shape checks.
    """
    def __call__(self, shape_str: str) -> ShapeRule:
        """
        :param shape_str: The shape string to parse.
        :returns: a shape rule which can be used to check if an array's shape conforms to it.
        """
        return ShapeRule(self, shape_str)
