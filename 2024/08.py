from typing import Set

from utils import Point, Problem, ProblemRunner


class Problem2024Day08(Problem):
    """Solution to 2024/problems/08.md"""

    def __init__(self):
        """Identifies all antenna locations."""
        super().__init__()

        self.antenna_locations = {}
        for y, line in enumerate(self.lines[::-1]):
            for x, c in enumerate(line):
                if c == ".":
                    continue

                self.antenna_locations[c] = self.antenna_locations.get(c, [])
                self.antenna_locations[c].append(Point(x, y))

        self.oob_x = len(self.lines[0])
        self.oob_y = len(self.lines)

    def is_point_on_grid(self, point: Point) -> bool:
        """Determines whether a point is on the grid.

        :param point: the point to check
        :return: True if point is on the grid, False otherwise
        """
        return 0 <= point.x < self.oob_x and 0 <= point.y < self.oob_y

    def calculate_antinodes(self, p1: Point, p2: Point, resonant_harmonics=False) -> Set[Point]:
        """Calculates the all antinode locations for a pair of antenna locations.

        :param p1: the first antenna location
        :param p2: the second antenna location
        :param resonant_harmonics: True if resonant harmonics should be included, False otherwise
        :return: the set of all antinode locations
        """
        distance_x, distance_y = p1.calculate_distance(p2)
        antinodes = set()

        if resonant_harmonics:
            antinodes.update({p1, p2})

            last_antinode = p1
            while True:
                last_antinode = Point(last_antinode.x + distance_x, last_antinode.y + distance_y)
                if not self.is_point_on_grid(last_antinode):
                    break

                antinodes.add(last_antinode)

            last_antinode = p2
            while True:
                last_antinode = Point(last_antinode.x - distance_x, last_antinode.y - distance_y)
                if not self.is_point_on_grid(last_antinode):
                    break

                antinodes.add(last_antinode)
        else:
            for antinode in {Point(p1.x + distance_x, p1.y + distance_y), Point(p2.x - distance_x, p2.y - distance_y)}:
                if self.is_point_on_grid(antinode):
                    antinodes.add(antinode)

        return antinodes

    def calculate_num_antinodes(self, resonant_harmonics=False) -> int:
        """Calculates the total number of antinode locations on the grid.

        :param resonant_harmonics: True if resonant harmonics should be included, False otherwise
        :return: the total number of antinode locations on the grid
        """
        antinodes = set()
        for signal, locations in self.antenna_locations.items():
            for i, location in enumerate(locations[:-1]):
                for other_location in locations[i + 1 :]:
                    if location != other_location:
                        antinodes.update(
                            {
                                antinode
                                for antinode in self.calculate_antinodes(location, other_location, resonant_harmonics)
                            }
                        )

        return len(antinodes)

    def part_one(self) -> int:
        """Calculates the total number of antinode locations on the grid without resonant harmonics."""
        return self.calculate_num_antinodes()

    def part_two(self) -> int:
        """Calculates the total number of antinode locations on the grid with resonant harmonics."""
        return self.calculate_num_antinodes(resonant_harmonics=True)


if __name__ == "__main__":
    ProblemRunner(Problem2024Day08).run()
