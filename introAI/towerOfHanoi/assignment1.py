#ring and post project
#Sebastian Dobon
#EECS 348
import copy, sys

sys.setrecursionlimit(8200)

disks = input('How many disks? ')
pegs = input('How many pegs? ')


fullPost = range(disks, 0, -1)


class systemState:
    def __init__(self):
        self.curr = [ [] for _ in range(pegs) ]
        self.history = []

stateInit = systemState()
stateInit.curr[0] = fullPost

forGlobalHistory = []
baseDepth = 0


def goDeeper(state, globalHistory, depth):
    depth += 1

    print state.curr

    lastState = copy.deepcopy(state.curr)
    state.history.append(lastState)
    globalHistory.append(lastState)

    #check if state is the solution
    if state.curr[-1] == fullPost:
        print "success!"
        print len(state.history)
        print state.history
        return True

    #limit for depth of recursion
    if depth <= pow(2, disks + 3):

        #loop throuh all possible moves
        for moveFrom in state.curr:
            for moveTo in state.curr:

                #copy the state object, we will be editing the new copy
                newState = copy.deepcopy(state)

                #if moveFrom has any disks on the stack, grab the top
                if len(moveFrom) > 0:
                    moving = newState.curr[state.curr.index(moveFrom)].pop()

                    #if it is a valid move, put the disk down
                    if moveFrom != moveTo and (len(newState.curr[state.curr.index(moveTo)]) == 0 or moving < newState.curr[state.curr.index(moveTo)][-1]):
                        newState.curr[state.curr.index(moveTo)].append(moving)

                        if newState.curr not in globalHistory:

                            # the if statement here allows the "return True" at the top to carry all the
                            # way back to the top and exit the recursion when a solution is found
                            if goDeeper(newState, globalHistory, depth):
                                return True

goDeeper(stateInit, forGlobalHistory, baseDepth)
print "done!"
