import pytest
import os, sys
import filecmp
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from squishy import *
squishy = Squishy()

def test_reconstructable():
    squishy.compress('penguin1.jpg')
    squishy.decompress('penguin1.bin', 'penguin1_new.png')
    assert images_equal('penguin1.jpg', 'penguin1_new.png')

def test_identical():
    squishy.compress('penguin1.jpg')
    squishy.compress('penguin2.jpg')
    assert filecmp.cmp('penguin1.bin', 'penguin2.bin')