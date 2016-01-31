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
        self.elements = {name:self.Element(self,name) for name in operator_dict.keys()}

    def get_element(self, name):
        return self.elements[name]

    def multiply(self, left, right):
        return self.elements[self.operator_dict[left][right]]

    def __getitem__(self, index):
        return self.elements[index]

    def __len__(self):
        return self.compute_order()

    #TODO: group producst; right now this is just cosets
    def __mul__(self, other):
        #right coset
        return [ele * other for ele in self.elements.values()]

    def __rmul__(self, other):
        #left coset
        return [other * ele for ele in self.elements.values()]

    def subgroup(self, generators):
        #TODO: bet this can be way more efficient!
        subgroup = set()
        novel = set(generators)
        while len(novel) > 0:
            subgroup |= novel
            novel = set()
            for left in subgroup:
                for right in subgroup:
                    result = left*right
                    if result not in subgroup:
                        novel.add(result)

        subgroup_dict = {}
        for left in subgroup:
            subgroup_dict[left.name] = {}
            for right in subgroup:
                subgroup_dict[left.name][right.name] = (left*right).name
        return Group(subgroup_dict)

    def compute_order(self):
        return len(self.elements)

    class Element(object):
        def __init__(self, group, name):
            self.name = name
            self.group = group
            #self.order = self.compute_order()

        def __mul__(self, other):
            if isinstance(other, Group):
                return other.__rmul__(self)
            try:
                return self.group.multiply(self.name, other.name)
            except KeyError:
                return other.group.multiply(self.name, other.name)

        #def __rmul__(self, other):
        #    return self.__mul__(other, self)

        def __eq__(self, other):
            return self.name == other.name and self.group == other.group

        def __ne__(self, other):
            return not self.__eq__(other)

        def __repr__(self):
            return "{} in [{}]".format(self.name, hash(self.group))

        def __str__(self):
            return str(self.name)

        def __len__(self):
            return self.compute_order()

        def compute_order(self):
            current = self*self
            count = 1
            while current != self:
                current*=self
                count += 1
            return count
