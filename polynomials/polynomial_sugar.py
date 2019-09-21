import functools
from ..exceptions import LogicError
from .polynomial import Polynomial


# GCD for polynomials
def polynomial_gcd(*nums):
    def polynomial_bin_gcd(P, Q):
        if Q == Polynomial(field=Q.field):
            return P
        return polynomial_bin_gcd(Q, P % Q)

    result = functools.reduce(polynomial_bin_gcd, nums)
    result.bring()
    return result


# Reflexive polynomial for given polynomial
def reflexive_polynomial(P):
    if type(P) != Polynomial:
        raise ValueError('invalid literal for reflexive_Polynomial()')
    return Polynomial(*P.coefficients, reverse=True, field=P.field)


# Lagrange's interpolation polynomial
def interpolation_polynomial(*args, field=None):
    if len(args) == 0:
        raise ValueError('interpolation_Polynomial() must have at least one arguments')
    if len(args) == 1:
        from_x_to_y = args[0]
        x = list(from_x_to_y.keys())[0]
        if type(from_x_to_y) != dict or not from_x_to_y:
            raise ValueError('invalid literal for interpolation_Polynomial: ' + str(args[0]))
        X = list(from_x_to_y.keys())
        Y = list(from_x_to_y.values())
    elif len(args) == 2:
        try:
            X = list(args[0])
            Y = list(args[1])
        except:
            raise ValueError('invalid literal for interpolation_Polynomial: ' + ', '.join(list(map(str, args))))
        if len(X) != len(Y):
            raise LogicError('invalid literal for interpolation_Polynomial: ' + ', '.join(list(map(str, args))))
        if len(X) == 0:
            raise ValueError('invalid literal for interpolation_Polynomial: ' + ', '.join(list(map(str, args))))
        x = X[0]
    else:
        raise ValueError('interpolation_Polynomial() takes at most 2 arguments (' + str(len(args)) + ' given)')
    if type(field) not in [type, type(None)]:
        raise ValueError('invalid literal for interpolation_Polynomial: ' + ', '.join(args + ()))
    if field is not None:
        try:
            X = list(map(field, X))
            Y = list(map(field, Y))
        except:
            raise ValueError("can't convert arguments or values of Polynomial by the field")
    else:
        x = X[0]
        if not all([type(t) == type(x) for t in X + Y]):
            raise LogicError('all arguments and values of Polynomial should be elments of a single field')
        field = type(x)
    return sum([Y[i] * functools.reduce(lambda P, Q: P * Q, [(Polynomial(-X[j], 1, field=field)) // Polynomial(X[i] - X[j], field=field) for j in list(range(i)) + list(range(i + 1, len(X)))]) for i in range(len(X))])


# It's like an 'exec' for polynomials TODO: Переписать exec для многочленов
def compile_polynomial(string, field=float):
    if type(string) != str or type(field) != type:
        raise TypeError('invalid literals for compile_Polynomial: ' + repr(string) + ', ' + repr(field))

    def compile_it(arr):
        for i in range(len(arr)):
            if type(arr[i]) == list:
                arr[i] = str(compile_it(arr[i]))

        try:
            return Polynomial(''.join(arr), field=field)
        except:
            raise ValueError('invalid string for compile_Polynomial: ' + repr(string))

    STR = []
    Brackets = []
    last_end = -1
    i = 0
    while i < len(string):
        if string[i] == '(':
            if not Brackets:
                STR.append(string[last_end + 1: i])
                x = list()
                STR.append(x)
                Brackets.append(x)
            else:
                Brackets[-1].append(string[last_end + 1: i])
                x = list()
                Brackets[-1].append(x)
                Brackets.append(x)
            last_end = i
        elif string[i] == ')':
            if not Brackets:
                raise ValueError('invalid string for compile_Polynomial: ' + repr(string))
            else:
                Brackets[-1].append(string[last_end + 1: i])
                Brackets.pop()
                last_end = i
        i += 1
    if Brackets:
        raise ValueError('invalid string for compile_Polynomial: ' + repr(string))
    STR.append(string[last_end + 1: i])
    return compile_it(STR)


def NewPolynomial(field):
    return functools.partial(Polynomial, field=field)
