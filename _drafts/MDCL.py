from functools import reduce
from itertools import starmap, chain
from copy import copy, deepcopy
from ..lists import DynamicCoordList as DCL


def _MDCL_item_check(item, dim):
    SLs = []
    if type(item) is not tuple:
        item = [item]
    for i in range(len(item)):
        if type(item[i]) == slice:
            SLs.append(i)
    if len(SLs) > 1:
        raise ValueError('there must be at most one slice and it must be with None as step')
    if SLs:
        i = SLs[0]
        if item[i].step is not None:
            raise ValueError('there must be at most one slice and it must be with None as step')
        dirs = [(*item[:i], *item[i].start) if type(item[i].start) == tuple else (*item[:i], item[i].start),
                (*item[i].stop, *item[i+1:]) if type(item[i].start) == tuple else (item[i].stop, *item[i+1:])]
    else:
        dirs = [(*item,)]
    for i in range(len(dirs)):
        if not all([type(dirs[i][j]) == int for j in range(len(dirs[i]))]):
            if len(dirs[i]) != 1:
                raise ValueError('slice indices must be integers or None or tuples of integers')
            elif type(dirs[i][0]) not in [type(None), tuple]:
                raise ValueError('slice indices must be integers or None or tuples of integers')
            else:
                dirs[i] = dirs[i][0]
                if type(dirs[i]) == tuple and not (all([type(dirs[i][j]) == int for j in range(len(dirs[i]))]) and
                                                   len(dirs[i]) != dim):
                    if dim != 1:
                        raise ValueError('every index must be exactly ' + str(dim) + ' integers or tuple with them')
                    else:
                        raise ValueError('every index must be exactly 1 integer or tuple with it')
        else:
            if len(dirs[i]) != dim:
                if dim != 1:
                    raise ValueError('every index must be exactly ' + str(dim) + ' integers or tuple with them')
                else:
                    raise ValueError('every index must be exactly 1 integer or tuple with it')
    return slice(*dirs) if len(dirs) == 2 else dirs[0]


