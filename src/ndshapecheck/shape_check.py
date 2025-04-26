# Copyright (c) 2025 Joseph Agrane
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
from __future__ import annotations
from ndshapecheck.shape_rule import ShapeRule

__all__ = ["ShapeCheck"]

class ShapeCheck:
    """
    Contains a context for maintaining consistency of symbols between
    subsequent shape checks.
    """
    def __init__(self) -> None:
        self._vars: dict[str, tuple[int, ...]] = {}
        self._why: str = ''

    def __call__(self, shape_str: str) -> ShapeRule:
        """
        :param shape_str: The shape string to parse.
        :returns: a shape rule which can be used to check if an array's shape conforms to it.
        """
        return ShapeRule(self, shape_str)

    @property
    def why(self) -> str:
        """
        :returns: The reason for the failure of a check() call.
        """
        return self._why
