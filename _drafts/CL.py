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


# Class of list with any segment of indexes
class CoordList:
    def __init__(self, iterative, start=0):
        iterative = list(iterative)
        self._correction = -start
        self._list = iterative

    @property
    def correction(self):
        return self._correction

    def __len__(self):
        return len(self._list)

    @property
    def start(self):
        return self.correction

    @property
    def end(self):
        return len(self) + self.correction - 1

    @property
    def stop(self):
        return len(self) + self.correction

    def __getitem__(self, item):
        if type(item) is slice:
            item = _CL_slice_check(item)
            if item.step is None:
                item.step = 1
            if item.step > 0:
                if item.start is None:
                    item.start = 0
                else:
                    item.start += self.correction
                    item.start = max(item.start, item.start % item.step)
                if item.stop is None:
                    item.stop = len(self)
                else:
                    item.stop = min(item.stop + self.correction, len(self))
            else:
                if item.start is None:
                    item.start = len(self)
                else:
                    item.start += self.correction
                    item.start = min(item.start, len(self) - 1 + (item.start - len(self) + 1) % item.step)
                if item.stop is None:
                    item.stop = 0
                else:
                    item.stop = max(item.stop + self.correction, -1)

            return self._list[item]
        elif type(item) is int:
            index = item
            if not 0 <= index + self.correction < len(self):
                raise IndexError('CoordList index out of range')
            else:
                return self._list[index + self.correction]
        else:
            raise TypeError('CoordList indices must be integers or slices, not ' + type(item).__name__)

    def __setitem__(self, item, value):
        if type(item) is slice:
            item = _CL_slice_check(item)
            if item.step is None:
                item.step = 1
            if item.step > 0:
                if item.start is None:
                    item.start = 0
                else:
                    item.start += self.correction
                    item.start = max(item.start, item.start % item.step)
                if item.stop is None:
                    item.stop = len(self)
                else:
                    item.stop = min(item.stop + self.correction, len(self))
            else:
                if item.start is None:
                    item.start = len(self)
                else:
                    item.start += self.correction
                    item.start = min(item.start, len(self) - 1 + (item.start - len(self) + 1) % item.step)
                if item.stop is None:
                    item.stop = 0
                else:
                    item.stop = max(item.stop + self.correction, -1)

            if not hasattr(value, '__iter__'):
                    raise TypeError('can only assign an iterable')
            else:
                value = tuple(iter(value))

            if len(value) != -((item.start - item.stop) // item.step):
                raise ValueError('attempt to assign sequence of size ' +
                                 str(-((item.start - item.stop) // item.step)) +
                                 ' to extended slice of size ' +
                                 str(len(value)))
            else:
                self._list[item] = value

        elif type(item) is int:
            index = item
            if not 0 <= index + self.correction < len(self):
                raise IndexError('CoordList index out of range')
            else:
                self._list[index + self.correction] = value
        else:
            raise TypeError('CoordList indices must be integers or slices, not ' + type(item).__name__)

    def __delitem__(self, item):
        if type(item) is slice:
            item = _CL_slice_check(item)
            if item.step is None:
                item.step = 1
            if item.step > 0:
                if item.start is None:
                    item.start = 0
                else:
                    item.start += self.correction
                    item.start = max(item.start, item.start % item.step)
                if item.stop is None:
                    item.stop = len(self)
                else:
                    item.stop = min(item.stop + self.correction, len(self))
            else:
                if item.start is None:
                    item.start = len(self)
                else:
                    item.start += self.correction
                    item.start = min(item.start, len(self) - 1 + (item.start - len(self) + 1) % item.step)
                if item.stop is None:
                    item.stop = 0
                else:
                    item.stop = max(item.stop + self.correction, -1)

            self._list[item] = [None] * -((item.start - item.stop) // item.step)

        elif type(item) is int:
            index = item
            if not 0 <= index + self.correction < len(self):
                raise IndexError('CoordList index out of range')
            else:
                self._list[index + self.correction] = None
        else:
            raise TypeError('CoordList indices must be integers or slices, not ' + type(item).__name__)

    def __iter__(self):
        return iter(self._list)

    def __reversed__(self):
        return CoordList(reversed(self._list), start=-self.correction)

    def __contains__(self, item):
        return item in self._list

    def __bool__(self):
        return any(self._list)

    def __copy__(self):
        return CoordList(copy(self._list), start=-self.correction)

    def __deepcopy__(self, memodict={}):
        if id(self) in memodict:
            return memodict[id(self)]

        memodict[id(self)] = CoordList([], start=-self.correction)
        memodict[id(self)]._list = deepcopy(self._list, memodict)
        return memodict[id(self)]

    def __repr__(self):
        return 'CoordList(' + repr(self._list) + ', ' + 'start=' + str(-self.correction) + ')'

    def __str__(self):
        return 'CoordList(' + repr(self._list) + ', ' + 'start=' + str(-self.correction) + ')'
