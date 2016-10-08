import itertools
import collections

def rewrite(word, relations):
    dirty = True
    while dirty:
        dirty = False
        for left,right in relations:
            index = word.find(left)
            while index != -1:
                word = word[:index] + right + word[index + len(left):]
                index = word.find(left)
                dirty = True
    return word

def reduce_relations(relations):
    kept = [1 for r in relations]
    for i,r in enumerate(relations):
        for j,s in enumerate(relations):
            if i != j and s[0] in r[0]:
                kept[i] = 0
                break
    return sorted(list(itertools.compress(relations, kept)))

def find_critical(relations):
    criticals = []
    for i,(r,rc) in enumerate(relations):
        for s,sc in relations[i+1:]:
            for j in range(1,len(r)+1):
                if r[-j:] != s[:j]:
                    break
            j -= 1
            if j != 0:
                print "!",r[:-j],s[:], r, s, j
                criticals.append((r[:-j]+s[:],((r,rc),(s,sc))))
    return criticals

def find_normal_words(gens, relations):
    kept = set([""])
    words = [""]
    while words:
        print words
        print kept
        print "-"*20
        word = words.pop()
        for g in gens:
            print g
            for new in [g + word, word + g]:
                print new
                if rewrite(new, relations) == new:
                    if new not in kept:
                        kept.add(new)
                        words.append(new)
    return kept

def from_presentation(relations, iterations=100):
    #relations = ((left,right),...)
    relations = sorted(relations)
    criticals = find_critical(relations)
    print criticals
    modified = True
    for i in range(iterations):
        modified = False
        for word,rels in criticals:
            left = rewrite(word, [rels[0]])
            right = rewrite(word, [rels[1]])
            print word
            print left, right
            print rewrite(left,relations), rewrite(right,relations)
            print "-"*20
            if len(left) < len(right) or (len(left) == len(right) and left < right):
                left,right = right,left
            if rewrite(left,relations) != rewrite(right,relations):
                print left, right, left > right
                modified = True
                relations.append((left, right))
        relations = reduce_relations(relations)
        criticals = find_critical(relations)
        if not modified:
            break
    return relations

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

def dihedral(n):
    operator_dict = {}
    for lr,lf in itertools.product(range(n), ["","f"]):
        lname = "{}{}".format(lf, lr)
        operator_dict[lname] = {}
        for rr,rf in itertools.product(range(n), ["","f"]):
            rname = "{}{}".format(rf, rr)
            result_f = "f" if lf != rf else ""
            if not rf:
                result_r = (lr + rr)%n
            else:
                result_r = ((n - lr) + rr) % n
            result_name = "{}{}".format(result_f,result_r)
            operator_dict[lname][rname] = result_name
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

    #TODO: group products; right now this is just cosets
    def __mul__(self, other):
        #right coset
        return set([ele * other for ele in self.elements.values()])

    def __rmul__(self, other):
        #left coset
        return set([other * ele for ele in self.elements.values()])

    @staticmethod
    def from_presentation(gens, relations, max_depth=25):
        #TODO: actually build a group
        assert "e" not in gens
        words = set()
        stack = [("",0)]
        while len(stack) > 0:
            current,depth = stack.pop()
            if depth > max_depth:
                print "hit max depth with", current
                continue
            for r in relations:
                while r in current:
                    loc = current.index(r)
                    current = current[:loc] + current[loc+len(r):]
            if current in words:
                continue
            words.add(current)
            for g in gens:
                stack.append((g+current,depth+1))
                stack.append((current+g,depth+1))
        return words

    def find_generators(self):
        generators = []
        options = [e.name for e in self.elements.values()]
        orders = {name:len(self[name]) for name in self.elements.keys()}
        while options:
            largest = self[max(options, key=lambda x : orders[x])]
            generators.append(largest)
            removed = set([largest.name])
            cycle =  largest * largest
            while cycle != largest:
                removed.add(cycle.name)
                cycle *= largest
            options = [o for o in options if o not in removed]

        return self._prune_generators(generators)

    def get_presentation(self):
        #TODO: how should i actually do this?
        generators = self.find_generators()
        inverses = [g.inverse() for g in generators]

        gen_identities = [[g,i] for g,i in zip(generators, inverses)]

        pair_identities = []

        for g in generators:
            for h in generators:
                if g != h:
                    product = g*h
                    inverted = product.inverse()
                    pair_identities.append([product, inverted])

        return generators, gen_identities + pair_identities


    def _prune_generators(self, generators):
        #not exhaustive, just takes care of obvious cases (eg, half of D being in generators)

        kept = set()
        seen = set()

        for g in generators:
            if g not in seen:
                kept.add(g)
            for h in generators:
                if h not in seen:
                    kept.add(h)
                seen.add(g*h)
                seen.add(h*g)
        return kept

    def order_by_subgroups(self, subgroups=None):
        #TODO:also assumes that identity is first lexicographically
        elements = sorted(self.elements.keys())
        #reverse order here, assuming the user wanted the first subgroup to be most prominent
        for subgroup in subgroups[::-1]:
            elements.sort(key=lambda x : sorted([ele.name for ele in self[x]*subgroup]))
        return elements

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

        def inverse(self):
            prev = self
            current = self
            new = self*self
            while new != self:
                prev = current
                current = new
                new *= self
            return prev
