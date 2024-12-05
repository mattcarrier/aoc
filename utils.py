import os
import sys
import time
from contextlib import contextmanager
from typing import Generator, List, Type


class Timed:
    """A context manager that times the execution of a function."""

    def __init__(self):
        self.execution_time = None

    @contextmanager
    def start(self) -> Generator["Timed", None, None]:
        start = time.time() * 1000
        try:
            yield self
        finally:
            self.execution_time = round(time.time() * 1000 - start, 5)

    @staticmethod
    def sum(*timed: "Timed") -> float:
        return round(sum((t.execution_time for t in timed)), 5)


class Problem:
    def __init__(self):
        self.lines = self.read_input_file()

    def part_one(self) -> int | str:
        raise NotImplementedError()

    def part_two(self) -> int | str:
        raise NotImplementedError()

    @staticmethod
    def read_input_file() -> List[str]:
        """Reads the txt file with the same name as the basename of the script in an "input" directory in the same
        directory as the execution script.

        :return: the contained lines in the input file
        """
        script_split = sys.argv[0].split(os.path.sep)
        with open(os.path.sep + os.path.join(*script_split[:-1], "input", script_split[-1].replace("py", "txt"))) as f:
            return [line.strip() for line in f.readlines()]


class ProblemRunner:
    """Runner class for problems that handles calculating timings for all pieces of the problem solution."""

    def __init__(self, problem_type: Type[Problem]):
        self.problem_type = problem_type

    def run(self):
        with Timed().start() as setup_time:
            problem = self.problem_type()

        with Timed().start() as part1_time:
            p1 = problem.part_one()

        with Timed().start() as part2_time:
            p2 = problem.part_two()

        print("-------\nAnswers\n-------")
        print(f"Part 1: {p1}")
        print(f"Part 2: {p2}")

        print("\n-----------\nTiming (ms)\n-----------")
        print(f"Setup: {setup_time.execution_time}")
        print(
            f"Part 1: algorithmic: {part1_time.execution_time} | "
            f"algorithmic + setup: {Timed.sum(setup_time, part1_time)}"
        )

        print(
            f"Part 2: algorithmic: {part2_time.execution_time} | "
            f"algorithmic + setup: {Timed.sum(setup_time, part2_time)}"
        )

        print(
            f"Combined: algorithmic: {Timed.sum(part1_time, part2_time)} | "
            f"algorithmic + setup: {Timed.sum(setup_time, part1_time, part2_time)}"
        )
