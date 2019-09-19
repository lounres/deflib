import copy
import functools


# TODO: def all_surjections
# All maps from set_from to set_to
def all_maps(set_from, set_to):
    def plus(d, k, v):
        new_d = copy.deepcopy(d)
        new_d[k] = v
        return new_d

    if len(set_from) == 0:
        return [{}]
    New_set_from = copy.deepcopy(set_from)
    elem = New_set_from.pop()
    Pseudo_maps = all_maps(New_set_from, set_to)
    return functools.reduce(lambda res, arr: res + arr, [list(map(lambda dic: plus(dic, elem, e), Pseudo_maps)) for e in set_to], [])


# All injections from set_from to set_to
def all_injections(set_from, set_to):
    def plus(d, k, v):
        new_d = copy.deepcopy(d)
        new_d[k] = v
        return new_d

    if len(set_from) == 0:
        return [{}]
    New_set_from = copy.deepcopy(set_from)
    elem = New_set_from.pop()
    return functools.reduce(lambda res, arr: res + arr, [list(map(lambda dic: plus(dic, elem, e), all_injections(New_set_from, set_to - {e}))) for e in set_to], [])


# All bijections from set_from to set_to
def all_bijections(set_from, set_to):
    def plus(d, k, v):
        new_d = copy.deepcopy(d)
        new_d[k] = v
        return new_d

    if len(set_to) != len(set_from):
        return []
    if len(set_from) == 0:
        return [{}]
    New_set_from = copy.deepcopy(set_from)
    elem = New_set_from.pop()
    return functools.reduce(lambda res, arr: res + arr, [list(map(lambda dic: plus(dic, elem, e), all_injections(New_set_from, set_to - {e}))) for e in set_to], [])
