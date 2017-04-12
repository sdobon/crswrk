def easy_riding(v):
    n = len(v) - 1
    OPT = {}
    e = {}

    e[n] = 0
    OPT[n] = 0

    for i in range(n-1, -1, -1):
        e[i] = v[i+1] - v[i]
        OPT[i] = min(e[i], e[i] + OPT[i+1])

    print min(OPT.itervalues())


easy_riding([5, 3, 6, 7, 0, 4, 6, 3, 1])
