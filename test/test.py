import pytest
import os, sys
import filecmp
import random
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from squishy import *
from huffman import *

class TestHuffman:
    def setup_method(self, method):
        self.yellow = Image.open('yellow.png')
        self.cyanmagenta = Image.open('cyanmagenta.png')

    def teardown_method(self, method):
        self.yellow = None
        self.cyanmagenta = None

    def test_count_symbols_one_col(self):
        counts = count_symbols(self.yellow)
        assert counts[0] == (99, 160000) and counts[1] == (226, 160000) and counts[2] == (235, 160000)

    def test_count_symbols_multi_col(self):
        counts = count_symbols(self.cyanmagenta)
        assert counts[0] == (0, 8) and counts[1] == (255, 16)

    def test_build_tree_one_col(self):
        counts = count_symbols(self.yellow)
        tree = build_tree(counts)
        assert tree == (235, (99, 226))

    def test_build_tree_multi_col(self):
        counts = count_symbols(self.cyanmagenta)
        tree = build_tree(counts)
        assert tree == (0, 255)

    def test_assign_binary_patterns_one_col(self):
        counts = count_symbols(self.yellow)
        tree = build_tree(counts)
        codes = assign_binary_patterns(tree)
        assert codes == {235: [0], 99: [1, 0], 226: [1, 1]}

    def test_assign_binary_patterns_multi_col(self):
        counts = count_symbols(self.cyanmagenta)
        tree = build_tree(counts)
        codes = assign_binary_patterns(tree)
        assert codes == {0: [0], 255: [1]}

    def test_int_to_binary_zero(self):
        assert int_to_binary(0) == [0]

    def test_int_to_binary_one(self):
        assert int_to_binary(1) == [1]

    def test_int_to_binary_one(self):
        assert int_to_binary(1) == [1]

    def test_int_to_binary_multi_digit(self):
        assert int_to_binary(123) == [1, 1, 1, 1, 0, 1, 1]

    def test_binary_to_int_zero(self):
        assert binary_to_int([0]) == 0

    def test_binary_to_int_one(self):
        assert binary_to_int([1]) == 1

    def test_binary_to_int_multi_digit(self):
        assert binary_to_int([1, 0, 0, 0, 1, 0, 1]) == 69

    def test_pad_bits_random(self):
        num = random.randint(5,10)
        pattern = [1, 0]
        padded = pad_bits(pattern, num)
        assert padded == (num - len(pattern)) * [0] + pattern

    def test_pad_bits_byte(self):
        assert pad_bits(int_to_binary(3), 8) == [0, 0, 0, 0, 0, 0, 1, 1]