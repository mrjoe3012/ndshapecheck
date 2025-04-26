Examples
========

The examples below pass a ``tuple`` to the ``check`` method. In practice you can pass any instance
with a ``shape`` property.

Basic Usage
-----------

You can use ``ShapeCheck`` to verify that array shapes match a pattern:

.. code-block:: python

   from ndshapecheck.shape_check import ShapeCheck

   sc = ShapeCheck()
   sc('1,2,3').check((1, 2, 3))  # ✅ Passes
   sc('N,M').check((5, 5))       # ✅ N = 5, M = 5
   sc('N,1,M').check((3, 1, 4))  # ❌ Fails
   sc('N,1,M').check((5, 1, 5))  # ✅ N = 5, M = 5

Symbols
-------

Symbols (like ``N``, ``M``, ``A``) represent dimensions that can match any value:

.. code-block:: python

   sc = ShapeCheck()
   sc('A,B,C').check((1920, 1080, 3))  # ✅ A=1920, B=1080, C=3
   sc('A').check((1920,))              # ✅ A=1920

Optional Dimensions (?)
------------------------

Use ``?`` to indicate a dimension may or may not be present:

.. code-block:: python

   sc = ShapeCheck()
   sc('M?,1,2').check((1, 2))         # ✅ M? is omitted
   sc('M?,1,2').check((1, 1, 2))      # ❌ Fails, M? should be omitted.


Multiple Dimensions (* and +)
-----------------------------

- ``*``: Zero or more dimensions
- ``+``: One or more dimensions

.. code-block:: python

   sc = ShapeCheck()
   sc('longer_symbol_1+,3').check((1, 3))                   # ✅ 'longer_symbol_1+'=1
   sc('longer_symbol_2+,3').check((1, 2, 3, 5, 4, 10, 3, 3))# ✅ 'longer_symbol_2+'=(1,2,3,5,4,10,3,3)

   sc('N*').check((1, 2, 3))                  # ✅ N*=(1,2,3)
   sc('N*,2').check((1, 2, 3, 2))             # ✅

Consistency of Symbols Across Checks
-------------------------------------

A ``ShapeCheck`` instance remembers the values assigned to symbols between checks.

.. code-block:: python

   sc = ShapeCheck()

   sc('N,M').check((1, 2))  # ✅ N=1, M=2

   sc('N,2?').check((1,))  # ✅ N=1, second dim=(), OK

   sc('N,2').check((2, 2))  # ❌ Fails: N = 1, got 2

If you want independent checks with fresh symbols, create a new ``ShapeCheck()`` instance.

ShapeCheck.why
--------------

If a shape check fails, ``ShapeCheck`` records a human-readable explanation in ``why``.

.. code-block:: python

   sc = ShapeCheck()

   sc('N?,1,2,3').check((1, 2, 3))
   print(sc.why)  # ''

   sc('N?,3').check((1, 3))
   print(sc.why)  # "The shape (1, 3) does not match the rule 'N?=(),3'."

   sc('dims,N*').check((3, 56, 54))
   sc('dims,N*').check((4, 56, 54))
   print(sc.why)  # "The shape (4, 56, 54) does not match the rule 'dims=(3,),N*=(56, 54)'."

Invalid Examples
----------------

These examples show when a shape does **not** match:

.. code-block:: python

   sc('1,2').check((1,1))         # ❌ Different second dimension
   sc('A,B').check((1,))          # ❌ Missing B
   sc('1,A*').check((2,1))        # ❌ Different first dimension.
   sc('X?,A+').check((3,))        # ❌ Needs at least one more for A
