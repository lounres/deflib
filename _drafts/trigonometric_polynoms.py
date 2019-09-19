from ..polynomials import Polynomial
from ..rings_n_fields import Rational
from ..combinatorial import binomial


def cos_of_n_args(n):
    return sum([Polynomial('x', field=Rational) ** (n - 2 * k) * Polynomial('x^2-1', field=Rational) ** k * binomial(n, 2 * k) for k in range(n // 2 + 1)])