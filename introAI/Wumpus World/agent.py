import updatewumpusNowWithRocks
import FOPC
import copy

# world = updatewumpusNowWithRocks.intialize_my_world("Cell 41", "Cell 44", ["Cell 14","Cell 23","Cell 32"])
world = updatewumpusNowWithRocks.intialize_world()

facts = []
rules = [
            [
                ['solid', '?y'],   #then
                ['calm', '?x'],    #if
                ['adjacent', '?x', '?y'] #and
            ],
            [
                ['uninhabited', '?y'],
                ['clean', '?x'],
                ['adjacent', '?x', '?y']
            ],
            [
                ['safe', '?x'],
                ['solid', '?x'],
                ['uninhabited', '?x']
            ],
            [
                ['wumpus', '?d'],
                ['safe', '?a'],
                ['adjacent', '?a', '?b'],
                ['adjacent', '?a', '?c'],
                ['nasty', '?b'],
                ['nasty', '?c'],
                ['adjacent', '?b', '?d'],
                ['adjacent', '?c', '?d']
            ],
            [
                ['pit', '?d'],
                ['safe', '?a'],
                ['adjacent', '?a', '?b'],
                ['adjacent', '?a', '?c'],
                ['breeze', '?b'],
                ['breeze', '?c'],
                ['adjacent', '?b', '?d'],
                ['adjacent', '?c', '?d']
            ],
            [
                ['try_rock', '?a'],
                ['safe', '?a'],
                ['safe', '?b'],
                ['pit', '?c'],
                ['adjacent', '?a', '?b'],
                ['adjacent', '?a', '?c']
            ],
            [
                ['try_rock', '?a'],
                ['safe', '?a'],
                ['pit', '?b'],
                ['pit', '?c'],
                ['adjacent', '?a', '?b'],
                ['adjacent', '?a', '?c']
            ]
]

#functions related to KB / inference_engine

def insert_fact(fact, facts):
    if fact not in facts:
        facts.append(fact)

def add_percepts(world, percepts, facts):
    location = percepts[5]
    insert_fact( [percepts[0], location], facts )
    insert_fact( [percepts[1], location], facts )
    adjacents = updatewumpusNowWithRocks.look_ahead(world)
    for adjacent in adjacents:
        insert_fact( ['adjacent', location, adjacent], facts)

def contains_variable(phrase):
    for term in phrase:
        if FOPC.is_variable(term):
            return True
    return False

def all_are_facts_or_variables(sequence, facts):
    for phrase in sequence[1:]: #skip the first phrase
        if (not contains_variable(phrase)) and (phrase not in facts):
            return False
    return True

def ready_to_insert(sequence, facts):
    for phrase in sequence[1:]: #skip the first phrase
        if phrase not in facts:
            return False
        # curr = copy.deepcopy(sequence)
        # curr.remove(phrase)
        # if phrase in curr:
        #     return False
    if contains_variable(sequence[0]):
        return False
    else:
        return True

def continuing_without_duplication(sequence, bindings):
    for phrase in sequence:
        for term in phrase:
            if term in bindings.values():
                return False
    return True

def branch(sequence, facts):

    if ready_to_insert(sequence, facts):
        insert_fact(sequence[0], facts)

    for fact in facts:
        for pattern in sequence[1:]:

            bindings = {}
            if FOPC.match(fact, pattern, bindings): #also calls match and alters bindings
                if continuing_without_duplication(sequence, bindings):  #checks if we are trying to double bind (ie ?y = ?x = Cell 11)
                    new_sequence = []
                    for phrase in sequence:
                        new_sequence.append(FOPC.instantiate(phrase, bindings))
                    if all_are_facts_or_variables(new_sequence, facts):
                        branch(new_sequence, facts)

def inference_engine(rules, facts):
    KBsize = 0
    while len(facts) != KBsize:
        KBsize = len(facts)
        print str(KBsize) + " facts in KB"
        for rule in rules:
            branch(rule, facts)

#functions related to planner

