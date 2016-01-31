from groupy import group
import pytest

def test_construct_from_matrix():
    matrix = [[0,1,2],
              [1,2,0],
              [2,0,1]]
    G = group.from_matrix(matrix)
    for i,row in enumerate(matrix):
        for j,element in enumerate(row):
            assert matrix[i][j] == G.operator_dict[i][j]

def test_group_access():
    matrix = [[0,1,2],
              [1,2,0],
              [2,0,1]]
    G = group.from_matrix(matrix)
    assert G[0].name == 0
    assert G[1].name == 1
    assert G[2].name == 2

@pytest.mark.parametrize("n",[1,4,7])
def test_construct_cyclic(n):
    C = group.cyclic(n)
    for i in xrange(n):
        for j in xrange(n):
            (C[i] * C[j]).name == (i+j)%n

def test_element_order():
    C = group.cyclic(6)
    expected = [1,6,3,2,3,6]
    for i in xrange(6):
        assert len(C[i]) == expected[i]

@pytest.mark.parametrize("n",[1,4,7])
def test_group_order(n):
    C = group.cyclic(n)
    assert len(C) == n

def test_left_coset():
    D = group.dihedral(4)
    F = D.subgroup([D["f0"]])
    expected = set(["1","f3"])
    coset = D["1"] * F
    names = set(c.name for c in coset)
    assert names == expected

def test_right_coset():
    D = group.dihedral(4)
    F = D.subgroup([D["f0"]])
    expected = set(["1","f1"])
    coset = F * D["1"]
    names = set(c.name for c in coset)
    assert names == expected
