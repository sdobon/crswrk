def processor_power(n, m, c, C):
    OPT = {}

    for j in range(m):
        OPT[n-1, j] = c[n-1][j]

    for i in range(n-2, -1, -1):
        for j in range(m):
            pp = {}
            for p in range(m):
                if p==j:
                    pp[p] = c[i][j] + OPT[i+1, p]
                else:
                    pp[p] = C + c[i][j] + OPT[i+1, p]
            OPT[i,j] = min(pp.itervalues())

    first_job = {}
    for j in range(m):
        first_job[j] = OPT[0, j]

    print min(first_job.itervalues())

processor_power(3,4, [[4,70, 30, 20], [20,1, 10, 20], [80,90, 20 , 15]],  7)
