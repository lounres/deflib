# Checking for primality of the number
def primality(n):
    n = abs(n)
    if n <= 1:
        return False
    prime_numbers = [True] * (n + 1)
    for i in range(2, int(n ** 0.5) + 1):
        if prime_numbers[i]:
            for j in range(n // i + 1):
                prime_numbers[i * j] = False
    return prime_numbers[n]


# Lagrange's sign of a and p
def lagrange_sign(a, p):
    if type(a) != int:
        raise TypeError(type(a).__name__ + ' object cannot be interpreted as an integer')
    if type(p) != int:
        raise TypeError(type(p).__name__ + ' object cannot be interpreted as an integer')
    if not primality(p):
        raise ValueError(str(p) + ' isn\'t prime')

    def find_prime_divider(n, lower_verge=2):
        for i in range(max(lower_verge, 2), int(n ** 0.5) + 1):
            if not n % i:
                return i
        return n

    a %= p
    if a == 0:
        return 0
    if p == 2:
        return 1

    result = 1
    prime_div = find_prime_divider(a)
    while a != 1:
        order_of_prime = 0
        while not a % prime_div:
            a //= prime_div
            order_of_prime += 1
        if order_of_prime % 2:
            if prime_div == 2:
                if p % 8 not in [1, 7]:
                    result *= -1
            else:
                result *= lagrange_sign(p, prime_div) * (-1) ** ((p - 1) * (prime_div - 1) // 4)
        prime_div = find_prime_divider(a, prime_div + 1)
    return result
