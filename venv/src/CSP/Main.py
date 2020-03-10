from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Dict, List, Optional

V = TypeVar('V')
D = TypeVar('D')


class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    @abstractmethod
    def isValid(self, assignment: Dict[V, D]) -> bool:
        ...


class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for var in self.variables:
            self.constraints[var] = []
            if var not in self.domains:
                raise LookupError

    def add_constraint(self, constraint: Constraint[V, D]):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError
            else:
                self.constraints[variable].append(constraint)

    def check_valid(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.isValid(assignment):
                return False

        return True

    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        if len(assignment) == len(self.variables):
            return assignment
        unassigned: List[V] = [variable for variable in self.variables
                               if variable not in assignment]
        current_var = unassigned[0]
        for value in self.domains[current_var]:
            test_assignment = assignment.copy()
            test_assignment[current_var] = value
            if self.check_valid(current_var, test_assignment):
                result: Optional[Dict[V, D]] = self.backtracking_search(test_assignment)
                if result is not None:
                    return result
                else:
                    return None
        return None
