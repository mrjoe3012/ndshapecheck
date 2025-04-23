from typing import Protocol, runtime_checkable

__all__ = ['HasShape']

@runtime_checkable
class HasShape(Protocol):
    """
    Typing for objects with .shape property.
    """
    @property
    def shape(self) -> tuple[int, ...]:
        """
        :returns: Shape of the multidimensional array as a tuple of positive integers.
        """
        ...
