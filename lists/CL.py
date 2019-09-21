from copy import copy, deepcopy


def _CL_slice_check(S):
    def arg_check(st):
        if type(st) not in [int, type(None)]:
            try:
                st = st.__index__()
            except AttributeError or TypeError:
                raise TypeError('slice indices must be integers or None or have __index__ method')
        return st

    S = [arg_check(S.start), arg_check(S.stop), arg_check(S.step)]
    if S[2] == 0:
        raise ValueError('slice step cannot be zero')
    return S


class DynamicCoordList:
    def __init__(self):
        self._right_list = []
        self._left_list = []
        self._right_len = 0
        self._left_len = 0

        self._str_in_proc = False

    @property
    def right_len(self):
        return self._right_len

    @property
    def left_len(self):
        return self._left_len

    def __len__(self):
        return self.left_len + self.right_len

    @property
    def indices(self):
        return list(filter(lambda i: self._right_list[i][1] if i >= 0 else self._left_list[-i - 1][1],
                           range(-self.left_len, self.right_len)))

    def _optimise(self):
        right = len(self._right_list) - 1
        while right >= 0 and not self._right_list[right][1]:
            right -= 1

        del self._right_list[right + 1:]

        left = len(self._left_list) - 1
        while left >= 0 and not self._left_list[left][1]:
            left -= 1

        del self._left_list[left + 1:]

        if left == -1:
            if right == -1:
                self._left_len = 0
                self._right_len = 0
            else:
                self._right_len = right + 1
                i = 0
                while i < self.right_len and not self._right_list[i][1]:
                    i += 1
                self._left_len = -i
        else:
            self._left_len = left + 1
            if right == -1:
                i = 0
                while i < self.left_len and not self._left_list[i][1]:
                    i += 1
                self._right_len = -i
            else:
                self._right_len = right + 1

    def _index_check(self, index):
        if index >= 0:
            if index >= self.right_len or not self._right_list[index][1]:
                return False
            else:
                return self._right_list[index][1]
        else:
            index = -1 - index
            if index >= self.left_len or not self._left_list[index][1]:
                return False
            else:
                return self._left_list[index][1]

    def __getitem__(self, item):
        if type(item) is slice:
            item = _CL_slice_check(item)
            if item[2] is None:
                item[2] = 1
            left = self.left_len
            right = self.right_len
            if item[2] > 0:
                if item[0] is None:
                    item[0] = -(left - left % item[2])
                else:
                    item[0] = max(item[0], -(left - (left + item[0]) % item[2]))
                if item[1] is None:
                    item[1] = right
                else:
                    item[1] = min(item[1], right)
            else:
                if item[0] is None:
                    item[0] = -((1 - right) - (1 - right) % item[2])
                else:
                    item[0] = min(item[0], -((1 - right) - (1 - right + item[0]) % item[2]))
                if item[1] is None:
                    item[1] = -left - 1
                else:
                    item[1] = max(item[1], -left - 1)

            New = DynamicCoordList()
            New._right_list = [[None, False] for _ in range(self.right_len)]
            New._left_list = [[None, False] for _ in range(self.left_len)]
            New._left_len = self._left_len
            New._right_len = self._right_len

            for i in range(*item):
                if self._index_check(i):
                    New[i] = self[i]

            New._optimise()
            return New

        elif type(item) is int:
            index = item
            if index >= 0:
                if index >= self.right_len or not self._right_list[index][1]:
                    raise IndexError('DynamicCoordList index out of range')
                else:
                    return self._right_list[index][0]
            else:
                index = -1 - index
                if index >= self.left_len or not self._left_list[index][1]:
                    raise IndexError('DynamicCoordList index out of range')
                else:
                    return self._left_list[index][0]
        else:
            raise TypeError('CoordList indices must be integers or slices, not ' + type(item).__name__)

    def __setitem__(self, item, value):
        if type(item) is slice:
            item = _CL_slice_check(item)
            if item[2] is None:
                item[2] = 1
            if type(value) == DynamicCoordList:
                left = max(self.left_len, value.left_len)
                right = max(self.right_len, value.right_len)
                if item[2] > 0:
                    if item[0] is None:
                        item[0] = -(left - left % item[2])
                    else:
                        item[0] = max(item[0], -(left - (left + item[0]) % item[2]))
                    if item[1] is None:
                        item[1] = right
                    else:
                        item[1] = min(item[1], right)
                else:
                    if item[0] is None:
                        item[0] = -((1 - right) - (1 - right) % item[2])
                    else:
                        item[0] = min(item[0], -((1 - right) - (1 - right + item[0]) % item[2]))
                    if item[1] is None:
                        item[1] = -left - 1
                    else:
                        item[1] = max(item[1], -left - 1)

                for i in range(item[0], item[1], item[2]):
                    try:
                        self[i] = value[i]
                    except IndexError:
                        if self._index_check(i):
                            del self[i]
            else:
                if hasattr(value, '__getitem__'):
                    for i in range(item[0], item[1], item[2]):
                        try:
                            self[i] = value[i]
                        except IndexError:
                            if self._index_check(i):
                                del self[i]
                elif hasattr(value, '__iter__'):
                    value = iter(value)
                    new_value = []
                    for i in range(-((item[0] - item[1]) // item[2])):
                        try:
                            new_value.append(next(value))
                        except StopIteration:
                            raise ValueError('attempt to assign sequence of size ' +
                                             str(-((item[0] - item[1]) // item[2])) +
                                             ' to extended slice of size ' + str(i))
                    value = new_value
                    for i, j in zip(range(item[0], item[1], item[2]), range((item[1] - item[0]) // item[2])):
                        self[i] = value[j]
                else:
                    raise TypeError('can only assign an iterable')
        elif type(item) is int:
            index = item
            if index >= 0:
                if index >= len(self._right_list):
                    self._right_list += [[None, False] for _ in range(index - len(self._right_list))] + [[value, True]]
                    self._right_len = len(self._right_list)
                else:
                    self._right_list[index][0] = value
                    self._right_list[index][1] = True
            else:
                index = -1 - index
                if index >= len(self._left_list):
                    self._left_list += [[None, False] for _ in range(index - len(self._left_list))] + [[value, True]]
                    self._left_len = len(self._left_list)
                else:
                    self._left_list[index][0] = value
                    self._left_list[index][1] = True
            self._optimise()
        else:
            raise TypeError('CoordList indices must be integers or slices, not ' + type(item).__name__)

    def __delitem__(self, item):
        if type(item) is slice:  # TODO: Оптимизировать количество использований ._optimise()
            item = _CL_slice_check(item)
            if item[2] is None:
                item[2] = 1
            left = self.left_len
            right = self.right_len
            if item[2] > 0:
                if item[0] is None:
                    item[0] = -(left - left % item[2])
                else:
                    item[0] = max(item[0], -(left - (left + item[0]) % item[2]))
                if item[1] is None:
                    item[1] = right
                else:
                    item[1] = min(item[1], right)
            else:
                if item[0] is None:
                    item[0] = -((1 - right) - (1 - right) % item[2])
                else:
                    item[0] = min(item[0], -((1 - right) - (1 - right + item[0]) % item[2]))
                if item[1] is None:
                    item[1] = -left - 1
                else:
                    item[1] = max(item[1], -left - 1)

            for i in range(item[0], item[1], item[2]):
                if self._index_check(i):
                    del self[i]

        elif type(item) is int:
            index = item
            if index >= 0:
                if index >= len(self._right_list) or not self._right_list[index][1]:
                    raise IndexError('DynamicCoordList index out of range')
                else:
                    self._right_list[index][0] = None
                    self._right_list[index][1] = False
            else:
                index = -1 - index
                if index >= len(self._left_list) or not self._left_list[index][1]:
                    raise IndexError('DynamicCoordList index out of range')
                else:
                    self._left_list[index][0] = None
                    self._left_list[index][1] = False
            self._optimise()

        else:
            raise TypeError('CoordList indices must be integers or slices, not ' + type(item).__name__)

    # def __eq__(self, other):  # TODO: Написать "=", "!="
    #     pass
    #
    # def __ne__(self, other):
    #     pass

    def shift(self, shift):
        if shift >= 0:
            self._right_list = [[None, False] for _ in range(shift - len(self._left_list))] +\
                               list(reversed(self._left_list[:shift])) +\
                               self._right_list
            self._left_list = self._left_list[shift:]
        else:
            self._left_list = [[None, False] for _ in range(-shift - len(self._right_list))] +\
                               list(reversed(self._right_list[:-shift])) +\
                               self._left_list
            self._right_list = self._right_list[-shift:]
        self._left_len -= shift
        self._right_len += shift
        self._optimise()

    def shifted(self, shift):
        New = copy(self)
        New.shift(shift)
        return New

    def _cash(self):
        return list(map(lambda pair: pair[0], filter(lambda pair: pair[1], list(reversed(self._left_list)) +
                                                     self._right_list)))

    def __iter__(self):
        return map(lambda pair: pair[0], filter(lambda pair: pair[1], list(reversed(self._left_list))
                                                + self._right_list))

    def __bool__(self):
        return bool(len(self))

    def __str__(self):
        if self._str_in_proc:
            return '<SELF>'
        else:
            self._str_in_proc = True

            if self.left_len < -2:
                result = '[; <EMPTY>, ...(✕' + str(-self.left_len - 2) + '), <EMPTY>, ' +\
                       ', '.join(map(lambda pair: repr(pair[0]) if pair[1] else '<EMPTY>',
                                     self._right_list[-self.left_len: self.right_len])) + ']'
            elif self.right_len < -2:
                result = '[' + ', '.join(map(lambda pair: repr(pair[0]) if pair[1] else '<EMPTY>',
                                           self._left_list[-self.left_len: self.right_len: -1])) +\
                       '<EMPTY>, ...(X' + str(-self.right_len - 2) + ', <EMPTY>, ' + ']'
            else:
                result = '[' + ', '.join(map(lambda pair: repr(pair[0]) if pair[1] else '<EMPTY>',
                                           list(reversed(self._left_list)))) +\
                       '; ' + ', '.join(map(lambda pair: repr(pair[0]) if pair[1] else '<EMPTY>',
                                            self._right_list)) + ']'

            self._str_in_proc = False
            return result

    def __repr__(self):
        if self._str_in_proc:
            return '<SELF>'
        else:
            return 'DynamicCoordList(' + str(self) + ')'

    def __copy__(self):
        New = DynamicCoordList()
        New._right_list = self._right_list[:]
        New._left_list = self._left_list[:]
        New._right_len = self._right_len
        New._left_len = self._left_len
        return New

    def __deepcopy__(self, memodict={}):
        if id(self) in memodict:
            return memodict[id(self)]

        memodict[id(self)] = DynamicCoordList()
        memodict[id(self)]._right_list = deepcopy(self._right_list, memodict)
        memodict[id(self)]._left_list = deepcopy(self._left_list, memodict)
        memodict[id(self)]._right_len = self._right_len
        memodict[id(self)]._left_len = self._left_len
        return memodict[id(self)]
