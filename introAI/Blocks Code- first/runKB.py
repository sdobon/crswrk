import read
import facts_and_rules

facts, rules = read.read_tokenize("statements_backup.txt")

global KB
KB = []

global RB
RB = []

def assert_rule(rule):
    if rule not in RB:
        RB.append(rule)
        infer_from_rule(rule)

def assert_fact(fact):
    if fact not in KB:
        KB.append(fact)
        infer_from_fact(fact)

def infer_from_fact(fact):
    for r in RB:
        bindings = facts_and_rules.match(r.lhs[0], fact)
        if bindings != False:
            if len(r.lhs) == 1:
                new_statement = facts_and_rules.statement(facts_and_rules.instantiate(r.rhs.full, bindings))
                if r.type == "Assert":
                    fact.add_fact(new_statement)
                    assert_fact(new_statement)
                    print "adding inference: " + str(new_statement.full)
                elif r.type == "Retract":
                    retract(new_statement)
                    print "retracting: " + str(new_statement.full)
            else:
                tests = map(lambda x: facts_and_rules.instantiate(x.full, bindings), r.lhs[1:])
                rhs = facts_and_rules.instantiate(r.rhs.full, bindings)
                new_rule = facts_and_rules.rule(tests, rhs)
                fact.add_rule(new_rule)
                assert_rule(new_rule)

def infer_from_rule(rule):
    for f in KB:
        bindings = facts_and_rules.match(rule.lhs[0], f)
        if bindings != False:
            if len(rule.lhs) == 1:
                new_statement = facts_and_rules.statement(facts_and_rules.instantiate(rule.rhs.full, bindings))
                if rule.type == "Assert":
                    f.add_fact(new_statement)
                    assert_fact(new_statement)
                    print "adding inference: " + str(new_statement.full)
                elif rule.type == "Retract":
                    retract(new_statement)
            else:
                tests = map(lambda x: facts_and_rules.instantiate(x.full, bindings), rule.lhs[1:])
                rhs = facts_and_rules.instantiate(rule.rhs.full, bindings)
                new_rule = facts_and_rules.rule(tests, rhs)
                rule.add_rule(new_rule)
                assert_rule(new_rule)

def retract(item):
    for fact in KB:
        if facts_and_rules.match(item, fact) != False:
            remove_supports(fact)

def remove_supports(fact):
    if fact in KB:
        print "Retracting: " + fact.pretty()
        for f in fact.facts:
            remove_supports(f)
        KB.remove(fact)

def ask(pattern):
    for fact in KB:
        bindings_lists = []
        bindings = facts_and_rules.match(pattern, fact)
        if bindings != False:
            bindings_lists.append(bindings)
        for b in bindings_lists:
            print "This is true: \t",
            print facts_and_rules.statement(facts_and_rules.instantiate(pattern.full, b)).pretty()










for new_fact in facts:
    assert_fact(facts_and_rules.statement(new_fact))


for new_rule in rules:
    assert_rule(facts_and_rules.rule(new_rule[0], new_rule[1]))

ask(facts_and_rules.statement(["flat", "?x"]))

for f in KB:
    print f.pretty()
