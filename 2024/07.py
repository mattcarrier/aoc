from dataclasses import dataclass, field
from enum import Enum
from typing import List, Set

from utils import Problem, ProblemRunner


class Problem2024Day07(Problem):
    """Solution to 2024/problems/07.md"""

    def __init__(self):
        """Parses the problem input into a list of tuples of target result to list of constants."""
        super().__init__()
        self.parsed_lines = [
            (int(split[0]), [int(i) for i in split[1].strip().split()])
            for split in [line.split(":") for line in self.lines]
        ]

    class Operator(Enum):
        """Represents possible operators."""

        ADD = 1
        MULTIPLY = 2
        CONCATENATION = 3

        def evaluate(self, left: int, right: int) -> int:
            """Evaluates the operation.

            :param left: the left constant
            :param right: the right constant
            :return: the result
            """
            if self == Problem2024Day07.Operator.ADD:
                return left + right
            elif self == Problem2024Day07.Operator.MULTIPLY:
                return left * right
            elif self == Problem2024Day07.Operator.CONCATENATION:
                return int(f"{left}{right}")

            raise NotImplementedError(f"Operator: {self.name}")

    @dataclass
    class EquationSolver:
        """Dataclass that tries to solve possible equations."""

        target_result: int
        constants: List[int]
        possible_operators: Set["Problem2024Day07.Operator"]
        is_valid: bool = field(init=False)

        def __post_init__(self) -> None:
            """Tries to solve the equation."""
            possible_results = {self.constants[0]}
            for i, num in enumerate(self.constants[1:]):
                next_possible_results = set()
                for current_result in possible_results:
                    for op in self.possible_operators:
                        next_possible_results.add(op.evaluate(current_result, num))

                possible_results = next_possible_results

            self.is_valid = self.target_result in possible_results

    def solve_for_operators(self, possible_operators: Set["Problem2024Day07.Operator"]) -> int:
        """Tries to solve all possible equations with the given set of possible operators.

        :param possible_operators: the possible operator set
        :return: summation of the results of all valid equations
        """
        return sum(
            eq.target_result
            for eq in [
                Problem2024Day07.EquationSolver(
                    target_result=target_result, constants=constants, possible_operators=possible_operators
                )
                for target_result, constants in self.parsed_lines
            ]
            if eq.is_valid
        )

    def part_one(self) -> int:
        """Finds all the coordinates that the guard traverses along their predetermined path.

        :return: the total number of coordinates
        """
        return self.solve_for_operators({self.Operator.ADD, self.Operator.MULTIPLY})

    def part_two(self) -> int:
        """Finds all the possible coordinates where a single obstacle can be placed that would trick the guard to get
        caught in a looping path.

        :return: the total number of possible coordinates
        """
        return self.solve_for_operators({op for op in self.Operator})


if __name__ == "__main__":
    ProblemRunner(Problem2024Day07).run()
