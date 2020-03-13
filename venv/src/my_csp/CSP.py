from typing import Generic, TypeVar, Dict, List, Optional

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
            print("TESTING " + self.left_var + self.op + self.right_var)
            if self.op == '<':
                return assignment[self.left_var] < assignment[self.right_var]
            elif self.op == '>':
                return assignment[self.left_var] < assignment[self.right_var]
            elif self.op == '=':
                return assignment[self.left_var] == assignment[self.right_var]
            elif self.op == '!':
                return assignment[self.left_var] != assignment[self.right_var]


class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables = variables
        self.domains = domains
        self.constraints = list()

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def check_valid(self, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints:
            if not constraint.isValid(assignment):
                return False
        return True

    def backtracking_search(self, assignment: Dict[V, D] = None) -> Optional[Dict[V, D]]:
        if assignment is None:
            assignment = {}
            print("Initial Assignment: %s" % assignment)
        if len(assignment) == len(self.variables):
            print("return assignment")
            return assignment
        unassigned: List[V] = [variable for variable in self.variables if variable not in assignment]
        current_var = unassigned[0]
        for value in self.domains[current_var]:
            if self.check_valid(assignment):
                assignment[current_var] = value
                result = self.backtracking_search(assignment)
                if result is not None:
                    return result
            else:
                print(assignment)
                assignment.pop(current_var)
        return None
