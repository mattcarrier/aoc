import re
from typing import List, Tuple

from utils import Problem, ProblemRunner


class Problem2024Day03(Problem):
    """Solution to 2024/problems/03.md"""

    @staticmethod
    def identify_mul_ops(lines: List[str]) -> List[Tuple[int, ...]]:
        """Returns all the multiplication operations found in the list of lines.

        :param lines: the list of lines
        :return: all multiplication operations modeled as a Tuple with both integers
        """
        matches = []
        for line in lines:
            matches.extend(
                [tuple([int(i) for i in m[4:-1].split(",")]) for m in re.findall(r"mul\(\d{1,3},\d{1,3}\)", line)]
            )

        return matches

    def part_one(self) -> int:
        """Calculates the sum of all the multiplication operations found in the problem input.

        :return: the sum of all the multiplication operations found in the problem input
        """
        return sum([i * j for i, j in self.identify_mul_ops(self.lines)])

    def part_two(self) -> int:
        """Calculates the sum of all the multiplication operations found in the problem input that are not disabled.

        :return: the sum of all the multiplication operations found in the problem input that are not disabled
        """
        matches = []
        dont_splits = "".join(self.lines).split("don't()")
        matches.extend(self.identify_mul_ops([dont_splits[0]]))
        for dont_split in dont_splits[1:]:
            if "do()" in dont_split:
                matches.extend(self.identify_mul_ops(dont_split.split("do()")[1:]))

        return sum([i * j for i, j in matches])


if __name__ == "__main__":
    ProblemRunner(Problem2024Day03).run()