# Class of multi-dimensional list with any segment of indices by every coordinate
# class MultiDimCoordList:  # TODO: Написать класс координатного...
#     def __init__(self, iterative, start=0):
#         iterative = list(iterative)
#         self._correction = -start
#         self._list = iterative
#
#     @property
#     def correction(self):
#         return self._correction
#
#     def __len__(self):
#         return len(self._list)
#
#     @property
#     def start(self):
#         return self.correction
#
#     @property
#     def end(self):
#         return len(self) + self.correction - 1
#
#     @property
#     def stop(self):
#         return len(self) + self.correction
#
#     def __getitem__(self, item):
#         if type(item) is slice:
#             item = _CL_slice_check(item)
#             if item.step is None:
#                 item.step = 1
#             if item.step > 0:
#                 if item[0] is None:
#                     item[0] = 0
#                 else:
#                     item[0] += self.correction
#                     item[0] = max(item[0], item[0] % item.step)
#                 if item[1] is None:
#                     item[1] = len(self)
#                 else:
#                     item[1] = min(item[1] + self.correction, len(self))
#             else:
#                 if item[0] is None:
#                     item[0] = len(self)
#                 else:
#                     item[0] += self.correction
#                     item[0] = min(item[0], len(self) - 1 + (item[0] - len(self) + 1) % item.step)
#                 if item[1] is None:
#                     item[1] = 0
#                 else:
#                     item[1] = max(item[1] + self.correction, -1)
#
#             return self._list[item]
#         elif type(item) is int:
#             index = item
#             if not 0 <= index + self.correction < len(self):
#                 raise IndexError('CoordList index out of range')
#             else:
#                 return self._list[index + self.correction]
#         else:
#             raise TypeError('CoordList indices must be integers or slices, not ' + type(item).__name__)
#
#     def __setitem__(self, item, value):
#         if type(item) is slice:
#             item = _CL_slice_check(item)
#             if item.step is None:
#                 item.step = 1
#             if item.step > 0:
#                 if item[0] is None:
#                     item[0] = 0
#                 else:
#                     item[0] += self.correction
#                     item[0] = max(item[0], item[0] % item.step)
#                 if item[1] is None:
#                     item[1] = len(self)
#                 else:
#                     item[1] = min(item[1] + self.correction, len(self))
#             else:
#                 if item[0] is None:
#                     item[0] = len(self)
#                 else:
#                     item[0] += self.correction
#                     item[0] = min(item[0], len(self) - 1 + (item[0] - len(self) + 1) % item.step)
#                 if item[1] is None:
#                     item[1] = 0
#                 else:
#                     item[1] = max(item[1] + self.correction, -1)
#
#             if not hasattr(value, '__tuple__'):
#                 if not hasattr(value, '__list__'):
#                     raise TypeError('can only assign an iterable')
#                 else:
#                     value = list(value)
#             else:
#                 value = tuple(value)
#
#             if len(value) != -((item[0] - item[1]) // item.step):
#                 raise ValueError('attempt to assign sequence of size ' +
#                                  str(-((item[0] - item[1]) // item.step)) +
#                                  ' to extended slice of size ' +
#                                  str(len(value)))
#             else:
#                 self._list[item] = value
#
#         elif type(item) is int:
#             index = item
#             if not 0 <= index + self.correction < len(self):
#                 raise IndexError('CoordList index out of range')
#             else:
#                 self._list[index + self.correction] = value
#         else:
#             raise TypeError('CoordList indices must be integers or slices, not ' + type(item).__name__)
#
#     def __delitem__(self, item):
#         if type(item) is slice:
#             item = _CL_slice_check(item)
#             if item.step is None:
#                 item.step = 1
#             if item.step > 0:
#                 if item[0] is None:
#                     item[0] = 0
#                 else:
#                     item[0] += self.correction
#                     item[0] = max(item[0], item[0] % item.step)
#                 if item[1] is None:
#                     item[1] = len(self)
#                 else:
#                     item[1] = min(item[1] + self.correction, len(self))
#             else:
#                 if item[0] is None:
#                     item[0] = len(self)
#                 else:
#                     item[0] += self.correction
#                     item[0] = min(item[0], len(self) - 1 + (item[0] - len(self) + 1) % item.step)
#                 if item[1] is None:
#                     item[1] = 0
#                 else:
#                     item[1] = max(item[1] + self.correction, -1)
#
#             self._list[item] = [None] * -((item[0] - item[1]) // item.step)
#
#         elif type(item) is int:
#             index = item
#             if not 0 <= index + self.correction < len(self):
#                 raise IndexError('CoordList index out of range')
#             else:
#                 self._list[index + self.correction] = None
#         else:
#             raise TypeError('CoordList indices must be integers or slices, not ' + type(item).__name__)
#
#     def __iter__(self):
#         return iter(self._list)
#
#     def __reversed__(self):
#         return CoordList(reversed(self._list), start=-self.correction)
#
#     def __contains__(self, item):
#         return item in self._list
#
#     def __bool__(self):
#         return any(self._list)
#
#     def __copy__(self):
#         return CoordList(copy(self._list), start=-self.correction)
#
#     def __deepcopy__(self, memodict={}):
#         if id(self) in memodict:
#             return memodict[id(self)]
#
#         memodict[id(self)] = CoordList([], start=-self.correction)
#         memodict[id(self)]._list = deepcopy(self._list, memodict)
#         return memodict[id(self)]
#
#     def __repr__(self):
#         return 'CoordList(' + repr(self._list) + ', ' + 'start=' + str(-self.correction) + ')'
#
#     def __str__(self):
#         return 'CoordList(' + repr(self._list) + ', ' + 'start=' + str(-self.correction) + ')'