def chutes_and_ladders(x, t):
    OPT = {}
    n = len(x) - 1

    prob = .166666666666666

    for i in range(n):
        OPT[i, 1] = 0

    #initialize first 6 in front of finish
    OPT[n-1, 1] = 6 * prob
    OPT[n-2, 1] = 5 * prob
    OPT[n-3, 1] = 4 * prob
    OPT[n-4, 1] = 3 * prob
    OPT[n-5, 1] = 2 * prob
    OPT[n-6, 1] = 1 * prob

    #if we make it past finish, succeeded for sure
    for i in range(1,7):
        OPT[n+0, i] = 6 * prob
        OPT[n+1, i] = 6 * prob
        OPT[n+2, i] = 6 * prob
        OPT[n+3, i] = 6 * prob
        OPT[n+4, i] = 6 * prob
        OPT[n+5, i] = 6 * prob

    #first loop, skipping chutes for memoization
    for i in range(n-1, -1, -1):
        for R in range(2, t+1):
            sigma = 0
            for roll in range(1, 7):
                sigma += prob * OPT[i + roll, R-1]
            #if we choose to roll the die
            if x[i] <= 0:
                OPT[i,R] = sigma
            #else we choose to take the ladder
            else:
                OPT[i,R] = max(sigma, OPT[i + x[i], R])
            if OPT[i,R] > 1:
                OPT[i,R] = 1.0
    #second loop adding chutes back in
    for i in range(n-1, -1, -1):
        for R in range(2, t+1):
            sigma = 0
            for roll in range(1, 7):
                sigma += prob * OPT[i + roll, R-1]
            #if we choose to roll the die
            if x[i] == 0:
                OPT[i,R] = sigma
            #else we choose to take the chute/ladder
            else:
                OPT[i,R] = max(sigma, OPT[i + x[i], R])
            if OPT[i,R] > 1:
                OPT[i,R] = 1.0

    #to fix rounding issues
    for i, R in OPT.iterkeys():
        if OPT[i,R] > .9999:
            OPT[i,R] = 1.0

    for i in range(0, n):
        print 'Position ' +  str(i + 1)
        print '     ' + str(OPT[i, t])

chutes_and_ladders([0,0,0,0,0,0,0,0,0,0,0], 3)
'''
Results - Printing the prob starting from each position with T rolls remaining

chutes_and_ladders([0,0,0,0,0,0,0,0,0,0,0], 3)

Position 1
     0.625
Position 2
     0.740740740741
Position 3
     0.837962962963
Position 4
     0.907407407407
Position 5
     0.953703703704
Position 6
     0.981481481481
Position 7
     0.99537037037
Position 8
     1.0
Position 9
     1.0
Position 10
     1.0

chutes_and_ladders([0,0,0,0,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 5)

Position 1
     0.309670781893
Position 2
     0.313914609053
Position 3
     0.336805555556
Position 4
     0.378986625514
Position 5
     1.0
Position 6
     0.399691358025
Position 7
     0.5
Position 8
     0.600308641975
Position 9
     0.694830246914
Position 10
     0.778549382716
Position 11
     0.84799382716
Position 12
     0.902006172839
Position 13
     0.941229423868
Position 14
     0.967592592593
Position 15
     0.983796296296
Position 16
     0.992798353909
Position 17
     0.997299382716
Position 18
     0.999228395062
Position 19
     0.999871399177
Position 20
     1.0
Position 21
     1.0
Position 22
     1.0
Position 23
     1.0
Position 24
     1.0

The results get better when we add in a short chute after a big ladder

chutes_and_ladders([0,0,0,0,15,0,-4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 5)

Position 1
     0.331147119342
Position 2
     0.331661522634
Position 3
     0.350823045267
Position 4
     0.389274691358
Position 5
     1.0
Position 6
     0.40625
Position 7
     0.5
Position 8
     0.600308641975
Position 9
     0.694830246914
Position 10
     0.778549382716
Position 11
     0.84799382716
Position 12
     0.902006172839
Position 13
     0.941229423868
Position 14
     0.967592592593
Position 15
     0.983796296296
Position 16
     0.992798353909
Position 17
     0.997299382716
Position 18
     0.999228395062
Position 19
     0.999871399177
Position 20
     1.0
Position 21
     1.0
Position 22
     1.0
Position 23
     1.0
Position 24
     1.0
'''
