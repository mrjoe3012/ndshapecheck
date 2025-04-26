Quickstart
==========

Requirements
------------

- Python 3.10 or newer

Installation
------------

Install the library with:

.. code-block:: bash

   pip install ndshapecheck

Basic Usage
-----------

Import the library:

.. code-block:: python

   from ndshapecheck import ShapeCheck

Create a `ShapeCheck` instance and verify shapes:

.. code-block:: python

   import numpy as np
   sc = ShapeCheck()

   assert sc('A,B,3').check(np.zeros(10, 10, 3)), sc.why # A = 10, B = 10
   assert sc('A,C*,3').check(np.zeros(10, 3, 2, 3, 3)), sc.why # C*=3, 2, 3

Notes
-----

- **Symbol Binding:** `ShapeCheck` objects *remember* symbol values between checks.
  
  In the example above, the first call sets `A=10` and `B=10`.  
  Subsequent checks using these symbols will fail if a value other than 10 is found within the
  shape.

- **Shape Rules:**  
  Shape rules are **comma-separated** strings.  
  Each element is either:
  
  - A non-negative integer (e.g., `3`, `5`)
  - A case-sensitive symbolic name (`A`, `B1`, `my_dim`)

- **Quantifiers:**  
  You can append standard regular expression quantifiers to symbols:

  - ``*`` — zero or more dimensions
  - ``+`` — one or more dimensions
  - ``?`` — optional dimension

- **Important:**  
  `A`, `A*`, `A?` and `A+` are treated as **separate symbols**.  
  Example:

  .. code-block:: python

     sc('A*,A').check(np.zeros((5, 10, 10)))
     # Assigns A* = (5,10) and A = 10 separately
  
- **Important:**
  If an optional symbol is omitted, it must also be omitted in future checks.
  Example:

  .. code-block:: python

     sc('optional_batch?,n_features').check((12,))  # no batch dimension
     sc('optional_batch?,n_labels').check((10, 3))  # fails. batch dimension should be omitted

- **Error Messages:**  
  If a shape check fails, `sc.why` contains a message string explaining why.
