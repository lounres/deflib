import math
import functools
from .exceptions import LogicError


# Binomial coefficient from n to k
def binomial(n, k):
    if type(n) != int or type(k) != int:
        raise TypeError('Binomial coefficient only for non-negative integers')
    if n < 0 or k < 0:
        raise LogicError('Binomial coefficient only for non-negative integers')
    if n < k:
        raise LogicError('Binomial coefficient only from non-less integer to non-greater integer')
    return math.factorial(n) // math.factorial(k) // math.factorial(n-k)


# Greatest Common Divisor from only two numbers
bin_gcd = math.gcd


# Greatest Common Divisor from many numbers
def gcd(*nums):
    if not all(map(lambda i: True if type(i) == int else False, nums)):
        raise TypeError('GCD exists only for integers')
    return functools.reduce(bin_gcd, nums)
