# Copyright (c) 2025 Joseph Agrane
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
import pytest

@pytest.fixture(autouse=True)
def no_output(capsys):
    yield
    stdout, stderr = capsys.readouterr()
    assert len(stdout) == 0 and len(stderr) == 0, \
        f"Captured outputs! No print statements are allowed. {stdout=} {stderr=}"
