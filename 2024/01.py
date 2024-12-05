from utils import Problem, ProblemRunner


class Problem2024Day01(Problem):
    """Solution to 2024/problems/01.md"""

    def __init__(self):
        """Parses a list of strings into 2 separate lists of integers sorted in increasing order. Each line must have 2
        integers separated by whitespace. The left and right integers will be appended to the left and right lists in
        the return tuple respectively.
        """
        super().__init__()
        list1, list2 = [], []
        for line in self.lines:
            split = line.split()
            list1.append(int(split[0]))
            list2.append(int(split[1]))

        self.list1 = sorted(list1)
        self.list2 = sorted(list2)

    def part_one(self) -> int:
        """Calculates the total distance of two lists by calculating the summation of the absolute distance between two
        lists of integers by index.

        :return: the calculated total distance
        """
        total_distance = 0
        for i in range(len(self.list1)):
            total_distance += abs(self.list1[i] - self.list2[i])

        return total_distance

    def part_two(self) -> int:
        """Calculates the total distance between the two lists with the following formula:

        ```
        for i in list1:
            total_distance += i * <occurrences of i in list2>
        ```

        :return: the calculated total distance
        """
        occurrence_map = {}
        for i in self.list2:
            occurrence_map[i] = occurrence_map.get(i, 0) + 1

        total_distance = 0
        for i in self.list1:
            total_distance += i * occurrence_map.get(i, 0)

        return total_distance


if __name__ == "__main__":
    ProblemRunner(Problem2024Day01).run()
