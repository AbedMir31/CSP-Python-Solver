from io import BytesIO as StringIO
import sys


class BinaryConstraint:
    def __init__(self, left_var, op, right_var):
        self.left_var = left_var
        self.right_var = right_var
        self.op = op

    def isValid(self, assignment):
        if self.left_var not in assignment or self.right_var not in assignment:
            return True
        else:
            if self.op == '<':
                return assignment[self.left_var] < assignment[self.right_var]
            elif self.op == '>':
                return assignment[self.left_var] > assignment[self.right_var]
            elif self.op == '=':
                return assignment[self.left_var] == assignment[self.right_var]
            elif self.op == '!':
                return assignment[self.left_var] != assignment[self.right_var]

    def in_constraint(self, var):
        if var == self.left_var or self.right_var:
            return True
        else:
            return False

    def check_two(self, var1, val1, var2, val2):
        left, right = None, None
        if var1 == self.left_var:
            left = val1
        elif var1 == self.right_var:
            right = val1
        if var2 == self.left_var:
            left = val2
        elif var2 == self.right_var:
            right = val2
        if left is None or right is None:
            return True
        else:
            if self.op == '<':
                return left < right
            elif self.op == '>':
                return left > right
            elif self.op == '=':
                return left == right
            elif self.op == '!':
                return left != right

    def __str__(self):
        return "%s%s%s" % (self.left_var, self.op, self.right_var)


class CSP:
    count = 0

    def __init__(self, variables, domains, forward_check):
        self.current_domain = None
        self.trim_domain = None
        self.variables = variables
        self.domains = domains
        self.constraints = list()
        self.forward_check = forward_check

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def assign(self, var, val, assignment):
        assignment[var] = val
        if self.current_domain:
            if self.forward_check:
                self.do_forward_check(var, val, assignment)

    def unassign(self, var, assignment):
        if var in assignment:
            if self.current_domain:
                self.current_domain[var] = self.domains[var][:]
            del assignment[var]

    def print_assignment(self, assignment):
        if not len(assignment) == 0:
            self.count = self.count + 1
            ret = StringIO()
            ret.write("%d. " % self.count)
            for var in assignment:
                ret.write("%s=%d, " % (var, assignment[var]))
            sys.stdout.write(ret.getvalue()[:-2])
            if len(assignment) == len(self.variables):
                sys.stdout.write("  solution\n")
            else:
                sys.stdout.write("  failure\n")

    def do_forward_check(self, var, val, assignment):
        if self.current_domain:
            for (N, n) in self.trim_domain[var]:
                self.current_domain[N].append(n)
            self.trim_domain[var] = []
            for N in self.variables:
                if N not in assignment:
                    for n in self.current_domain[N][:]:
                        for c in self.constraints:
                            if not BinaryConstraint.check_two(c, var, val, N, n):
                                self.current_domain[N].remove(n)
                                self.trim_domain[var].append((N, n))

        # print("REDUCED curr domain: %s" % self.current_domain)

    def check_conflicts(self, var, val, assignment):
        test = assignment.copy()
        self.assign(var, val, test)
        num_conflicts = 0
        for constraint in self.constraints:
            if not constraint.isValid(test):
                num_conflicts = num_conflicts + 1
        return num_conflicts

    def check_neighbors(self, var, val):
        num_conflicts = 0
        for neighbor in self.variables:
            if not var == neighbor:
                for nval in self.domains[neighbor]:
                    for c in self.constraints:
                        if not BinaryConstraint.check_two(c, var, val, neighbor, nval):
                            num_conflicts = num_conflicts + 1
        return num_conflicts

    def choose_var(self, assignment):
        # print("Choosing Var: ")
        unassigned = [v for v in self.variables if v not in assignment]
        unassigned.sort(key=lambda var: (self.find_legal(var), self.most_constraints(var), var))
        # print("UNASSIGNED: %s" % unassigned)
        return unassigned[0]

    def find_legal(self, var):
        if self.current_domain:
            # print("Curr Domain: %s, len: %d" % (self.current_domain[var], len(self.current_domain[var])))
            return len(self.current_domain[var])
        else:
            # print("Domain len: %d" % len(self.domains[var]))
            return len(self.domains[var])

    def most_constraints(self, var):
        num_constraint = 0
        for constraint in self.constraints:
            if constraint.in_constraint(var):
                num_constraint = num_constraint + 1
        return num_constraint

    def order_val(self, var):
        if self.current_domain:
            domain = self.current_domain[var]
            # print("Using current domain: %s" % domain)
        else:
            domain = self.domains[var][:]

        domain.sort(key=lambda val: (self.check_neighbors(var, val), val))
        return domain

    def backtracking_search(self):
        if self.forward_check:
            self.current_domain = {}
            self.trim_domain = {}
            for var in self.variables:
                self.current_domain[var] = self.domains[var][:]
                self.trim_domain[var] = []
        return self.recursive_backtrack({})

    def recursive_backtrack(self, assignment):
        if assignment is None:
            assignment = {}
        if len(assignment) == len(self.variables):
            self.print_assignment(assignment)
            return assignment
        current_var = self.choose_var(assignment)
        for value in self.order_val(current_var):
            if self.forward_check or self.check_conflicts(current_var, value, assignment) == 0:
                self.assign(current_var, value, assignment)
                result = self.recursive_backtrack(assignment)
                if result is not None:
                    return result
                self.unassign(current_var, assignment)
            self.print_assignment(assignment)
        return None
