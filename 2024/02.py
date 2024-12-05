from typing import List

from utils import Problem, ProblemRunner


class Problem2024Day02(Problem):
    """Solution to 2024/problems/02.md"""

    def __init__(self):
        """Splits the lines by whitespace to construct the list of reports."""
        super().__init__()
        self.reports = [line.split() for line in self.lines]

    @staticmethod
    def is_safe(report: List[int]) -> bool:
        """Determines whether a report is safe.

        :param report: the report to verify
        :return: true if safe, false otherwise
        """
        if report == sorted(report):
            prev_level = None
            for level in report:
                if prev_level is None or (prev_level != level and prev_level + 4 > level):
                    prev_level = level
                else:
                    return False
        elif report == sorted(report, reverse=True):
            prev_level = None
            for level in report:
                if prev_level is None or (prev_level != level and prev_level - 4 < level):
                    prev_level = level
                else:
                    return False
        else:
            return False

        return True

    def detect_safe(self, reports: List[List[str]], level_dampener_enabled: bool = False) -> int:
        """Calculates the total number of safe reports.

        :param reports: the reports to verify
        :param level_dampener_enabled: whether to use level dampening
        :return: the total number of safe reports
        """
        total_safe = 0
        for report in reports:
            int_report = [int(c) for c in report]
            if self.is_safe(int_report):
                total_safe += 1
            elif level_dampener_enabled:
                for i in range(len(int_report)):
                    cloned = int_report.copy()
                    del cloned[i]
                    if self.is_safe(cloned):
                        total_safe += 1
                        break

        return total_safe

    def part_one(self) -> int:
        """Calculates the total number of safe reports without level dampening.

        :return: the total number of safe reports
        """
        return self.detect_safe(self.reports)

    def part_two(self) -> int:
        """Calculates the total number of safe reports with level dampening.

        :return: the total number of safe reports
        """
        return self.detect_safe(self.reports, True)


if __name__ == "__main__":
    ProblemRunner(Problem2024Day02).run()