def face_to(to_cell, percepts):
    cur_cell = percepts[5]
    # `Cell 12` and `Cell 11`
    if cur_cell[5] == to_cell[5]:
        return 'Up' if to_cell[6] > cur_cell[6] else 'Down'
    elif cur_cell[6] == to_cell[6]:
        return 'Right' if to_cell[5] > cur_cell[5] else 'Left'
    return None




def find_gold(world, percepts, facts, rules, order_to_visit, trace):
    location = percepts[5]

    if location in order_to_visit:
        order_to_visit.remove(location)
    order_to_visit.append(location)
    trace.append(location)

    # add facts and run inferences
    add_percepts(world, percepts, facts)
    inference_engine(rules, facts)

    adjacents = updatewumpusNowWithRocks.look_ahead(world)

    if ['try_rock', location] in facts:
        print "trying rock"
        for cell in adjacents:
            if ['pit', cell] not in facts and ['safe', cell] not in facts:
                print "found a guess"
                updatewumpusNowWithRocks.take_action(world, face_to(cell, percepts))
                sound = updatewumpusNowWithRocks.take_action(world, 'Toss')
                if sound == 'Quiet':
                    insert_fact(['pit', cell], facts)
                if sound == 'Clink':
                    insert_fact(['solid', cell], facts)
        facts.remove(['try_rock', location])

    for cell in adjacents:
        if ['wumpus', cell] in facts:
            updatewumpusNowWithRocks.take_action(world, face_to(cell, percepts))
            percepts = updatewumpusNowWithRocks.take_action(world, 'Shoot')
            for fact in facts:
                if fact[0] == 'wumpus' or fact[0] == 'nasty':
                    facts.remove(fact)
                    print "removing fact" + str(fact)
            return percepts

    # this block moves to an adjacent cell if any are safe & unvisited
    for cell in adjacents:
        if cell not in order_to_visit:
            if ['safe', cell] in facts:
                print "\n*********************************\nTrying unvisited cell: " + str(cell)
                updatewumpusNowWithRocks.take_action(world, face_to(cell, percepts))
                percepts = updatewumpusNowWithRocks.take_action(world, 'Step')
                return percepts

    # this block ranks cells to move to, choosing the one that was visited the longest ago, then moves
    # that cell to the end of the order
    rankings = []
    for cell in adjacents:
        if ['safe', cell] in facts:
            rankings.append( order_to_visit.index(cell) )
        else:
            rankings.append( 999 )
    index = rankings.index( min(rankings) )
    if min(rankings) < 999:
        # get the min scored cell
        move_to = adjacents[index]

        # move to end of list
        order_to_visit.remove(move_to)
        order_to_visit.append(move_to)

        # move to that cell
        print "\n*********************************\nTrying to revisit " + str(move_to)
        updatewumpusNowWithRocks.take_action(world, face_to(move_to, percepts))
        percepts = updatewumpusNowWithRocks.take_action(world, 'Step')
        return percepts
    move_to = trace[-2]
    print "\n*********************************\nTrying to step back to " + str(move_to)
    updatewumpusNowWithRocks.take_action(world, face_to(move_to, percepts))
    percepts = updatewumpusNowWithRocks.take_action(world, 'Step')
    return percepts

def go_back_home(world, home, percepts, order_to_visit):
    location = percepts[5]
    adjacents = updatewumpusNowWithRocks.look_ahead(world)
    for cell in order_to_visit[order_to_visit.index(home):]:
        if cell in adjacents:
            updatewumpusNowWithRocks.take_action(world, face_to(cell, percepts))
            percepts = updatewumpusNowWithRocks.take_action(world, 'Step')
            return percepts


#start the actual solutione


order_to_visit = []
trace = []
percepts = updatewumpusNowWithRocks.take_action(world, "Up")

home = percepts[5]

while percepts[2] != 'glitter' and percepts[7] != 'dead': #until we find the gold
    percepts = find_gold(world, percepts, facts, rules, order_to_visit, trace)

print order_to_visit
add_percepts(world, percepts, facts)
inference_engine(rules, facts)

updatewumpusNowWithRocks.take_action(world, "PickUp")

while percepts[5] != home:
    percepts = go_back_home(world, home, percepts, order_to_visit)

updatewumpusNowWithRocks.take_action(world, "Exit")

for fact in facts:
    print fact
