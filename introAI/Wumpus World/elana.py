# Theodore Bisdikian and Elana Stettin

import updatewumpus
import FOPC
from Queue import Queue

KB = set()
patterns = {('clean', '?x'), ('nasty', '?x'), ('calm', '?x'), ('breeze', '?x')}

# Adds to the knowledge base based on perceptions
def make_statements(w, p):
    loc = p[5]
    if ('visited', loc) not in KB:
        KB.add(('safe', loc))
        KB.add(('visited', loc))
        for pat in patterns:
            for per in p:
                bindings = {}
                statement = (per, loc)
                if FOPC.match(statement, pat, bindings):
                    st = FOPC.instantiate(statement, bindings)
                    KB.add((st[0], st[1]))
        adj_pattern = ('adjacent', '?x', '?y')
        for adj_cell in updatewumpus.look_ahead(w):
            statements = []
            statements.append(('adjacent', loc, adj_cell))
            statements.append(('adjacent', adj_cell, loc))
            for s in statements:
                bindings = {}
                if FOPC.match(s, adj_pattern, bindings):
                    adj_list = FOPC.instantiate(s, bindings)
                    KB.add((adj_list[0], adj_list[1], adj_list[2]))
        make_inferences(w, p)


# implement a list of rules to make inferences
# if the wumpus is found, kill the wumpus
def make_inferences(w, p):
    loc = p[5]
    for x in updatewumpus.look_ahead(w):
        if ('calm', loc) in KB:
            KB.add(('solid', x))
        if ('clean', loc) in KB:
            KB.add(('no wumpus', x))
        if ('nasty', loc) in KB:
            if('safe', x) not in KB:
                if ('wumpus?', x) in KB:
                    kill_wumpus(w, p, x)
                    KB.remove(('wumpus?', x))
                    KB.add(('no wumpus', x))
                else:
                    KB.add(('wumpus?', x))
        if ('solid', x) in KB and ('no wumpus', x) in KB:
            KB.add(('safe', x))
            if ('wumpus?', x) in KB:
                KB.remove(('wumpus?', x))


# Turn to an adjacent cell, given your location and the string of an adjacent cell
def turn_adjacent(w, p, target):
    loc = p[5]
    x = int(loc[-2])
    y = int(loc[-1])
    tx = int(target[-2])
    ty = int(target[-1])

    if(x-1 == tx):
        if p[6] != "Left":
            updatewumpus.take_action(w, "Left")
    elif(x+1 == tx):
        if p[6] != "Right":
            updatewumpus.take_action(w, "Right")
    elif(y-1 == ty):
        if p[6] != "Down":
            updatewumpus.take_action(w, "Down")
    elif(y+1 == ty):
        if p[6] != "Up":
            updatewumpus.take_action(w, "Up")
    else:
        print "ERROR"


# Move to an adjacent cell, given your location and the string of an adjacent cell
def move_adjacent(w, p, target):
    turn_adjacent(w, p, target)
    ret = updatewumpus.take_action(w, "Step")
    make_statements(w, ret)
    return ret

# Returns a list of safe adjacent cells to get from your location to a target
def route_planner(w, p, target):
    class routeCell:
        def __init__(self, name, prev):
            self.name = name
            self.prev = prev
    q = Queue()
    q.put(routeCell(p[5], None))
    tarCell = None

    while q.not_empty:
        cur = q.get(False)
        if cur.name == target:
            tarCell = cur
            break
        for adj in get_adjacent_cells(cur.name):
            if ('safe', adj) in KB:
                q.put(routeCell(adj, cur))

    ret = []
    while(tarCell):
        ret.insert(0, tarCell.name)
        tarCell = tarCell.prev
    ret.pop(0)
    return ret

# Returns a list of adjacent cells from the knowledge base given a str input
def get_adjacent_cells(cell):
    ret = []
    x = int(cell[-2])
    y = int(cell[-1])
    if ('adjacent', cell, 'Cell ' + str(x+1) + str(y)) in KB:
        ret.append('Cell ' + str(x+1) + str(y))
    if ('adjacent', cell, 'Cell ' + str(x-1) + str(y)) in KB:
        ret.append('Cell ' + str(x-1) + str(y))
    if ('adjacent', cell, 'Cell ' + str(x) + str(y+1)) in KB:
        ret.append('Cell ' + str(x) + str(y+1))
    if ('adjacent', cell, 'Cell ' + str(x) + str(y-1)) in KB:
        ret.append('Cell ' + str(x) + str(y-1))
    return ret


# Move from current cell to target cell given a list of moves
def move_to_target(w, p, moves):
    current = p
    while(len(moves) > 0):
        current = move_adjacent(w, current, moves.pop(0))
    return current


# return all cells in KB that are safe and have not been visited
def get_all_options():
    opts = []
    for statement in KB:
        cell = statement[1]
        if ('safe', cell) in KB and ('visited', cell) not in KB:
            if cell not in opts:
                opts.append(cell)
    return opts


# Kill the wumpus
def kill_wumpus(w, p, wumpus):
    turn_adjacent(w, p, wumpus)
    updatewumpus.take_action(w, "Shoot")


# The main planning function
def planner(w, p):
    while(len(get_all_options()) > 0):
        opts = get_all_options()
        opt_paths = map(lambda(x): route_planner(w, p, x), opts)
        path = opt_paths[0]
        for o in opt_paths:
            if len(o) < len(path):
                path = o
        p = move_to_target(w, p, path)
        if(p[2] == 'glitter'):
            updatewumpus.take_action(w, "PickUp")
    move_to_target(w, p, route_planner(w, p, 'Cell 11'))
    updatewumpus.take_action(w, "Exit")


def main():
    name = updatewumpus.intialize_world()
    current = updatewumpus.take_action(name, "Down")
    make_statements(name, current)
    planner(name, current)


if __name__ == '__main__':
    main()
