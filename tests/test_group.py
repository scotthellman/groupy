from groupy import group

def test_construct_from_matrix():
    matrix = [[0,1,2],
              [1,2,0],
              [2,0,1]]
    G = group.Group.from_matrix(matrix)
    for i,row in enumerate(matrix):
        for j,element in enumerate(row):
            assert matrix[i][j] == G.operator_dict[i][j]
