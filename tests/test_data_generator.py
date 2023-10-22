# test_your_project_files.py

import unittest  # if using the unittest framework
import pytest     # if using pytest

from generators.data_generator import generate_data

# Example using unittest:
class TestYourProject(unittest.TestCase):
    def test_function_output(self):
        expected_value=10
        result = generate_data(10)
        self.assertEqual(result.shape[0], expected_value)

# Example using pytest:
def test_function_output():
    result = generate_data()
    assert result.shape[0] == expected_value
