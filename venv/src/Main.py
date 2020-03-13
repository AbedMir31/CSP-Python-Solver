from my_csp.CSP import CSP, BinaryConstraint
import sys

# for arg in enumerate(sys.argv):
#    print(arg)
filename = open(sys.argv[1], "rt")
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

if sys.argv[3] == "fc":
    fc = True
elif sys.argv[3] == "none":
    fc = False
else:
    raise ValueError
csp = CSP(variables, domains, fc)

fileCon = open(sys.argv[2], "rt")
linesCon = fileCon.readlines()
leftop = list()
rightop = list()
op = list()
for line in linesCon:
    con = BinaryConstraint(line[0], line[2], line[4])
    csp.add_constraint(con)

solution = csp.backtracking_search()
# print("%s    solution" % solution)
