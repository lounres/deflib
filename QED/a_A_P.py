from decimal import Decimal
from .b_B_Q import B_table, b_table, Q_table, vec_B, vec_b, Q_set


def A_table(M_up, M_bypass=set(), mass=Decimal(1)):
    """
    Returning computed table T such that T[i][j] is \\vec{A}(i, j bypassing M_bypass, mass, sign) for all (i, j) in
    'upper bound' M_up.

    :param M_up: Upper bounding set. It means that there will be computed only points in M_up and all points to the left
    or lower than these points.
    :param M_bypass: Set to bypass.
    :param mass: Mass from mass model.

    :return: Computed Table of vectors \\vec{A}.
    """
    pass


def a_table(M_up, M_bypass=set(), mass=Decimal(1)):
    pass


def P_table(M_up, M_bypass=set(), mass=Decimal(1)):
    pass


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
    pass


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
    pass


def P(x, y, M_bypass=set(), mass=Decimal(1)):
    """
    Probability to get to point (x, y).

    :param x: x-coordinate on lattice.
    :param y: y-coordinate on lattice.
    :param M_bypass: Set to bypass.
    :param mass: Mass in model.

    :return: Probability to get to point (x, y).
    """
    pass


def P_set(M, M_bypass=set(), mass=Decimal(1)):
    """
    Probability to get to set M.

    :param M: Set, which probability is computing.
    :param M_bypass: Set to bypass.
    :param mass: Mass in model.

    :return: Probability to get to set M.
    """
    pass
