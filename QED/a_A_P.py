from decimal import Decimal
from ..lists import DynamicMultiDimCoordList as DMDCL
from .b_B_Q import B_table, b_table, Q_table, vec_B, vec_b, Q, Q_set
from .xy_and_tu import t_u, x_y


def _t_u_corrected(x, y):
    return t_u(x, y - (x + y) % 2)


def A_table(M_up, M_bypass=set(), mass=Decimal(1)):
    """
    Returning computed table T such that T[i, j] is \\vec{A}(i, j bypassing M_bypass, mass, sign) for all (i, j) in
    'upper bound' M_up.

    :param M_up: Upper bounding set. It means that there will be computed only points in M_up and all points to the left
    or lower than these points.
    :param M_bypass: Set to bypass.
    :param mass: Mass from mass model.

    :return: Computed Table of vectors \\vec{A}.
    """

    M_up = {_t_u_corrected(*point) for point in M_up}
    M_bypass = {t_u(*point) for point in filter(lambda point: (point[0] + point[1] + 1) % 2, M_bypass)}

    Table_B = B_table(set(M_up), M_bypass)
    Table_A = DMDCL(2)

    for point in Table_B.indices:
        Table_A[x_y(*point)] = Table_B[point]

    return Table_A


def a_table(M_up, M_bypass=set(), mass=Decimal(1)):
    """
    Returning computed table T such that T[i, j] is \\vec{a}(i, j bypassing M_bypass, mass, sign) for all (i, j) in
    'upper bound' M_up.

    :param M_up: Upper bounding set. It means that there will be computed only points in M_up and all points to the left
    or lower than these points.
    :param M_bypass: Set to bypass.
    :param mass: Mass from mass model.

    :return: Computed Table of vectors \\vec{a}.
    """

    M_up = {_t_u_corrected(*point) for point in M_up}
    M_bypass = {t_u(*point) for point in filter(lambda point: (point[0] + point[1] + 1) % 2, M_bypass)}

    Table_b = b_table(set(M_up), M_bypass)
    Table_a = DMDCL(2)

    for point in Table_b.indices:
        Table_a[x_y(*point)] = Table_b[point]

    return Table_a


def P_table(M_up, M_bypass=set(), mass=Decimal(1)):
    """
    Returning computed table T such that T[i, j] is P(i, j bypassing M_bypass, mass, sign) for all (i, j) in
    'upper bound' M_up.

    :param M_up: Upper bounding set. It means that there will be computed only points in M_up and all points to the left
    or lower than these points.
    :param M_bypass: Set to bypass.
    :param mass: Mass from mass model.

    :return: Computed Table of vectors P.
    """

    M_up = {_t_u_corrected(*point) for point in M_up}
    M_bypass = {t_u(*point) for point in filter(lambda point: (point[0] + point[1] + 1) % 2, M_bypass)}

    Table_Q = Q_table(set(M_up), M_bypass)
    Table_P = DMDCL(2)

    for point in Table_Q.indices:
        Table_P[x_y(*point)] = Table_Q[point]

    return Table_P


def vec_A(x, y, M_bypass=set(), mass=Decimal(1), sign=None):
    """
    Vector \\vec{A}(x, y) in t-u coordinates with the same arguments.

    :param x: x-coordinate on lattice.
    :param y: y-coordinate on lattice.
    :param M_bypass: Set to bypass.
    :param mass: Mass from definition.
    :param sign: '+', '-' or None for '+'-vector, '-'-vector or common vector.

    :return: Vector-value in (t, u).
    """

    M_bypass = {t_u(*point) for point in filter(lambda point: (point[0] + point[1] + 1) % 2, M_bypass)}

    if (x + y) % 2:
        return 0, 0
    else:
        return vec_B(*t_u(x, y), M_bypass=M_bypass, mass=mass, sign=sign)


def vec_a(x, y, M_bypass=set(), mass=Decimal(1), sign=None):
    """
    Vector \\vec{a}(x, y) in x-y coordinates with the same arguments.

    :param x: x-coordinate on lattice.
    :param y: y-coordinate on lattice.
    :param M_bypass: Set to bypass.
    :param mass: Mass from definition.
    :param sign: '+', '-' or None for '+'-vector, '-'-vector or common vector.

    :return: Vector-value in (x, y).
    """

    M_bypass = {t_u(*point) for point in filter(lambda point: (point[0] + point[1] + 1) % 2, M_bypass)}

    if (x + y) % 2:
        return 0, 0
    else:
        return vec_b(*t_u(x, y), M_bypass=M_bypass, mass=mass, sign=sign)


def P(x, y, M_bypass=set(), mass=Decimal(1), sign=None):
    """
    Probability to get to point (x, y).

    :param x: x-coordinate on lattice.
    :param y: y-coordinate on lattice.
    :param M_bypass: Set to bypass.
    :param mass: Mass in model.
    :param sign: '+', '-' or None for '+'-probability, '-'-probability or common probability.

    :return: Probability to get to point (x, y).
    """

    M_bypass = {t_u(*point) for point in filter(lambda point: (point[0] + point[1] + 1) % 2, M_bypass)}

    if (x + y) % 2:
        return 0, 0
    else:
        return Q(*t_u(x, y), M_bypass=M_bypass, mass=mass, sign=sign)


def P_set(M, M_bypass=set(), mass=Decimal(1)):
    """
    Probability to get to set M.

    :param M: Set, which probability is computing.
    :param M_bypass: Set to bypass.
    :param mass: Mass in model.

    :return: Probability to get to set M.
    """

    M = {t_u(*point) for point in filter(lambda point: (point[0] + point[1] + 1) % 2, M)}
    M_bypass = {t_u(*point) for point in filter(lambda point: (point[0] + point[1] + 1) % 2, M_bypass)}

    return Q_set(M, M_bypass=M_bypass, mass=mass)
