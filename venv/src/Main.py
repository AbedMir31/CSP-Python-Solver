from my_csp.CSP import CSP, BinaryConstraint

filename = open("ex1.var", "rt")
variables = list()
domains = dict()
Lines = filename.readlines()
for line in Lines:
    var = line[0]
    variables.append(var)
    num_arr = line[2:len(line)].strip().split(' ')
    num_list = list()
    for num in num_arr:
        num_list.append(int(num))
    domains[var] = num_list
# for v in variables:
# print(v + ": " + str(domains[v]))

csp = CSP(variables, domains, False)
csp.add_constraint(BinaryConstraint('A', '>', 'B'))
csp.add_constraint(BinaryConstraint('B', '>', 'F'))
csp.add_constraint(BinaryConstraint('A', '>', 'C'))
csp.add_constraint(BinaryConstraint('C', '>', 'E'))
csp.add_constraint(BinaryConstraint('A', '>', 'D'))
csp.add_constraint(BinaryConstraint('D', '=', 'E'))
for var in csp.variables:
    print("%s: %s" % (var, csp.domains[var]))
solution = csp.backtracking_search()
# print("%s    solution" % solution)
