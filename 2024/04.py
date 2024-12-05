from utils import Problem, ProblemRunner


class Problem2024Day04(Problem):
    def __init__(self):
        """Parses the list of lines into a word search matrix"""
        super().__init__()
        self.matrix = [list(line) for line in self.lines]

    def part_one(self) -> int:
        """Finds all the XMAS occurrences in the word search matrix.

        :return: the number of occurrences in the word search matrix
        """
        num_occurrences = 0
        max_y = len(self.matrix) - 4
        max_x = len(self.matrix[0]) - 4
        min_xy = 3
        for y, chars in enumerate(self.matrix):
            for x, c in enumerate(chars):
                if c == "X":
                    # horizontal
                    if x <= max_x and chars[x + 1] == "M" and chars[x + 2] == "A" and chars[x + 3] == "S":
                        num_occurrences += 1
                    if x >= min_xy and chars[x - 1] == "M" and chars[x - 2] == "A" and chars[x - 3] == "S":
                        num_occurrences += 1

                    # vertical
                    if (
                        y <= max_y
                        and self.matrix[y + 1][x] == "M"
                        and self.matrix[y + 2][x] == "A"
                        and self.matrix[y + 3][x] == "S"
                    ):
                        num_occurrences += 1
                    if (
                        y >= min_xy
                        and self.matrix[y - 1][x] == "M"
                        and self.matrix[y - 2][x] == "A"
                        and self.matrix[y - 3][x] == "S"
                    ):
                        num_occurrences += 1

                    # diagonal right
                    if (
                        y >= min_xy
                        and x <= max_x
                        and self.matrix[y - 1][x + 1] == "M"
                        and self.matrix[y - 2][x + 2] == "A"
                        and self.matrix[y - 3][x + 3] == "S"
                    ):
                        num_occurrences += 1
                    if (
                        y <= max_y
                        and x <= max_x
                        and self.matrix[y + 1][x + 1] == "M"
                        and self.matrix[y + 2][x + 2] == "A"
                        and self.matrix[y + 3][x + 3] == "S"
                    ):
                        num_occurrences += 1

                    # diagonal left
                    if (
                        y >= min_xy
                        and x >= min_xy
                        and self.matrix[y - 1][x - 1] == "M"
                        and self.matrix[y - 2][x - 2] == "A"
                        and self.matrix[y - 3][x - 3] == "S"
                    ):
                        num_occurrences += 1
                    if (
                        y <= max_y
                        and x >= min_xy
                        and self.matrix[y + 1][x - 1] == "M"
                        and self.matrix[y + 2][x - 2] == "A"
                        and self.matrix[y + 3][x - 3] == "S"
                    ):
                        num_occurrences += 1

        return num_occurrences

    def part_two(self) -> int:
        """Finds all the X-MAS occurrences in the word search matrix.

        :return: the number of occurrences in the word search matrix
        """
        num_occurrences = 0
        for y, chars in enumerate(self.matrix[1:-1]):
            for x, c in enumerate(chars[1:-1]):
                if c == "A":
                    if (
                        (self.matrix[y][x] == "M" and self.matrix[y + 2][x + 2] == "S")
                        or (self.matrix[y][x] == "S" and self.matrix[y + 2][x + 2] == "M")
                    ) and (
                        (self.matrix[y + 2][x] == "M" and self.matrix[y][x + 2] == "S")
                        or (self.matrix[y + 2][x] == "S" and self.matrix[y][x + 2] == "M")
                    ):
                        num_occurrences += 1

        return num_occurrences


if __name__ == "__main__":
    ProblemRunner(Problem2024Day04).run()
