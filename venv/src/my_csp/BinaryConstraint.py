from typing import Dict, List
from abc import ABC
from Main import CSP, Constraint


class BinaryConstraint(Constraint[int, chr, int], ABC):
    def __init__(self, left_var: int, op: chr, right_var: int) -> None:
        super().__init__([left_var, op, right_var])
        self.left_var: int = left_var
        self.op: chr = op
        self.right_var: int = right_var

    def isValid(self, assignment: Dict[chr, int]) -> bool:
        if self.left_var not in assignment or self.right_var not in assignment:
            return True
        else:
            if self.op == '<':
                return assignment[self.left_var] < assignment[self.right_var]
            elif self.op == '>':
                return assignment[self.left_var] < assignment[self.right_var]
            elif self.op == '=':
                return assignment[self.left_var] == assignment[self.right_var]
            elif self.op == '!':
                return assignment[self.left_var] != assignment[self.right_var]

