#Pattern - What is <relationship> <name>?

question = ["What", "is", "on", "Block17"]

class Rule:
    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern


global RB
RB = []

simpleRule = Rule("sentence1", ["What", "is", "<relationship>", "<name>"])
RB.append(simpleRule)
secondRule = Rule("relationship", ["on"])

RB.append(secondRule)
RB.append(Rule("name", ["Block17"]))

def invokeParser(question):
    for rule in RB:
        result = applyPattern(question, rule.pattern)
        if result:
            return result
    return False

def applyPattern(question, pattern):
    if len(question) == 0 or len(pattern) == 0:
        return len(question) == 0 and len(pattern) == 0
    if goodToGo(question[0], pattern[0]):
        if pattern[1][0] == "<":
            for r in RB:
                if r.name == pattern[1][0]:
                    # pattern[1] = r.pattern[0]
                    pattern = r.pattern + pattern[1:]
        else:
            pattern = pattern[1:]

        return applyPattern(question[1:], pattern)

def goodToGo(e1, e2):
    print e1, e2
    if e2[0] == "<":
        e2 = e2[1:-1]
        for r in RB:
            if r.name == e2:
                e2 = r.pattern[0]
    if e1 == e2:
        return True
    return False

print invokeParser(question)
