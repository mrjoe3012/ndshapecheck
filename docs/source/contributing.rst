Contributing
============

Thank you for considering contributing to this project!

Below are the guidelines to help you get started.

Setup
-----

First, set up your development environment:

1. Install the package manager:

   .. code-block:: bash

      pip install uv

2. Install all development dependencies:

   .. code-block:: bash

      uv sync --group dev

Code Style
----------

We use **mypy** for type checking and **ruff** for linting.

Before submitting a pull request, please ensure:

- Code passes linting:

  .. code-block:: bash

      uv run ruff check src test

- Code passes type checking:

  .. code-block:: bash

      uv run mypy src test

Testing
-------

We use **pytest** for running tests.

- To run all tests:

  .. code-block:: bash

      uv run pytest test

Test organization:

- **Feature tests**: placed in the top-level project directory.
- **Regression tests**: placed under ``test/regression/`` and named:

  .. code-block:: bash

      test_regression_<issue_number>.py

Contribution Checklist
-----------------------

- Create your own fork
- Add yourself to ``contributors.md``.
- Add or update tests if needed.
- Add a copyright header:
  
  - You may add your name to the copyright line
    of any files you significantly modify or create.
- Create a pull request

Thank you for helping to improve the project!
