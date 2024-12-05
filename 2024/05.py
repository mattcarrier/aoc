from typing import List

from utils import Problem, ProblemRunner


class Problem2024Day05(Problem):
    def __init__(self):
        """Parses the problem input.

        Part 1 (Ordering Rules) -- Page Left must print before Page Right (Pipe-Delimited):
        69|26
        93|46
        93|43
        ...

        Empty-Line

        Part 2 (Manual Updates):
        57,47,82,32,18
        74,56,86,81,84,44,53,92,12,36,15,66,95,26,71
        26,68,47,42,73,41,52,44,78,64,24,76,29,82,38
        ...
        """
        super().__init__()
        printing_rules = {}
        manual_updates = []
        part1 = True
        for line in self.lines:
            if line == "":
                part1 = False
                continue

            if part1:
                left, right = line.split("|")
                rules = printing_rules.get(left, set())
                rules.add(right)
                printing_rules[left] = rules
            else:
                manual_updates.append(line.split(","))

        self.printing_rules = printing_rules
        self.manual_updates = manual_updates

    def is_update_valid(self, update: List[str]) -> bool:
        """Checks whether the update is valid.

        :param update: the update to check
        :return: true if the update is valid, false otherwise
        """
        prev_pages = []
        for s in update:
            if s not in self.printing_rules:
                continue

            for p in prev_pages:
                if p in self.printing_rules[s]:
                    return False

            prev_pages.append(s)

        return True

    def part_one(self) -> int:
        """Calculates the total of all the middle numbers in the valid updates.

        :return: the calculated total
        """
        total_valid_medians = 0
        for u in self.manual_updates:
            if self.is_update_valid(u):
                total_valid_medians += int(u[int(len(u) / 2)])

        return total_valid_medians

    def part_two(self) -> int:
        """Reorders the invalid updates and calculates the total of all the middle numbers of the reordered updates.

        :return: the calculated total
        """
        total_valid_medians = 0
        for u in self.manual_updates:
            if not self.is_update_valid(u):
                u_copy = u.copy()
                while True:
                    invalid = False
                    for oi, i in enumerate(u_copy[::-1]):
                        for ni, j in enumerate(u_copy[: len(u_copy) - (oi + 1)]):
                            if j in self.printing_rules[i]:
                                invalid = True
                                break

                        if invalid:
                            break

                    if invalid:
                        u_copy.pop(len(u_copy) - (oi + 1))
                        u_copy = [i, *u_copy] if ni == 0 else [*u_copy[:ni], i, *u_copy[ni:]]
                    else:
                        break

                total_valid_medians += int(u_copy[int(len(u_copy) / 2)])
        return total_valid_medians


if __name__ == "__main__":
    ProblemRunner(Problem2024Day05).run()
