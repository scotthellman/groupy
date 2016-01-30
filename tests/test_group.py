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
