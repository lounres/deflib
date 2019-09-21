from functools import reduce
from itertools import starmap, chain
from copy import copy, deepcopy
from .CL import DynamicCoordList as DCL


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
        if not all([type(dirs[i][j]) in [type(None), int] for j in range(len(dirs[i]))]):
            if len(dirs[i]) != 1:
                raise ValueError('slice indices must be integers or None or tuples of integers')
            elif type(dirs[i][0]) not in tuple:
                raise ValueError('slice indices must be integers or None or tuples of integers')
            else:
                dirs[i] = dirs[i][0]
                if type(dirs[i]) == tuple and not (all([type(dirs[i][j]) == [type(None), int] for j in
                                                        range(len(dirs[i]))]) and len(dirs[i]) != dim):
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


class DynamicMultiDimCoordList:
    def __init__(self, dimension=1):
        self._dim = dimension
        self._list = DCL()
        self._str_in_proc = False

    @property
    def dim(self):
        return self._dim

    @property
    def right_len(self):
        if self.dim == 1:
            return self._list.right_len,
        else:
            L = [self._list[i].right_len for i in range(-self._list.left_len, self._list.right_len)]
            return (self._list.right_len, *[max([L[i][k] for i in range(len(L))]) for k in range(self.dim - 1)])

    @property
    def left_len(self):
        if self.dim == 1:
            return self._list.left_len,
        else:
            L = [self._list[i].left_len for i in range(-self._list.left_len, self._list.right_len)]
            return (self._list.left_len, *[max([L[i][k] for i in range(len(L))]) for k in range(self.dim - 1)])

    @property
    def sizes(self):
        if not self:
            return (0,) * self.dim
        return tuple(self.left_len[i] + self.right_len[i] for i in range(self.dim))

    def __len__(self):
        return reduce(lambda x, y: x * y, self.sizes)

    @property
    def indices(self):
        if self.dim == 1:
            return list(map(lambda i: (i,), self._list.indices))
        else:
            return sum(list(starmap(lambda L, i: [(i,) + index for index in L.indices], zip(list(self._list), self._list.indices))), [])

    def _optimise(self):
        if self.dim != 1:
            for i in self._list.indices:
                self._list[i]._optimise()
                if not self._list[i]:
                    del self._list[i]
        self._list._optimise()

    def __getitem__(self, item):
        if not self:
            return DynamicMultiDimCoordList(self.dim)

        item = _MDCL_item_check(item, self.dim)

        if type(item) is slice:
            item = [item.start, item.stop]
            left_len = self.left_len
            item[0] = tuple(-left_len[i] if item[0][i] is None else max(item[0][i], -left_len[i])
                            for i in range(self.dim))
            item[1] = tuple(self.right_len[i] if item[1][i] is None else min(item[1][i], self.right_len[i])
                            for i in range(self.dim))

            New = DynamicMultiDimCoordList(self.dim)

            for i in range(item[0][0], item[1][0]):
                if self.dim == 1:
                    try:
                        New._list[i] = self._list[i]
                    except IndexError:
                        pass
                else:
                    try:
                        if not New._list._index_check(i):
                            New._list[i] = DynamicMultiDimCoordList(self.dim - 1)
                        New._list[i][item[0][1:]:item[1][1:]] = self._list[i][item[0][1:]:item[1][1:]]
                    except IndexError:
                        pass

            New._optimise()
            return New

        elif type(item) is tuple:
            try:
                if self.dim == 1:
                    return self._list[item[0]]
                else:
                    return self._list[item[0]][item[1:]]
            except IndexError:
                raise IndexError('DynamicMultiDimCoordList index out of range')

    def __setitem__(self, *args):
        item, value = args
        item = _MDCL_item_check(item, self.dim)

        if type(item) is slice:
            if type(value) is not DynamicMultiDimCoordList:
                raise TypeError('can\'t assign object not of DynamicMultiDimCoordList to slice '
                                'of DynamicMultiDimCoordList')
            item = [item.start, item.stop]
            if self.dim != value.dim:
                raise ValueError('DynamicMultiDimCoordList slices must have the same number of dimensions')

            item[0] = tuple(-value.left_len[i] if item[0][i] is None else
                            max(item[0][i], -value.left_len[i])
                            for i in range(self.dim))
            item[1] = tuple(value.right_len[i] if item[1][i] is None else
                            min(item[1][i], value.right_len[i])
                            for i in range(self.dim))

            for i in range(item[0][0], item[1][0]):
                if self.dim == 1:
                    try:
                        self._list[i] = value._list[i]
                    except IndexError:
                        try:
                            del self._list[i]
                        except IndexError:
                            pass
                else:
                    try:
                        if not self._list._index_check(i):
                            self._list[i] = DynamicMultiDimCoordList(self.dim - 1)
                        self._list[i][item[0][1:]:item[1][1:]] = value._list[i][item[0][1:]:item[1][1:]]
                    except IndexError:
                        del self._list[i][item[0][1:]:item[1][1:]]

            self._optimise()

        elif type(item) is tuple:
            if self.dim == 1:
                self._list[item[0]] = value
            else:
                if not self._list._index_check(item[0]):
                    self._list[item[0]] = DynamicMultiDimCoordList(self.dim - 1)
                self._list[item[0]][item[1:]] = value
            self._optimise()

    def __delitem__(self, item):
        item = _MDCL_item_check(item, self.dim)

        if type(item) is slice:
            item = [item.start, item.stop]
            item[0] = tuple(-self.left_len[i] if item[0][i] is None else max(item[0][i], -self.left_len[i])
                            for i in range(self.dim))
            item[1] = tuple(self.right_len[i] if item[1][i] is None else min(item[1][i], self.right_len[i])
                            for i in range(self.dim))

            for i in range(item[0][0], item[1][0]):
                if self.dim == 1:
                    try:
                        del self._list[i]
                    except IndexError:
                        pass
                else:
                    try:
                        del self._list[i][item[0][1:]:item[1][1:]]
                    except IndexError:
                        pass

            self._optimise()

        elif type(item) is tuple:
            try:
                if self.dim == 1:
                    del self._list[item[0]]
                else:
                    del self._list[item[0]][item[1:]]
                self._optimise()
            except IndexError:
                raise IndexError('DynamicMultiDimCoordList index out of range')

    # def __eq__(self, other):  # TODO: Написать "=", "!="
    #     pass
    #
    # def __ne__(self, other):
    #     pass

    def shift(self, *shift):
        self._list.shift(shift[0])
        shift = shift[1:]
        for i in self._list.indices:
            self._list[i].shift(shift)

    def shifted(self, shift):
        New = copy(self)
        New.shift(shift)
        return New

    def __iter__(self):
        if self.dim == 1:
            return iter(self._list)
        else:
            return chain(*[iter(CL) for CL in iter(self._list)])

    def __bool__(self):
        return bool(len(self._list))

    def __str__(self):
        if self._str_in_proc:
            return '<SELF>'
        else:
            self._str_in_proc = True

            if self.dim == 1:
                result = str(self._list)
            else:
                if self._list.left_len < -2:
                    result = '[; <EMPTY>, ...(✕' + str(-self._list.left_len - 2) + '), <EMPTY>, ' +\
                           ', '.join(map(lambda pair: str(pair[0]) if pair[1] else '<EMPTY>',
                                         self._list._right_list[-self._list.left_len: self._list.right_len])) + ']'
                elif self._list.right_len < -2:
                    result = '[' + ', '.join(map(lambda pair: str(pair[0]) if pair[1] else '<EMPTY>',
                                                 self._list._left_list[-self._list.left_len: self._list.right_len: -1])) +\
                           '<EMPTY>, ...(X' + str(-self._list.right_len - 2) + ', <EMPTY>, ' + ']'
                else:
                    result = '[' + ', '.join(map(lambda pair: str(pair[0]) if pair[1] else '<EMPTY>',
                                                 list(reversed(self._list._left_list)))) +\
                           '; ' + ', '.join(map(lambda pair: str(pair[0]) if pair[1] else '<EMPTY>',
                                                self._list._right_list)) + ']'

            self._str_in_proc = False
            return result

    def __repr__(self):
        if self._str_in_proc:
            return '<SELF>'
        else:
            return 'DynamicCoordList(' + str(self) + ')'

    def __copy__(self):
        New = DynamicMultiDimCoordList(self.dim)
        New._list = copy(self._list)
        return New

    def __deepcopy__(self, memodict={}):
        if id(self) in memodict:
            return memodict[id(self)]

        memodict[id(self)] = DynamicMultiDimCoordList(self.dim)
        memodict[id(self)]._list = deepcopy(self._list)
        return memodict[id(self)]
