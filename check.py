from .exceptions import LogicError
from .combinatorial import binomial, gcd
from .rings_n_fields import Rational
from .k_degrees import B
from .number_theory import lagrange_sign

if __name__ == '__main__':
    print('LogicError', end = ' ')
    try:
        raise LogicError
    except LogicError:
        print('OK')

    print('Binomial coefficient', end = ' ')
    if binomial(2017, 5) != 276817455002088:
        raise ValueError
    print('OK')

    print('GCD', end = ' ')
    if gcd(2016, 256, 444) != 4:
        raise ValueError
    print('OK')

    print('Rational numbers', end = ' ')
    x = Rational(2016, 5) / Rational(36, 2015)
    if 8 / -x != Rational(-1, 2821, to_bring=False):
        raise ValueError
    del x
    print('OK')

    print('k degrees', end = ' ')
    if B(12) != Rational(-691, 2730, to_bring=False):
        raise ValueError
    print('OK')

    print(lagrange_sign(5, 17))

#    print('Graph:', end = ' ')
#    x = graph(False, False, False, 2, (1, 2), (2, 1))
#    print('OK')
