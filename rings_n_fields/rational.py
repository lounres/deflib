import copy
from deflib.common_functions import get_name_of_class
from deflib.exceptions import LogicError
from deflib.combinatorial import gcd


# Class of rational numbers
class Rational:
    def __init__(self, *args, to_bring=True):
        if len(args) == 0:
            numerator = 0
            denominator = 1
        elif len(args) == 1:
            if type(args[0]) == str:
                string = args[0].split('/')
                if len(string) == 1:
                    try:
                        numerator = int(string[0])
                    except ValueError:
                        raise ValueError('invalid literal for Rational(): ' + str(args[0]))
                    denominator = 1
                    to_bring = False
                elif len(string) == 2:
                    try:
                        numerator = int(string[0])
                        denominator = int(string[1])
                    except ValueError:
                        raise ValueError('invalid literal for Rational(): ' + str(args[0]))
                else:
                    raise ValueError('invalid literal for Rational(): ' + str(args[0]))
            elif type(args[0]) == int:
                numerator = args[0]
                denominator = 1
                to_bring = False
            elif type(args[0]) == Rational:
                numerator = args[0].numerator
                denominator = args[0].denominator
                to_bring = False
            else:
                raise ValueError('invalid literal for Rational(): ' + str(args[0]))
        elif len(args) == 2:
            if type(args[0]) != int or type(args[1]) != int:
                raise ValueError('invalid literal for Rational(): ' + str(args))
            else:
                numerator = args[0]
                denominator = args[1]
                if denominator == 0:
                    raise LogicError("doesn't exist Rationalional fraction with zero denominator")
        else:
            raise ValueError('rat() takes at most 2 arguments (' + str(len(args)) + ' given)')
        self.numerator = numerator
        self.denominator = denominator
        if to_bring:
            self.bring()

    def __str__(self):
        return str(self.numerator) + '/' + str(self.denominator) if self.denominator != 1 else str(self.numerator)

    def __repr__(self):
        return "rat('" + str(self) + "')"

    def __lt__(self, other):
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            raise TypeError("'<' not supported between instances of 'rat' and '" + get_name_of_class(type(other)) + "'")
        return self.numerator * copied_other.denominator < self.denominator * copied_other.numerator

    def __le__(self, other):
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            raise TypeError("'<=' not supported between instances of 'rat' and '"
                            + get_name_of_class(type(other)) + "'")
        return self.numerator * copied_other.denominator <= self.denominator * copied_other.numerator

    def __eq__(self, other):
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            return False
        return self.numerator * copied_other.denominator == self.denominator * copied_other.numerator

    def __ne__(self, other):
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            return True
        return self.numerator * copied_other.denominator != self.denominator * copied_other.numerator

    def __gt__(self, other):
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            raise TypeError("'>' not supported between instances of 'rat' and '" + get_name_of_class(type(other)) + "'")
        return self.numerator * copied_other.denominator > self.denominator * copied_other.numerator

    def __ge__(self, other):
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            raise TypeError("'>=' not supported between instances of 'rat' and '"
                            + get_name_of_class(type(other)) + "'")
        return self.numerator * copied_other.denominator >= self.denominator * copied_other.numerator

    def __bool__(self):
        return self.numerator != 0

    def __add__(self, other):
        copied_self = copy.copy(self)
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__radd__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for +: 'rat' and '" + get_name_of_class(type(other)) + "'")
        copied_self.numerator = self.numerator * copied_other.denominator + self.denominator * copied_other.numerator
        copied_self.denominator *= copied_other.denominator
        copied_self.bring()
        return copied_self

    def __sub__(self, other):
        copied_self = copy.copy(self)
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rsub__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for -: 'rat' and '" + get_name_of_class(type(other)) + "'")
        copied_self.numerator = self.numerator * copied_other.denominator - self.denominator * copied_other.numerator
        copied_self.denominator *= copied_other.denominator
        copied_self.bring()
        return copied_self

    def __mul__(self, other):
        copied_self = copy.copy(self)
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rmul__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for *: 'rat' and '" + get_name_of_class(type(other)) + "'")
        copied_self.numerator *= copied_other.numerator
        copied_self.denominator *= copied_other.denominator
        copied_self.bring()
        return copied_self

    def __truediv__(self, other):
        copied_self = copy.copy(self)
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rtruediv__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for /: 'rat' and '" + get_name_of_class(type(other)) + "'")
        if copied_other == 0:
            raise ZeroDivisionError('division by zero')
        copied_self.numerator *= copied_other.denominator
        copied_self.denominator *= copied_other.numerator
        copied_self.bring()
        return copied_self

    def __pow__(self, power, modulo=None):
        if type(power) == int and power < 0 and self == 0:
            raise ZeroDivisionError('0 cannot be raised to a negative power')
        return (Rational(self.numerator ** power, self.denominator ** power, to_bring=False) if power >= 0 else
                Rational(self.denominator ** -power, self.numerator ** -power, to_bring=False))\
            if type(power) == int else pow(float(self), power, modulo)

    def __radd__(self, other):
        copied_self = copy.copy(self)
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            raise TypeError("unsupported operand type(s) for +: '" + get_name_of_class(type(other)) + "' and 'rat'")
        copied_self.numerator = self.numerator * copied_other.denominator + self.denominator * copied_other.numerator
        copied_self.denominator *= copied_other.denominator
        copied_self.bring()
        return copied_self

    def __rsub__(self, other):
        copied_self = copy.copy(self)
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            raise TypeError("unsupported operand type(s) for -: '" + get_name_of_class(type(other)) + "' and 'rat'")
        copied_self.numerator = self.denominator * copied_other.numerator - self.numerator * copied_other.denominator
        copied_self.denominator *= copied_other.denominator
        copied_self.bring()
        return copied_self

    def __rmul__(self, other):
        copied_self = copy.copy(self)
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            raise TypeError("unsupported operand type(s) for *: '" + get_name_of_class(type(other)) + "' and 'rat'")
        copied_self.numerator *= copied_other.numerator
        copied_self.denominator *= copied_other.denominator
        copied_self.bring()
        return copied_self

    def __rtruediv__(self, other):
        copied_self = copy.copy(self)
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            raise TypeError("unsupported operand type(s) for /: '" + get_name_of_class(type(other)) + "' and 'rat'")
        copied_other.numerator *= copied_self.denominator
        copied_other.denominator *= copied_self.numerator
        copied_other.bring()
        return copied_other

    def __iadd__(self, other):
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__radd__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for +: 'rat' and '" + get_name_of_class(type(other)) + "'")
        self.numerator = self.numerator * copied_other.denominator + self.denominator * copied_other.numerator
        self.denominator *= copied_other.denominator
        self.bring()
        return self

    def __isub__(self, other):
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rsub__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for -: 'rat' and '" + get_name_of_class(type(other)) + "'")
        self.numerator = self.numerator * copied_other.denominator - self.denominator * copied_other.numerator
        self.denominator *= copied_other.denominator
        self.bring()
        return self

    def __imul__(self, other):
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rmul__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for *: 'rat' and '" + get_name_of_class(type(other)) + "'")
        self.numerator *= copied_other.numerator
        self.denominator *= copied_other.denominator
        self.bring()
        return self

    def __itruediv__(self, other):
        if type(other) == int:
            copied_other = Rational(other)
        elif type(other) == Rational:
            copied_other = copy.copy(other)
        else:
            try:
                return type(other).__rtruediv__(other, self)
            except:
                raise TypeError("unsupported operand type(s) for /: 'rat' and '" + get_name_of_class(type(other)) + "'")
        if copied_other == 0:
            raise ZeroDivisionError('division by zero')
        self.numerator *= copied_other.denominator
        self.denominator *= copied_other.numerator
        self.bring()
        return self

    def __ipow__(self, power, modulo=None):
        self = self.__pow__(power, modulo)
        return self

    def __neg__(self):
        return Rational(-self.numerator, self.denominator, to_bring=False)

    def __pos__(self):
        return Rational(self.numerator, self.denominator, to_bring=False)

    def __abs__(self):
        return Rational(abs(self.numerator), self.denominator, to_bring=False)

    def __complex__(self):
        return complex(float(self))

    def __int__(self):
        return self.numerator // self.denominator

    def __float__(self):
        return self.numerator / self.denominator

    # def __round__(self, n = None):
    #     return round(float(self), n)

    # def __index__(self):
    #     float_copy = float(self)
    #     float_copy.index()
    #     return float_copy

    def __copy__(self):
        return Rational(self.numerator, self.denominator, to_bring=False)

    def __deepcopy__(self, memodict={}):
        return Rational(self.numerator, self.denominator, to_bring=False)

    def bring(self):
        gcd_to_divide = gcd(self.numerator, self.denominator)
        self.numerator //= gcd_to_divide
        self.denominator //= gcd_to_divide
        if self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1
