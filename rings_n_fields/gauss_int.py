import copy
from deflib.common_functions import get_name_of_class


# Class of Gauss's integers
class GaussInt:
    def __init__(self, *args):
        if len(args) == 0:
            real = 0
            imaginary = 0
        elif len(args) == 1:
            if type(args[0]) == str:
                if len(args[0]) == 0 or args[0][0] == '+':
                    raise ValueError('invalid literal for GaussInt(): ' + str(args[0]))
                string = '+-'.join(args[0].split('-')).split('+')
                if string[0] == '':
                    string = string[1:]
                if not 1 <= len(string) <= 2:
                    raise ValueError('invalid literal for GaussInt(): ' + str(args[0]))
                try:
                    last_char = string[-1][-1]
                except IndexError:
                    raise ValueError('invalid literal for GaussInt(): ' + str(args[0]))
                if not (last_char.isdecimal() or last_char == 'i'):
                    raise ValueError('invalid literal for GaussInt(): ' + str(args[0]))
                if len(string) == 1:
                    string = string[0]
                    if string[-1] == 'i':
                        real = 0
                        try:
                            imaginary = int(string[:-1])
                        except:
                            raise ValueError('invalid literal for GaussInt(): ' + str(args[0]))
                    else:
                        try:
                            real = int(string)
                        except:
                            raise ValueError('invalid literal for GaussInt(): ' + str(args[0]))
                        imaginary = 0
                else:
                    if string[1][-1] != 'i':
                        raise ValueError('invalid literal for GaussInt(): ' + str(args[0]))
                    try:
                        real = int(string[0])
                        imaginary = 1 if not string[1][:-1] else (-1 if not string[1][-2].isdecimal() else int(string[1][:-1]))
                    except:
                        raise ValueError('invalid literal for GaussInt(): ' + str(args[0]))
            elif type(args[0]) == int:
                real = args[0]
                imaginary = 0
            else:
                raise ValueError('invalid literal for GaussInt(): ' + str(args[0]))
        elif len(args) == 2:
            if type(args[0]) != int or type(args[1]) != int:
                raise ValueError('invalid literal for GaussInt(): ' + str(args[0]))
            else:
                real = args[0]
                imaginary = args[1]
        else:
            raise ValueError('GaussInt() takes at most 2 arguments (' + str(len(args)) + ' given)')
        self.real = real
        self.imaginary = imaginary

    def __str__(self):
        if not self.imaginary:
            return str(self.real)
        if not self.real:
            return  str(self.imaginary) + 'i'
        return str(self.real) + ('+' if self.imaginary > 0 else '-') + (str(abs(self.imaginary)) if abs(self.imaginary) != 1 else '') + 'i'

    def __repr__(self):
        return "GaussInt('" + str(self) + "')"

    def __eq__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            return False
        return (self.real, self.imaginary) == (copied_other.real, copied_other.imaginary)

    def __ne__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            return True
        return (self.real, self.imaginary) != (copied_other.real, copied_other.imaginary)

    def __bool__(self):
        return self.real or self.imaginary

    def __add__(self, other):
        copied_self = copy.copy(self)
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__radd__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for +: 'GaussInt' and '" + get_name_of_class(type(other)) + "'")
        copied_self.real += copied_other.real
        copied_self.imaginary += copied_other.imaginary
        return copied_self

    def __sub__(self, other):
        copied_self = copy.copy(self)
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rsub__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for -: 'GaussInt' and '" + get_name_of_class(type(other)) + "'")
        copied_self.real -= copied_other.real
        copied_self.imaginary -= copied_other.imaginary
        return copied_self

    def __mul__(self, other):
        copied_self = copy.copy(self)
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rmul__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for *: 'GaussInt' and '" + get_name_of_class(type(other)) + "'")
        copied_self.real = self.real * copied_other.real - self.imaginary * copied_other.imaginary
        copied_self.imaginary = self.real * copied_other.imaginary + self.imaginary * copied_other.real
        return copied_self

    def __floordiv__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rfloordiv__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for //: 'GaussInt' and '" + get_name_of_class(type(other)) + "'")
        if copied_other == 0:
            raise ZeroDivisionError('GaussInt division by zero')
        Norm = copied_other.norm()
        return GaussInt((2 * (copied_other.real * self.real + copied_other.imaginary * self.imaginary) + Norm) // (2 * Norm), (2 * (copied_other.real * self.imaginary - copied_other.imaginary * self.real) + Norm) // (2 * Norm))

    def __mod__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rmod__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for %: 'GaussInt' and '" + get_name_of_class(type(other)) + "'")
        if copied_other == 0:
            raise ZeroDivisionError('GaussInt division by zero')
        Norm = copied_other.norm()
        quotient = ((2 * (copied_other.real * self.real + copied_other.imaginary * self.imaginary) + Norm) // (2 * Norm), (2 * (copied_other.real * self.imaginary - copied_other.imaginary * self.real) + Norm) // (2 * Norm))
        return GaussInt(self.real - copied_other.real * quotient[0] + copied_other.imaginary * quotient[1], self.imaginary - copied_other.real * quotient[1] - copied_other.imaginary * quotient[0])

    def __pow__(self, power, modulo = None):
        if type(power) != int or power < 0:
            return pow(complex(self), power, modulo)
        if modulo != None:
            try:
                modulo = GaussInt(modulo)
            except:
                ValueError('invalid modulo for GaussInt(): ' + str(modulo))
        if modulo == 0:
            raise ZeroDivisionError('GaussInt modulo by zero')
        if power == 0:
            return GaussInt(1)
        next_step = GaussInt(self.real ** 2 - self.imaginary ** 2, 2 * self.real * self.imaginary)
        if modulo != None:
            next_step %= modulo
        ans = pow(next_step, power // 2, modulo)
        if power % 2:
            ans *= self
            if modulo != None:
                ans %= modulo
        return ans

    def __radd__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            raise TypeError("unsupported operand type(s) for +: '" + get_name_of_class(type(other)) + "' and 'GaussInt'")
        copied_other.real += self.real
        copied_other.imaginary += self.imaginary
        return copied_other

    def __rsub__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            raise TypeError("unsupported operand type(s) for -: '" + get_name_of_class(type(other)) + "' and 'GaussInt'")
        copied_other.real -= self.real
        copied_other.imaginary -= self.imaginary
        return self

    def __rmul__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            raise TypeError("unsupported operand type(s) for *: '" + get_name_of_class(type(other)) + "' and 'GaussInt'")
        copied_other.real = self.real * copied_other.real - self.imaginary * copied_other.imaginary
        copied_other.imaginary = self.real * copied_other.imaginary + self.imaginary * copied_other.real
        return copied_other

    def __rfloordiv__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            raise TypeError("unsupported operand type(s) for //: '" + get_name_of_class(type(other)) + "' and 'GaussInt'")
        if self == 0:
            raise ZeroDivisionError('GaussInt division by zero')
        Norm = self.norm()
        return GaussInt((2 * (copied_other.real * self.real + copied_other.imaginary * self.imaginary) + Norm) // (2 * Norm), (2 * (copied_other.imaginary * self.real - copied_other.real * self.imaginary) + Norm) // (2 * Norm))

    def __rmod__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            raise TypeError("unsupported operand type(s) for %: '" + get_name_of_class(type(other)) + "' and 'GaussInt'")
        if self == 0:
            raise ZeroDivisionError('GaussInt division by zero')
        Norm = self.norm()
        quotient = ((2 * (copied_other.real * self.real + copied_other.imaginary * self.imaginary) + Norm) // (2 * Norm), (2 * (copied_other.imaginary * self.real - copied_other.real * self.imaginary) + Norm) // (2 * Norm))
        return GaussInt(copied_other.real - self.real * quotient[0] + self.imaginary * quotient[1], copied_other.imaginary - self.real * quotient[1] - self.imaginary * quotient[0])

    def __iadd__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__radd__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for +: 'GaussInt' and '" + get_name_of_class(type(other)) + "'")
        self.real += copied_other.real
        self.imaginary += copied_other.imaginary
        return self

    def __isub__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rsub__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for -: 'GaussInt' and '" + get_name_of_class(type(other)) + "'")
        self.real -= copied_other.real
        self.imaginary -= copied_other.imaginary
        return self

    def __imul__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rmul__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for *: 'GaussInt' and '" + get_name_of_class(type(other)) + "'")
        self.real = self.real * copied_other.real - self.imaginary * copied_other.imaginary
        self.imaginary = self.real * copied_other.imaginary + self.imaginary * copied_other.real
        return self

    def __ifloordiv__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rfloordiv__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for //: 'GaussInt' and '" + get_name_of_class(type(other)) + "'")
        if copied_other == 0:
            raise ZeroDivisionError('GaussInt division by zero')
        Norm = copied_other.norm()
        return GaussInt((2 * (copied_other.real * self.real + copied_other.imaginary * self.imaginary) + Norm) // (2 * Norm), (2 * (copied_other.real * self.imaginary - copied_other.imaginary * self.real) + Norm) // (2 * Norm))

    def __imod__(self, other):
        if type(other) == int:
            copied_other = GaussInt(other)
        elif type(other) == GaussInt:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rmod__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for %: 'GaussInt' and '" + get_name_of_class(type(other)) + "'")
        if copied_other == 0:
            raise ZeroDivisionError('GaussInt division by zero')
        Norm = copied_other.norm()
        quotient = ((2 * (copied_other.real * self.real + copied_other.imaginary * self.imaginary) + Norm) // (2 * Norm), (2 * (copied_other.real * self.imaginary - copied_other.imaginary * self.real) + Norm) // (2 * Norm))
        return GaussInt(self.real - copied_other.real * quotient[0] + copied_other.imaginary * quotient[1], self.imaginary - copied_other.real * quotient[1] - copied_other.imaginary * quotient[0])

    def __ipow__(self, power, modulo = None):
        return pow(self, power, modulo)

    def __neg__(self):
        return GaussInt(-self.real, -self.imaginary)

    def __pos__(self):
        return GaussInt(self.real, self.imaginary)

    def __complex__(self):
        return eval(str(self.real) + '+' + str(self.imaginary) + 'j')

    def __int__(self):
        return self.real

    def __float__(self):
        return float(self.real)

    def __copy__(self):
        return GaussInt(self.real, self.imaginary)

    def __deepcopy__(self, memodict={}):
        return GaussInt(self.real, self.imaginary)

    def __abs__(self):
        return self.norm() ** 0.5

    def norm(self):
        return self.real ** 2 + self.imaginary ** 2

    def conjugate(self):
        return GaussInt(self.real, -self.imaginary)