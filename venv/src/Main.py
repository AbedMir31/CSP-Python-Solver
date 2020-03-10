from my_csp.CSP import CSP, Constraint
filename = open("ex1.var", "rt")
variables = list()
domains = dict()
Lines = filename.readlines()
for line in Lines:
    variables.append(line[0])
    domains[line[0]] = line[2:len(line) - 1].strip().split(' ')
for v in variables:
    print(v + ": " + str(domains[v]))