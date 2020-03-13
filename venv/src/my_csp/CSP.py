from typing import Generic, TypeVar, Dict, List

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
            print("Testing " + self.left_var + "=" + assignment[self.left_var] + self.op + self.right_var +
                  '=' + assignment[self.right_var])
            if self.op == '<':
                return assignment[self.left_var] < assignment[self.right_var]
            elif self.op == '>':
                return assignment[self.left_var] > assignment[self.right_var]
            elif self.op == '=':
                return assignment[self.left_var] == assignment[self.right_var]
            elif self.op == '!':
                return assignment[self.left_var] != assignment[self.right_var]


def print_assignment(assignment):
    for var in assignment:
        print("%s=%s " % (var, assignment[var]), end='')
    print('')


def assign(var, value, assignment):
    assignment[var] = value


def unassign(var, assignment):
    if var in assignment:
        del assignment[var]


class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables = variables
        self.domains = domains
        self.constraints = list()

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def check_valid(self, var, value, assignment: Dict[V, D]) -> bool:
        test = assignment.copy()
        assign(var, value, test)
        for constraint in self.constraints:
            if not constraint.isValid(test):
                return False
        return True

    def choose_var(self, assignment):
        unassigned = [v for v in self.variables if v not in assignment]
        minlegalvar = unassigned[0]
        minlegalval = len(self.domains[unassigned[0]])
        for var in unassigned:
            if len(self.domains[var]) < minlegalval:
                minlegalvar = var
                minlegalval = len(self.domains[var])
        return minlegalvar

    def backtracking_search(self, forward_check: bool):
        if forward_check:
            ...
        return self.recursive_backtrack({})

    def recursive_backtrack(self, assignment):
        if assignment is None:
            assignment = {}
            print("Initial Assignment: %s" % assignment)
        if len(assignment) == len(self.variables):
            print("return assignment")
            return assignment
        current_var = self.choose_var(assignment)
        for value in self.domains[current_var]:
            print("Going to check " + current_var + " and " + value)
            if self.check_valid(current_var, value, assignment):
                print("Check passed")
                assignment[current_var] = value
                result = self.recursive_backtrack(assignment)
                if result is not None:
                    return result
                unassign(current_var, assignment)
            print("Check failed")
        print_assignment(assignment)
        return None
