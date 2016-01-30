def from_matrix(array):
    #TODO: checks on matrix properties
    lookup = array[0]
    operator_dict = {g:{} for g in lookup}
    for row in array:
        left = row[0]
        for right,element in zip(lookup,row):
            operator_dict[left][right] = element
    return Group(operator_dict)

def cyclic(n):
    operator_dict = {}
    for i in xrange(n):
        operator_dict[i] = {}
        for j in xrange(n):
            operator_dict[i][j] = (i+j)%n
    return Group(operator_dict)

class Group(object):

    def __init__(self, operator_dict):
        self.operator_dict = operator_dict

    def get_element(self, name):
        return self.Element(self, name)

    def multiply(self, left, right):
        return self.Element(self, self.operator_dict[left][right])

    def __getitem__(self, index):
        return self.Element(self, index)


    class Element(object):
        def __init__(self, group, name):
            self.name = name
            self.group = group

        def __mul__(self, other):
            return self.group.multiply(self.name, other.name)

        def __rmul__(self, other):
            return self.group.multiply(other.name, self.name)

        def __repr__(self):
            return "{} in [{}]".format(self.name, hash(self.group))

        def __str__(self):
            return str(self.name)
