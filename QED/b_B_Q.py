from itertools import groupby
from decimal import Decimal
from ..lists import DynamicMultiDimCoordList as DMDCL


# TODO: Написать ошибки и документацию


def B_table(M_up, M_bypass=set(), mass=Decimal(1)):
    """
    Returning computed table T such that T[i, j] is \\vec{B}(i, j bypassing M_bypass, mass, sign) for all (i, j) in
    'upper bound' M_up.

    :param M_up: Upper bounding set. It means that there will be computed only points in M_up and all points to the left
    or lower than these points.
    :param M_bypass: Set to bypass.
    :param mass: Mass from mass model.

    :return: Computed Table of vectors \\vec{B}.
    """

    Temp = sorted(M_up, key=lambda pair: (pair[0], -pair[1]))
    Temp = reversed([list(g)[0] for k, g in groupby(Temp, key=lambda pair: pair[0])])
    u_max = float('-inf')
    M_up = []
    for pair in Temp:
        if u_max < pair[1]:
            M_up.append(pair)
            u_max = pair[1]
    del Temp, u_max

    t = max(list(map(lambda pair: pair[0], M_up)))
    u = max(list(map(lambda pair: pair[1], M_up)))

    Table = DMDCL(2)
    M_check = DMDCL(2)
    for i in range(t + 1):
        for j in range(u + 1):
            M_check[i, j] = (i, j) in M_bypass

    Table[0, 0] = (0, 1)

    U = -1

    for point in M_up:
        for i in range(point[0] + 1):
            for j in range(U + 1, point[1] + 1):
                if i or j:
                    Table[i, j] = (0, 0)
                if i != 0 and not M_check[i - 1, j]:
                    Table[i, j] = (Table[i, j][0], Table[i, j][1] - mass * Table[i - 1, j][0] + Table[i - 1, j][1])
                if j != 0 and not M_check[i, j - 1]:
                    Table[i, j] = (Table[i, j][0] + Table[i, j - 1][0] + mass * Table[i, j - 1][1], Table[i, j][1])

    return Table


def b_table(M_up, M_bypass=set(), mass=Decimal(1)):
    """
    Returning computed table T such that T[i, j] is \\vec{b}(i, j bypassing M_bypass, mass, sign) for all (i, j) in
    'upper bound' M_up.

    :param M_up: Upper bounding set. It means that there will be computed only points in M_up and all points to the left
    or lower than these points.
    :param M_bypass: Set to bypass.
    :param mass: Mass from mass model.

    :return: Computed Table of vectors \\vec{b}.
    """

    Table = B_table(M_up, M_bypass=M_bypass, mass=mass)
    for point in Table.indices:
        y = point[0] + point[1]
        if type(mass) == float:
            Table[point] = (Table[point][0] / (1 + mass ** 2) ** (y / 2),
                            Table[point][1] / (1 + mass ** 2) ** (y / 2))
        else:
            Table[point] = (Table[point][0] / ((1 + mass ** 2) ** y).sqrt(),
                            Table[point][1] / ((1 + mass ** 2) ** y).sqrt())

    return Table


def Q_table(M_up, M_bypass=set(), mass=Decimal(1)):
    """
    Returning computed table T such that T[i, j] is Q(i, j bypassing M_bypass, mass, sign) for all (i, j) in
    'upper bound' M_up.

    :param M_up: Upper bounding set. It means that there will be computed only points in M_up and all points to the left
    or lower than these points.
    :param M_bypass: Set to bypass.
    :param mass: Mass from mass model.

    :return: Computed Table of vectors Q.
    """

    Table = B_table(M_up, M_bypass=M_bypass, mass=mass)
    for point in Table.indices:
        y = point[0] + point[1]
        Table[point] = (Table[point][0] ** 2 + Table[point][1] ** 2) / (1 + mass ** 2) ** y

    return Table


def vec_B(t, u, M_bypass=set(), mass=Decimal(1), sign=None):
    """
    Vector \\vec{A}(x, y) in t-u coordinates with the same arguments.

    :param t: t-coordinate on lattice.
    :param u: u-coordinate on lattice.
    :param M_bypass: Set to bypass.
    :param mass: Mass from definition.
    :param sign: '+', '-' or None for '+'-vector, '-'-vector or common vector.

    :return: Vector-value in (t, u).
    """

    def return_it(vec):
        if sign == '+':
            return 0, vec[1]
        elif sign == '-':
            return vec[0], 0
        else:
            return vec

    if t < 0 or u < 0:
        return return_it((0, 0))

    Table = B_table({(t, u)}, M_bypass=M_bypass, mass=mass)

    return return_it(Table[t, u])


def vec_b(t, u, M_bypass=set(), mass=Decimal(1), sign=None):
    """
    Vector \\vec{a}(x, y) in t-u coordinates with the same arguments.

    :param t: t-coordinate on lattice.
    :param u: u-coordinate on lattice.
    :param M_bypass: Set to bypass.
    :param mass: Mass from definition.
    :param sign: '+', '-' or None for '+'-vector, '-'-vector or common vector.

    :return: Vector-value in (t, u).
    """

    B = vec_B(t, u, M_bypass=M_bypass, mass=mass, sign=sign)
    if type(mass) == float:
        return B[0] / (1 + mass ** 2) ** ((t + u) / 2), B[1] / (1 + mass ** 2) ** ((t + u) / 2)
    else:
        return B[0] / ((1 + mass ** 2) ** (t + u)).sqrt(), B[1] / ((1 + mass ** 2) ** (t + u)).sqrt()


def Q(t, u, M_bypass=set(), mass=Decimal(1), sign=None):
    """
    Probability to get to point (t, u).

    :param t: t-coordinate on lattice.
    :param u: u-coordinate on lattice.
    :param M_bypass: Set to bypass.
    :param mass: Mass in model.
    :param sign: '+', '-' or None for '+'-probability, '-'-probability or common probability.

    :return: Probability to get to point (t, u).
    """

    B = vec_B(t, u, M_bypass=M_bypass, mass=mass, sign=sign)
    return (B[0] ** 2 + B[1] ** 2) / (1 + mass ** 2) ** (t + u)


def Q_set(M, M_bypass=set(), mass=Decimal(1)):
    """
    Probability to get to set M.

    :param M: Set, which probability is computing.
    :param M_bypass: Set to bypass.
    :param mass: Mass in model.

    :return: Probability to get to set M.
    """

    Table = B_table(M, M_bypass, mass=mass)

    return sum(list(map(lambda pair: (Table[pair][0] ** 2 + Table[pair][1] ** 2) /
                                     (1 + mass ** 2) ** (pair[0] + pair[1]), M)))
