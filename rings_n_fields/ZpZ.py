import copy
from ..number_theory import primality


# Class for the field Z/pZ
class ZpZ:
    def __init__(self, num, module):
        if type(module) != int or type(num) != int or not primality(module):
            raise ValueError('invalid literal for ZpZ: ' + str(num) + ' ' + str(module))
        self.module = module
        self.number = num % module

    def __eq__(self, other):
        if type(other) != ZpZ:
            return False
        return self.number == other.number and self.module == other.module

    def __ne__(self, other):
        if type(other) != ZpZ:
            return True
        return self.number != other.number or self.module != other.module

    def __bool__(self):
        return self.number != 0

    def __add__(self, other):
        copied_self = copy.copy(self)
        if type(other) != ZpZ:
            raise TypeError("unsupported operand type(s) for +: 'ZpZ' and '" + type(other).__name__ + "'")
        elif self.module != other.module:
            raise TypeError('unsupported module of Z/pZ for +')
        copied_self.number += other.number
        copied_self.number %= copied_self.module
        return copied_self

    def __sub__(self, other):
        copied_self = copy.copy(self)
        if type(other) != ZpZ:
            raise TypeError("unsupported operand type(s) for -: 'ZpZ' and '" + type(other).__name__ + "'")
        elif self.module != other.module:
            raise TypeError('unsupported module of Z/pZ for -')
        copied_self.numerator -= other.number
        copied_self.number %= copied_self.module
        return copied_self

    def __mul__(self, other):
        copied_self = copy.copy(self)
        if type(other) != ZpZ:
            raise TypeError("unsupported operand type(s) for *: 'ZpZ' and '" + type(other).__name__ + "'")
        elif self.module != other.module:
            raise TypeError('unsupported module of Z/pZ for *')
        copied_self.number *= other.number
        copied_self.number %= copied_self.module
        return copied_self

    def __truediv__(self, other):
        copied_self = copy.copy(self)
        if type(other) != ZpZ:
            raise TypeError("unsupported operand type(s) for /: 'ZpZ' and '" + type(other).__name__ + "'")
        elif self.module != other.module:
            raise TypeError('unsupported module of Z/pZ for /')
        if other.number == 0:
            raise ZeroDivisionError('division by zero')
        while copied_self.number % other.number:
            copied_self.number += copied_self.module
        copied_self.number //= other.number
        return copied_self

    def __pow__(self, power, modulo = None):
        if type(power) != int or modulo != None:
            raise TypeError("unsupported operand type(s) for ** or pow(): 'ZpZ'" + (" and '" + type(power).__name__ + "'" if modulo == None else ", '" + type(power).__name__ + "', '" + type(modulo).__name__ + "'"))
        if power == 0:
            return ZpZ(1, self.module)
        ans = (self * self) ** (abs(power) // 2)
        if power % 2:
            ans *= self
        return ans if power > 0 else 1 / ans

    def __radd__(self, other):
        if type(other) != ZpZ:
            raise TypeError("unsupported operand type(s) for +: '" + type(other).__name__ + "' and 'ZpZ'")
        elif self.module != other.module:
            raise TypeError('unsupported module of Z/pZ for +')
        copied_other = copy.copy(other)
        copied_other.number += self.number
        copied_other.number %= copied_other.module
        return copied_other

    def __rsub__(self, other):
        if type(other) != ZpZ:
            raise TypeError("unsupported operand type(s) for -: '" + type(other).__name__ + "' and 'ZpZ'")
        elif self.module != other.module:
            raise TypeError('unsupported module of Z/pZ for -')
        copied_other = copy.copy(other)
        copied_other.number -= self.number
        copied_other.number %= copied_other.module
        return copied_other

    def __rmul__(self, other):
        if type(other) != ZpZ:
            raise TypeError("unsupported operand type(s) for *: '" + type(other).__name__ + "' and 'ZpZ'")
        elif self.module != other.module:
            raise TypeError('unsupported module of Z/pZ for *')
        copied_other = copy.copy(other)
        copied_other.number *= self.number
        copied_other.number %= copied_other.module
        return copied_other

    def __rtruediv__(self, other):
        if type(other) != ZpZ:
            raise TypeError("unsupported operand type(s) for /: '" + type(other).__name__ + "' and 'ZpZ'")
        elif self.module != other.module:
            raise TypeError('unsupported module of Z/pZ for /')
        if self.number == 0:
            raise ZeroDivisionError('division by zero')
        copied_other = copy.copy(other)
        while copied_other.number % self.number:
            copied_other.number += copied_other.module
        copied_other.number //= other.number
        return copied_other

    def __iadd__(self, other):
        if type(other) != ZpZ:
            raise TypeError("unsupported operand type(s) for +: 'ZpZ' and '" + type(other).__name__ + "'")
        elif self.module != other.module:
            raise TypeError('unsupported module of Z/pZ for +')
        self.number += other.number
        self.number %= self.module
        return self

    def __isub__(self, other):
        if type(other) != ZpZ:
            raise TypeError("unsupported operand type(s) for -: 'ZpZ' and '" + type(other).__name__ + "'")
        elif self.module != other.module:
            raise TypeError('unsupported module of Z/pZ for -')
        self.number -= other.number
        self.number %= self.module
        return self

    def __imul__(self, other):
        if type(other) != ZpZ:
            raise TypeError("unsupported operand type(s) for *: 'ZpZ' and '" + type(other).__name__ + "'")
        elif self.module != other.module:
            raise TypeError('unsupported module of Z/pZ for *')
        self.number *= other.number
        self.number %= self.module
        return self

    def __itruediv__(self, other):
        if type(other) != ZpZ:
            raise TypeError("unsupported operand type(s) for /: 'ZpZ' and '" + type(other).__name__ + "'")
        elif self.module != other.module:
            raise TypeError('unsupported module of Z/pZ for /')
        if other.number == 0:
            raise ZeroDivisionError('division by zero')
        while self.number % other.number:
            self.number += self.module
        self.number //= other.number
        return self

    def __ipow__(self, power, modulo = None):
        return pow(self, power, modulo)

    def __neg__(self):
        return ZpZ(-self.number, self.module)

    def __pos__(self):
        return ZpZ(self.number, self.module)

    def __int__(self):
        return self.number

    def __copy__(self):
        return ZpZ(self.number, self.module)

    def __deepcopy__(self, memodict={}):
        return ZpZ(self.number, self.module)