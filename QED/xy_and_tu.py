def t_u(x, y):
    if (x + y) % 2:
        t = (x + y) / 2 - 1
        u = (y - x) / 2
    else:
        t = (x + y) // 2 - 1
        u = (y - x) // 2
    return t, u


def x_y(t, u):
    x = t - u + 1
    y = t + u + 1
    return x, y
