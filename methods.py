import numpy


def euler(f, a, b, n, w0):
    t = numpy.linspace(a, b, n + 1)
    h = (b - a) / n
    w = numpy.zeros(n + 1)
    w[0] = w0
    for i in range(n):
        w[i + 1] = w[i] + h * f(t[i], w[i])
    return t, w


def taylor2(f, ft, fy, a, b, n, w0):
    t = numpy.linspace(a, b, n + 1)
    h = (b - a) / n
    w = numpy.zeros(n + 1)
    w[0] = w0
    for i in range(n):
        w[i + 1] = w[i] \
                   + h * f(t[i], w[i]) \
                   + h ** 2 / 2 * (ft(t[i], w[i]) + fy(t[i], w[i]) * f(t[i], w[i]))
    return t, w


def trapezium(f, a, b, n, w0):
    t = numpy.linspace(a, b, n + 1)
    h = (b - a) / n
    w = numpy.zeros(n + 1)
    w[0] = w0
    for i in range(n):
        w[i + 1] = w[i]\
            + h * (f(t[i], w[i]) + f(t[i] + h, w[i] + h * f(t[i], w[i]))) / 2
    return t, w


def mean(f, a, b, n, w0):
    t = numpy.linspace(a, b, n + 1)
    h = (b - a) / n
    w = numpy.zeros(n + 1)
    w[0] = w0
    for i in range(n):
        w[i + 1] = w[i] + h * f(t[i] + h / 2, w[i] + h * f(t[i], w[i]) / 2)
    return t, w


def rk4(f, a, b, n, w0):
    t = numpy.linspace(a, b, n + 1)
    h = (b - a) / n
    w = numpy.zeros(n + 1)
    w[0] = w0
    for i in range(n):
        s1 = f(t[i], w[i])
        s2 = f(t[i] + h / 2, w[i] + h / 2 * s1)
        s3 = f(t[i] + h / 2, w[i] + h / 2 * s2)
        s4 = f(t[i] + h, w[i] + h * s3)
        w[i + 1] = w[i] + h / 6 * (s1 + 2 * s2 + 2 * s3 + s4)
    return t, w


def rkf(f, a, b, w0, tol, Kmax, Kmin):
    w = numpy.array(w0)
    t = numpy.array(a)
    k = Kmax
    flag = 1
    i = 1
    tt = a
    ww = w0
    while flag == 1:
        F0 = k * f(tt, ww)
        F1 = k * f(tt + k / 4, ww + F0 / 4)
        F2 = k * f(tt + 3 * k / 8, ww + 3 * F0 / 32 + 9 * F1 / 32)
        F3 = k * f(tt + 12 * k / 13, ww + 1932 * F0 / 2197 - 7200 * F1 / 2197 + 7296 * F2 / 2197)
        F4 = k * f(tt + k, ww + 439 * F0 / 216 - 8 * F1 + 3680 * F2 / 513 - 845 * F3 / 4104)
        F5 = k * f(tt + k / 2, ww - 8 * F0 / 27 + 2 * F1 - 3544 * F2 / 2565 + 1859 * F3 / 4104 - 11 * F4 / 40)
        R = abs(F0 / 360 - 128 * F2 / 4275 - 2197 * F3 / 75240 + F4 / 50 + 2 * F5 / 55) / k
        if R <= tol:
            tt = tt + k
            ww = ww + 25 * F0 / 216 + 1408 * F2 / 2565 + 2197 * F3 / 4104 - F4 / 5
        delta = 0.84 * (tol / R) ** (1 / 4)
        if delta <= 0.1:
            k = 0.1*k
        elif delta >= 4:
            k = 4 * k
        else:
            k = delta * k
        if k > Kmax:
            k = Kmax
        if tt >= b:
            flag = 0
        if tt + k >= b:
            k = b - tt
        if k < Kmin:
            flag = -1
        if R <= tol:
            i += 1
            t = numpy.append(t, tt)
            w = numpy.append(w, ww)
    return t, w


def pc(f, a, b, n, w0):
    t = numpy.linspace(a, b, n + 1)
    h = (b - a) / n
    w = numpy.zeros(n + 1)
    w[0] = w0
    for i in range(4):
        s1 = f(t[i], w[i])
        s2 = f(t[i] + h / 2, w[i] + h / 2 * s1)
        s3 = f(t[i] + h / 2, w[i] + h / 2 * s2)
        s4 = f(t[i] + h, w[i] + h * s3)
        w[i + 1] = w[i] + h / 6 * (s1 + 2 * s2 + 2 * s3 + s4)
        t[i + 1] = t[i] + h
    for i in range(4, n):
        w[i + 1] = w[i] + h * (55 * f(t[i], w[i]) - 59 * f(t[i - 1], w[i - 1]) + 37 * f(t[i - 2], w[i - 2]) - 9 * f(t[i - 3], w[i - 3])) / 24
        t[i + 1] = t[i] + h
        w[i + 1] = w[i] + h * (9 * f(t[i + 1], w[i + 1]) + 19 * f(t[i], w[i]) - 5 * f(t[i - 1], w[i - 1]) + f(t[i - 2], w[i - 2])) / 24
    return t, w
