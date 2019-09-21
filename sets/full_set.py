import copy


# Class of pseudo-full sets TODO: Дописать класс псевдополных множеств
class PseudoFullSet:
    def __init__(self):
        self.out_of_set = set()

    def add(self, other):
        self.out_of_set.remove(other)

    def __and__(self, other):
        copied_self = copy.copy(self)
        if type(other) == set:
            copied_self = other - self.out_of_set
        elif type(other) == PseudoFullSet:
            copied_self.out_of_set |= other.out_of_set
        else:
            raise TypeError("unsupported operand type(s) for +: 'PseudoFullSet' and '" + type(other).__name__ + "'")
        return copied_self

    def __or__(self, other):
        copied_self = copy.copy(self)
        if type(other) == set:
            copied_self.out_of_set -= other
        elif type(other) == PseudoFullSet:
            copied_self.out_of_set &= other.out_of_set
        else:
            raise TypeError("unsupported operand type(s) for +: 'PseudoFullSet' and '" + type(other).__name__ + "'")
        return copied_self

    def __sub__(self, other):
        copied_self = copy.copy(self)
        if type(other) == set:
            copied_self.out_of_set -= other
        elif type(other) == PseudoFullSet:
            copied_self.out_of_set |= other.out_of_set
        else:
            raise TypeError("unsupported operand type(s) for +: 'PseudoFullSet' and '" + type(other).__name__ + "'")
        return copied_self

    def __bool__(self):
        return bool(self.out_of_set)

    def __copy__(self):
        copied_self = PseudoFullSet
        copied_self.out_of_set = copy.copy(self.out_of_set)
        return copied_self
