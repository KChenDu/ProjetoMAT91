import numpy


def euler(f, a, b, n, w0):
    t = numpy.linspace(a, b, n + 1)
    k = (b - a) / n
    w = numpy.zeros(n + 1)
    w[0] = w0
    for i in range(n):
        w[i + 1] = w[i] + k * f(t[i], w[i])
    return t, w


def taylor2(f, ft, fy, a, b, n, w0):
    t = numpy.linspace(a, b, n + 1)
    k = (b - a) / n
    w = numpy.zeros(n + 1)
    w[0] = w0
    for i in range(n):
        w[i + 1] = w[i] \
                   + k * f(t[i], w[i]) \
                   + k ** 2 / 2 * (ft(t[i], w[i]) + fy(t[i], w[i]) * f(t[i], w[i]))
    return t, w


def trapezium(f, a, b, n, w0):
    t = numpy.linspace(a, b, n + 1)
    k = (b - a) / n
    w = numpy.zeros(n + 1)
    w[0] = w0
    for i in range(n):
        w[i + 1] = w[i]\
            + k * (f(t[i], w[i]) + f(t[i] + k, w[i] + k * f(t[i], w[i]))) / 2
    return t, w


def mean(f, a, b, n, w0):
    t = numpy.linspace(a, b, n + 1)
    k = (b - a) / n
    w = numpy.zeros(n + 1)
    w[0] = w0
    for i in range(n):
        w[i + 1] = w[i] + k * f(t[i] + k / 2, w[i] + k * f(t[i], w[i]) / 2)
    return t, w


def rk4(f, a, b, n, w0):
    t = numpy.linspace(a, b, n + 1)
    k = (b - a) / n
    w = numpy.zeros(n + 1)
    w[0] = w0
    for i in range(n):
        s1 = f(t[i], w[i])
        s2 = f(t[i] + k / 2, w[i] + k / 2 * s1)
        s3 = f(t[i] + k / 2, w[i] + k / 2 * s2)
        s4 = f(t[i] + k, w[i] + k * s3)
        w[i + 1] = w[i] + k / 6 * (s1 + 2 * s2 + 2 * s3 + s4)
    return t, w
