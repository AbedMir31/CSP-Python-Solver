from typing import Generic, TypeVar, Dict, List
from io import StringIO

V = TypeVar('V')
D = TypeVar('D')


class BinaryConstraint:
    def __init__(self, left_var, op, right_var):
        self.left_var = left_var
        self.right_var = right_var
        self.op = op

    def isValid(self, assignment: Dict[V, D]) -> bool:
        if self.left_var not in assignment or self.right_var not in assignment:
            return True
        else:
            print("Testing %s=%d %s %s=%d" % (self.left_var, assignment[self.left_var], self.op, self.right_var,
                                              assignment[self.right_var]))
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
        left, right, op = None, None, None
        if var1 == self.left_var:
            left = val1
        elif var1 == self.right_var:
            right = val1
        if var2 == self.left_var:
            left = val2
        elif var2 == self.right_var:
            right = val2
        if op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '=':
            return left == right
        elif op == '!':
            return left != right

    def __str__(self):
        return "%s%s%s" % (self.left_var, self.op, self.right_var)


def assign(var, value: int, assignment):
    assignment[var] = value


def unassign(var, assignment):
    if var in assignment:
        del assignment[var]


class CSP(Generic[V, D]):
    count = 0

    def __init__(self, variables: List[V], domains: Dict[V, List[D]], forward_check):
        self.current_domain = None
        self.trim_domain = None
        self.variables = variables
        self.domains = domains
        self.constraints = list()
        self.forward_check = forward_check

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def print_assignment(self, assignment):
        self.count = self.count + 1
        ret = StringIO()
        ret.write("%d. " % self.count)
        for var in assignment:
            ret.write("%s=%d, " % (var, assignment[var]))
        print(ret.getvalue()[:-1], end='')
        if len(assignment) == len(self.variables):
            print("  solution")
        else:
            print("  failure")

    def forward_check(self, var, val, assignment):
        if self.current_domain:
            for (N, n) in self.trim_domain:
                self.current_domain[N].append(n)
            self.trim_domain[var] = []
            for N in self.variables:
                if N not in assignment:
                    for n in self.current_domain[N][:]:
                        if not self.check_current(var, val, N, n):
                            self.current_domain[N].remove(n)
                            self.trim_domain[var].append((N, n))

    def check_current(self, var1, val1, var2, val2):
        for constraint in self.constraints:
            if not constraint.check_two(var1, val1, var2, val2):
                return False
        return True

    def check_conflicts(self, var, value, assignment: Dict[V, D]) -> int:
        test = assignment.copy()
        assign(var, value, test)
        num_conflicts = 0
        for constraint in self.constraints:
            # print("Constraint: %s" % constraint)
            if not constraint.isValid(test):
                num_conflicts = num_conflicts + 1
        return num_conflicts

    def choose_var(self, assignment):
        print("Choosing Var: ")
        unassigned: List[V] = [v for v in self.variables if v not in assignment]
        unassigned.sort(key=lambda var: (self.find_legal(var), self.most_constraints(var), var))
        print("UNASSIGNED: %s" % unassigned)
        return unassigned[0]

    def find_legal(self, var):
        if self.current_domain:
            return len(self.current_domain[var])
        else:
            """
            legal = list()
            for val in self.domains[var]:
                if self.check_conflicts(var, val, assignment) == 0:
                    legal.append(val)
            print("Var %s has %d legal values" % (var, len(legal)))
            return len(legal)
            """
            return len(self.domains[var])

    def most_constraints(self, var):
        num_constraint = 0
        for constraint in self.constraints:
            if constraint.in_constraint(var):
                num_constraint = num_constraint + 1
        return num_constraint

    def order_val(self, var: V, assignment: Dict[V, D]):
        if self.current_domain:
            domain = self.current_domain[var]
        else:
            domain = self.domains[var]
        domain.sort(key=lambda val: (self.check_conflicts(var, val, assignment)))
        print("SORTED DOMAIN for %s: %s" % (var, domain))
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
            print("Initial Assignment: %s" % assignment)
        if len(assignment) == len(self.variables):
            self.print_assignment(assignment)
            return assignment
        current_var = self.choose_var(assignment)
        print("Current Var: %s" % current_var)
        for value in self.order_val(current_var, assignment):
            print("Going to check %s and %s" % (current_var, value))
            if self.forward_check or self.check_conflicts(current_var, value, assignment) == 0:
                print("Check passed")
                assignment[current_var] = value
                print("Assigned %s to %s" % (current_var, value))
                result = self.recursive_backtrack(assignment)
                if result is not None:
                    return result
                print("Backtracking from %s=%s" % (current_var, assignment[current_var]))
                unassign(current_var, assignment)
            print("Check failed")
        return None
