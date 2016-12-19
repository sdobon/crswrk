import FOPC

statement1 = ['clean', 'Cell 11']
statement2 = ['clean', 'Cell 12']
pattern = ['clean', '?x']
bindings = {}

# first = FOPC.match(statement1,pattern,bindings)
# print first

if FOPC.match(statement1,pattern,bindings):
    print bindings
#
# print statement1 == ['clean', 'Cell 11']
#
# second = FOPC.match(statement2,pattern,first)
#
# if second and len(second) == 0:
#     print 'yes'
#
# rule_result =['safe', '?y']
# print FOPC.instantiate(rule_result, first)
