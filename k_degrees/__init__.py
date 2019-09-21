from math import factorial
from ..polynomials import Polynomial
from ..rings_n_fields import Rational


# k degrees
# Second secondary coefficient
def f(j, k):
    dp = [Rational(1)]
    for i in range(k - 1, j - 1, -1):
        dp.append(sum([-dp[k - t] / factorial(t - i + 1) for t in range(i + 1, k + 1)]))
    return dp[-1]

# Previous version (without DP)
# def f(j, k):
#     if j == k:
#         return rat(1)
#     return sum([-f(i, k) / math.factorial(i - j + 1) for i in range(j + 1, k + 1)])


# First secondary coefficient
def t(j, k):
    return (-1) ** (k - j) * f(j, k) * Rational(factorial(k + 1), factorial(j + 1), to_bring=False)


# Coefficient of j + 1 degree of the formal symbol in formula of sum of k degree of natural numbers
def A(j, k):
    return t(j, k) / (k + 1)


# Bernoulli number No. k
def B(k):
    return A(0, k)


# k degrees' polynomial
def k_deg_polynomial(k):
    # x = str(x)
    # return '+'.join([str(A(i, k)) + x + '^' + str(i + 1) for i in range(k + 1)])
    return Polynomial(*([0] + [A(i, k) for i in range(k + 1)]), field=Rational)