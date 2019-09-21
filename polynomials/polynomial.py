import copy
import functools


# Class of polynomials over any needed field
class Polynomial:
    def __init__(self, *args, **kwargs):
        kwargs['reverse'] = kwargs.get('reverse', False)
        reverse = kwargs.pop('reverse')
        if set(kwargs.keys()) - {'field'}:
            raise TypeError("'" + (set(kwargs.keys()) - {'field'}).pop() +
                            "' is an invalid keyword argument for this function")
        self.field = kwargs.get('field', float)
        if type(self.field) != type:
            raise TypeError('field must be a class')
        if len(args) == 0:
            coefs = []
        elif len(args) == 1:
            if type(args[0]) == str:
                coefs = {}
                for monomial in ('+-'.join(''.join(args[0].split()).split('-'))).split('+')[int(args[0][0] == '-'):]:
                    monomial = monomial.split('^')
                    if '' in monomial:
                        raise ValueError("invalid literal for Polynomial(): '" + args[0] + "'")
                    if len(monomial) == 1:
                        if monomial[0][-1] == 'x':
                            try:
                                coefs[1] = coefs.get(1, 0) + self.field('1' if monomial[0] == 'x' else ('-1' if monomial[0] == '-x' else monomial[0][:-1]))
                            except:
                                raise ValueError("invalid literal for Polynomial(): '" + args[0] + "'")
                        else:
                            try:
                                coefs[0] = coefs.get(0, 0) + self.field(monomial[0])
                            except:
                                raise ValueError("invalid literal for Polynomial(): '" + args[0] + "'")
                    elif len(monomial) == 2:
                        if monomial[0][-1] != 'x':
                            raise ValueError("invalid literal for Polynomial(): '" + args[0] + "'")
                        try:
                            coefs[int(monomial[1])] = coefs.get(int(monomial[1]), 0) + self.field('1' if monomial[0] == 'x' else ('-1' if monomial[0] == '-x' else monomial[0][:-1]))
                        except:
                            raise ValueError("invalid literal for Polynomial(): '" + args[0] + "'")
                    else:
                        raise ValueError("invalid literal for Polynomial(): '" + args[0] + "'")
                coefs = [coefs.get(i, self.field(0)) for i in range(max(coefs.keys()) + 1)]
            else:
                try:
                    coefs = map(self.field, args)
                except:
                    raise ValueError('invalid literal for Polynomial(): ' + str(args[0]))
        else:
            try:
                coefs = list(map(self.field, args))
            except:
                raise ValueError('invalid literal for Polynomial(): ' + str(args))
            if reverse:
                coefs.reverse()
        self.coefficients = tuple(coefs)
        self.remove_zeroes()

    def __str__(self):
        if len(self.coefficients) == 0:
            return '0'
        ans = []
        if self.coefficients[0] != 0:
            ans += [str(self.coefficients[0])]
        if len(self.coefficients) > 1:
            if self.coefficients[1] != 0:
                c = '' if self.coefficients[1] == 1 else ('-' if self.coefficients[1] == -1 else str(self.coefficients[1]))
                ans += [c + 'x']
        for i in range(2, len(self.coefficients)):
            if self.coefficients[i] != 0:
                c = '' if self.coefficients[i] == 1 else ('-' if self.coefficients[i] == -1 else str(self.coefficients[i]))
                ans += [c + 'x^' + str(i)]
        return '-'.join(('+'.join(ans)).split('+-'))

    def __repr__(self):
        return 'Polynomial(' + str(self) + ')'

    def __eq__(self, other):
        if type(other) == self.field:
            copied_other = Polynomial(other, field = self.field)
        elif type(other) == Polynomial:
            if self.field != other.field:
                return False
            copied_other = copy.copy(other)
        else:
            return False
        return self.coefficients == copied_other.coefficients

    def __ne__(self, other):
        if type(other) == self.field:
            copied_other = Polynomial(other, field = self.field)
        elif type(other) == Polynomial:
            if self.field != other.field:
                return True
            copied_other = copy.copy(other)
        else:
            return True
        return self.coefficients != copied_other.coefficients

    def __bool__(self):
        return bool(self.coefficients)

    def __add__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for +")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for +: 'Polynomial' and '" + type(other).__name__ + "'")
        self_coefs = list(self.coefficients) + [self.field(0)] * (len(copied_other.coefficients) - len(self.coefficients))
        other_coefs = list(copied_other.coefficients) + [self.field(0)] * (len(self.coefficients) - len(copied_other.coefficients))
        copied_other.coefficients = tuple(self_coefs[i] + other_coefs[i] for i in range(len(self_coefs)))
        copied_other.remove_zeroes()
        return copied_other

    def __sub__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        self_coefs = list(self.coefficients) + [self.field(0)] * (len(copied_other.coefficients) - len(self.coefficients))
        other_coefs = list(copied_other.coefficients) + [self.field(0)] * (len(self.coefficients) - len(copied_other.coefficients))
        copied_other.coefficients = tuple(self_coefs[i] - other_coefs[i] for i in range(len(self_coefs)))
        copied_other.remove_zeroes()
        return copied_other

    def __mul__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        if self == Polynomial(field = self.field) or copied_other == Polynomial(field = self.field):
            return Polynomial(field = self.field)
        copied_other.coefficients = tuple(sum([self.coefficients[j] * copied_other.coefficients[i - j] for j in range(max(0, i - len(copied_other.coefficients) +  1), min(i, len(self.coefficients) - 1) + 1)]) for i in range(len(self.coefficients ) + len(copied_other.coefficients)))
        return copied_other

    def __floordiv__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        if copied_other == self.field(0):
            raise ZeroDivisionError('Polynomial division by zero')
        copied_self = copy.copy(self)
        copied_self.coefficients = list(copied_self.coefficients)
        quotient = [0] * (len(copied_self.coefficients) - len(copied_other.coefficients) + 1)
        Len_of_divider = len(copied_other.coefficients)
        for i in range(len(copied_self.coefficients) - len(copied_other.coefficients), -1, -1):
            coef = quotient[i] = copied_self.coefficients[i + Len_of_divider - 1] / copied_other.coefficients[-1]
            for j in range(Len_of_divider):
                copied_self.coefficients[i + j] -= copied_other.coefficients[j] * coef
        quotient = Polynomial(*quotient, field=self.field)
        return quotient

    def __mod__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        if copied_other == self.field(0):
            raise ZeroDivisionError('Polynomial division by zero')
        copied_self = copy.copy(self)
        copied_self.coefficients = list(copied_self.coefficients)
        Len_of_divider = len(copied_other.coefficients)
        for i in range(len(copied_self.coefficients) - len(copied_other.coefficients), -1, -1):
            coef = copied_self.coefficients[i + Len_of_divider - 1] / copied_other.coefficients[-1]
            for j in range(Len_of_divider):
                copied_self.coefficients[i + j] -= copied_other.coefficients[j] * coef
        copied_self.coefficients = tuple(copied_self.coefficients)
        copied_self.remove_zeroes()
        return copied_self

    def __pow__(self, power, modulo = None):
        if type(power) != int or power < 0:
            raise ValueError('invalid power for Polynomial(): ' + str(power))
        if modulo == 0:
            raise ZeroDivisionError('Polynomial modulo by zero')
        if power == 0:
            return Polynomial(1, field=self.field)
        next_step = self * self
        if modulo != None:
            next_step %= modulo
        ans = pow(next_step, power // 2, modulo)
        if power % 2:
            ans *= self
            if modulo != None:
                ans %= modulo
        return ans

    def __radd__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        self_coefs = list(self.coefficients) + [self.field(0)] * (len(copied_other.coefficients) - len(self.coefficients))
        other_coefs = list(copied_other.coefficients) + [self.field(0)] * (len(self.coefficients) - len(copied_other.coefficients))
        copied_other.coefficients = tuple(self_coefs[i] + other_coefs[i] for i in range(len(self_coefs)))
        copied_other.remove_zeroes()
        return copied_other

    def __rsub__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        self_coefs = list(self.coefficients) + [self.field(0)] * (len(copied_other.coefficients) - len(self.coefficients))
        other_coefs = list(copied_other.coefficients) + [self.field(0)] * (len(self.coefficients) - len(copied_other.coefficients))
        copied_other.coefficients = tuple(other_coefs[i] - self_coefs[i] for i in range(len(self_coefs)))
        copied_other.remove_zeroes()
        return copied_other

    def __rmul__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        if self == Polynomial(field = self.field) or copied_other == Polynomial(field = self.field):
            return Polynomial(field = self.field)
        copied_other.coefficients = tuple(sum([self.coefficients[j] * copied_other.coefficients[i - j] for j in range(max(0, i - len(copied_other.coefficients) +  1), min(i, len(self.coefficients) - 1) + 1)]) for i in range(len(self.coefficients ) + len(copied_other.coefficients)))
        return copied_other

    def __rfloordiv__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        if self == self.field(0):
            raise ZeroDivisionError('Polynomial division by zero')
        copied_other.coefficients = list(copied_other.coefficients)
        quotient = [0] * (len(copied_other.coefficients) - len(self.coefficients) + 1)
        Len_of_divider = len(self.coefficients)
        for i in range(len(copied_other.coefficients) - len(self.coefficients), -1, -1):
            coef = quotient[i] = copied_other.coefficients[i + Len_of_divider - 1] / self.coefficients[-1]
            for j in range(Len_of_divider):
                copied_other.coefficients[i + j] -= self.coefficients[j] * coef
        quotient = Polynomial(*quotient, field=self.field)
        return quotient

    def __rmod__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        if self == self.field(0):
            raise ZeroDivisionError('Polynomial division by zero')
        copied_other.coefficients = list(copied_other.coefficients)
        Len_of_divider = len(self.coefficients)
        for i in range(len(copied_other.coefficients) - len(self.coefficients), -1, -1):
            coef = copied_other.coefficients[i + Len_of_divider - 1] / self.coefficients[-1]
            for j in range(Len_of_divider):
                copied_other.coefficients[i + j] -= self.coefficients[j] * coef
        copied_other.coefficient = tuple(copied_other.coefficients)
        copied_other.remove_zeroes()
        return copied_other

    def __iadd__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        self_coefs = list(self.coefficients) + [self.field(0)] * (len(copied_other.coefficients) - len(self.coefficients))
        other_coefs = list(copied_other.coefficients) + [self.field(0)] * (len(self.coefficients) - len(copied_other.coefficients))
        copied_other.coefficients = tuple(self_coefs[i] + other_coefs[i] for i in range(len(self_coefs)))
        copied_other.remove_zeroes()
        return copied_other

    def __isub__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        self_coefs = list(self.coefficients) + [self.field(0)] * (len(copied_other.coefficients) - len(self.coefficients))
        other_coefs = list(copied_other.coefficients) + [self.field(0)] * (len(self.coefficients) - len(copied_other.coefficients))
        copied_other.coefficients = tuple(self_coefs[i] - other_coefs[i] for i in range(len(self_coefs)))
        copied_other.remove_zeroes()
        return copied_other

    def __imul__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        if self == Polynomial(field = self.field) or copied_other == Polynomial(field = self.field):
            return Polynomial(field = self.field)
        copied_other.coefficients = tuple(sum([self.coefficients[j] * copied_other.coefficients[i - j] for j in range(max(0, i - len(copied_other.coefficients) +  1), min(i, len(self.coefficients) - 1) + 1)]) for i in range(len(self.coefficients ) + len(copied_other.coefficients)))
        return copied_other

    def __ifloordiv__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        if copied_other == self.field(0):
            raise ZeroDivisionError('Polynomial division by zero')
        copied_self = copy.copy(self)
        copied_self.coefficients = list(copied_self.coefficients)
        quotient = [0] * (len(copied_self.coefficients) - len(copied_other.coefficients) + 1)
        Len_of_divider = len(copied_other.coefficients)
        for i in range(len(copied_self.coefficients) - len(copied_other.coefficients), -1, -1):
            coef = quotient[i] = copied_self.coefficients[i + Len_of_divider - 1] / copied_other.coefficients[-1]
            for j in range(Len_of_divider):
                copied_self.coefficients[i + j] -= copied_other.coefficients[j] * coef
        quotient = Polynomial(*quotient, field=self.field)
        return quotient

    def __imod__(self, other):
        if type(other) == Polynomial:
            if self.field != other.field:
                raise TypeError("unsupported field of Polynomials for -")
            copied_other = copy.copy(other)
        else:
            try:
                copied_other = Polynomial(self.field(other), field = self.field)
            except:
                raise TypeError("unsupported operand type(s) for -: 'Polynomial' and '" + type(other).__name__ + "'")
        if copied_other == self.field(0):
            raise ZeroDivisionError('Polynomial division by zero')
        copied_self = copy.copy(self)
        copied_self.coefficients = list(copied_self.coefficients)
        Len_of_divider = len(copied_other.coefficients)
        for i in range(len(copied_self.coefficients) - len(copied_other.coefficients), -1, -1):
            coef = copied_self.coefficients[i + Len_of_divider - 1] / copied_other.coefficients[-1]
            for j in range(Len_of_divider):
                copied_self.coefficients[i + j] -= copied_other.coefficients[j] * coef
        copied_self.coefficients = tuple(copied_self.coefficients)
        copied_self.remove_zeroes()
        return copied_self

    def __ipow__(self, power, modulo = None):
        return pow(self, power, modulo)

    def __neg__(self):
        return Polynomial(*map(lambda x: -x, self.coefficients), field = self.field)

    def __pos__(self):
        return Polynomial(*self.coefficients, field = self.field)

    def __copy__(self):
        return Polynomial(*self.coefficients, field = self.field)

    def __deepcopy__(self, memodict={}):
        return Polynomial(*self.coefficients, field = self.field)

    def __len__(self):
        return len(self.coefficients) - 1

    def __call__(self, arg):
        try:
            coefs = list(self.coefficients)
            coefs.reverse()
            return functools.reduce(lambda res, new: res * arg + new, coefs)
        except:
            raise ValueError('invalid argument for Polynomial()')

    def __getitem__(self, item):
        if item > len(self):
            return self.field(0)
        elif item >= -len(self.coefficients):
            return self.coefficients[item]
        else:
            return self.field(0)

    def remove_zeroes(self):
        end = 0
        for i in range(len(self.coefficients) - 1, -1, -1):
            if self.coefficients[i] != self.field(0):
                end = i + 1
                break
        self.coefficients = self.coefficients[:end]

    def bring(self):
        if len(self) != -1:
            self.coefficients = tuple(map(lambda coef: coef / self.coefficients[-1], self.coefficients))
