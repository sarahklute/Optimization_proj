import pytest
import numpy as np
import pandas as pd
from class_sorter import overallocation, time_conf, under_sup, unwill, unpref


@pytest.fixture
def cases():
    test1 = np.array(pd.read_csv('test1.csv', header=None))
    test2 = np.array(pd.read_csv('test2.csv', header=None))
    test3 = np.array(pd.read_csv('test3.csv', header=None))
    return [test1, test2, test3]

def test_overallocation(cases):
    test1 = cases[0]
    test2 = cases[1]
    test3 = cases[2]
    assert overallocation(test1) == 37, "Incorrect overallocation score"
    assert overallocation(test2) == 41, "Incorrect overallocation score"
    assert overallocation(test3) == 23, "Incorrect overallocation score"

def test_time_conf(cases):
    test1 = cases[0]
    test2 = cases[1]
    test3 = cases[2]
    assert time_conf(test1) == 8, "Incorrect overallocation score"
    assert time_conf(test2) == 5, "Incorrect overallocation score"
    assert time_conf(test3) == 2, "Incorrect overallocation score"
def test_under_sup(cases):
    test1 = cases[0]
    test2 = cases[1]
    test3 = cases[2]
    assert under_sup(test1) == 1, "Incorrect overallocation score"
    assert under_sup(test2) == 0, "Incorrect overallocation score"
    assert under_sup(test3) == 7, "Incorrect overallocation score"

def test_unwill(cases):
    test1 = cases[0]
    test2 = cases[1]
    test3 = cases[2]
    assert unwill(test1) == 53, "Incorrect overallocation score"
    assert unwill(test2) == 58, "Incorrect overallocation score"
    assert unwill(test3) == 43, "Incorrect overallocation score"

def test_unpref(cases):
    test1 = cases[0]
    test2 = cases[1]
    test3 = cases[2]
    assert unpref(test1) == 15, "Incorrect overallocation score"
    assert unpref(test2) == 19, "Incorrect overallocation score"
    assert unpref(test3) == 10, "Incorrect overallocation score"
