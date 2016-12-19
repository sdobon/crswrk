#ring and post project
#Sebastian Dobon
#EECS 348
import copy, sys
from collections import deque

disks = input('How many disks? ')
pegs = input('How many pegs? ')

fullPost = range(disks, 0, -1)

class systemState:
    def __init__(self):
        self.curr = [ [] for _ in range(pegs) ]
        self.history = []

state = systemState()
state.curr[0] = fullPost


q = deque([])
q.append(state)

globalHistory = [ state ]

while state.curr[-1] != fullPost:
    print state.curr
    state = q.popleft()

    lastState = copy.deepcopy(state.curr)
    state.history.append(lastState)

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

                    if newState.curr[-1] == fullPost:
                        lastState = copy.deepcopy(newState.curr)
                        newState.history.append(lastState)

                        print "success!"
                        print len(newState.history)
                        print newState.history

                    if newState.curr not in globalHistory:

                        globalHistory.append(newState.curr)
                        q.append(newState)

print "done!"
