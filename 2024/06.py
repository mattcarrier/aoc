from enum import Enum
from typing import List, Optional, Set, Tuple

from utils import Problem, ProblemRunner


class Problem2024Day06(Problem):
    """Solution to 2024/problems/06.md"""

    class Direction(Enum):
        """Represents the direction of the guard"""

        NORTH = 1
        SOUTH = 2
        EAST = 3
        WEST = 4

        @staticmethod
        def get_directional_chars() -> Set[str]:
            """Returns a set of all directional chars"""
            return {"^", "<", ">", "v"}

        @staticmethod
        def from_str(s: str) -> "Problem2024Day06.Direction":
            """Finds the associated Direction from a string.

            :param s: the string
            :return: the associated Direction
            """
            if s == "^":
                return Problem2024Day06.Direction.NORTH
            elif s == "v":
                return Problem2024Day06.Direction.SOUTH
            elif s == "<":
                return Problem2024Day06.Direction.WEST
            elif s == ">":
                return Problem2024Day06.Direction.EAST

            raise ValueError(f"Invalid Direction: {s}")

    def __init__(self):
        """Parses the input into the following attributes:

        1. mapping of row number to a list of all column numbers that contain obstacles
        2. mapping of col number to a list of all row numbers that contain obstacles
        3. the max column number
        4. the max row number
        5. the initial location and direction of the guard
        """
        super().__init__()
        self.row_obstacles = {}
        self.col_obstacles = {}
        self.max_y = len(self.lines)
        self.max_x = len(self.lines[0])
        directional_chars = Problem2024Day06.Direction.get_directional_chars()
        for row, line in enumerate(self.lines):
            for col, char in enumerate(line):
                if char == "#":
                    self.row_obstacles[row] = self.row_obstacles.get(row, [])
                    self.row_obstacles[row].append(col)

                    self.col_obstacles[col] = self.col_obstacles.get(col, [])
                    self.col_obstacles[col].append(row)
                elif char in directional_chars:
                    self.initial_guard_location = (col, row), Problem2024Day06.Direction.from_str(char)

    @staticmethod
    def finalize_path_segment(
        path_segment: List[Tuple[Tuple[int, int], "Problem2024Day06.Direction"]],
        guard_path: List[Tuple[Tuple[int, int], "Problem2024Day06.Direction"]],
        guard_path_set: Set[Tuple[Tuple[int, int], "Problem2024Day06.Direction"]],
    ) -> bool:
        """Checks to see if the current path segment contains a (location and direction) that has already been traversed
        by the guard.  If so it returns True to mark this path as an infinite loop. If the path segment does not create
        an infinite loop then each location in the path segment is added to the guard_path and guard_path_set.

        :param path_segment: the path segment to check
        :param guard_path: the complete guard path to this point
        :param guard_path_set: the set of all (locations with directions) in the guard path
        :return: True if the path segment is an infinite loop, False otherwise
        """
        for location in path_segment:
            if location in guard_path_set:
                return True
            else:
                guard_path.append(location)
                guard_path_set.add(location)

        return False

    def add_extra_obstacle(
        self,
        guard_coords: Tuple[int, int],
        guard_direction: "Problem2024Day06.Direction",
        extra_obstacle: Optional[Tuple[int, int]] = None,
    ) -> List[int]:
        """Returns a copied version of the row or column obstacles with the request extra obstacle if it makes sense to
        do so, otherwise the current row or column obstacles are returned.

        :param guard_coords: the current guard location
        :param guard_direction: the current guard direction
        :param extra_obstacle: the extra obstacle to add
        :return: the list of obstacles
        """
        if guard_direction in (Problem2024Day06.Direction.WEST, Problem2024Day06.Direction.EAST):
            obstacles = self.row_obstacles.get(guard_coords[1], [])
            if extra_obstacle is not None and extra_obstacle[1] == guard_coords[1]:
                obstacles = obstacles.copy()
                obstacles.append(extra_obstacle[0])
                obstacles.sort()
        else:
            obstacles = self.col_obstacles.get(guard_coords[0], [])
            if extra_obstacle is not None and extra_obstacle[0] == guard_coords[0]:
                obstacles = obstacles.copy()
                obstacles.append(extra_obstacle[1])
                obstacles.sort()

        return obstacles

    def calculate_guard_path(
        self, extra_obstacle: Optional[Tuple[int, int]] = None
    ) -> Tuple[List[Tuple[int, int]], bool]:
        """Constructs the guard path with possible extra obstacle.

        :param extra_obstacle: the extra obstacle to add
        :return: a tuple of the guard path and a boolean indicating if the guard path is an infinite loop
        """
        guard_path = [self.initial_guard_location]
        guard_path_set = set(self.initial_guard_location)
        looping_path = False
        while True:
            guard_coords, guard_direction = guard_path[-1]
            if guard_direction == Problem2024Day06.Direction.WEST:
                obstacles = self.add_extra_obstacle(guard_coords, guard_direction, extra_obstacle)
                obstacle = next((x for x in obstacles[::-1] if x < guard_coords[0]), None)
                if obstacle is not None:
                    path_segment = [
                        ((x, guard_coords[1]), Problem2024Day06.Direction.WEST)
                        for x in range(guard_coords[0] - 1, obstacle + 1, -1)
                    ]
                    path_segment.append(((obstacle + 1, guard_coords[1]), Problem2024Day06.Direction.NORTH))
                    if self.finalize_path_segment(path_segment, guard_path, guard_path_set, extra_obstacle):
                        looping_path = True
                        break
                else:
                    guard_path.extend(
                        [
                            ((x, guard_coords[1]), Problem2024Day06.Direction.WEST)
                            for x in range(guard_coords[0] - 1, -1, -1)
                        ]
                    )
                    break
            elif guard_direction == Problem2024Day06.Direction.EAST:
                obstacles = self.add_extra_obstacle(guard_coords, guard_direction, extra_obstacle)
                obstacle = next((x for x in obstacles if x > guard_coords[0]), None)
                if obstacle is not None:
                    path_segment = [
                        ((x, guard_coords[1]), Problem2024Day06.Direction.EAST)
                        for x in range(guard_coords[0] + 1, obstacle - 1)
                    ]
                    path_segment.append(((obstacle - 1, guard_coords[1]), Problem2024Day06.Direction.SOUTH))
                    if self.finalize_path_segment(path_segment, guard_path, guard_path_set, extra_obstacle):
                        looping_path = True
                        break
                else:
                    guard_path.extend(
                        [
                            ((x, guard_coords[1]), Problem2024Day06.Direction.EAST)
                            for x in range(guard_coords[0] + 1, self.max_x)
                        ]
                    )
                    break
            elif guard_direction == Problem2024Day06.Direction.NORTH:
                obstacles = self.add_extra_obstacle(guard_coords, guard_direction, extra_obstacle)
                obstacle = next((y for y in obstacles[::-1] if y < guard_coords[1]), None)
                if obstacle is not None:
                    path_segment = [
                        ((guard_coords[0], y), Problem2024Day06.Direction.NORTH)
                        for y in range(guard_coords[1] - 1, obstacle + 1, -1)
                    ]
                    path_segment.append(((guard_coords[0], obstacle + 1), Problem2024Day06.Direction.EAST))
                    if self.finalize_path_segment(path_segment, guard_path, guard_path_set, extra_obstacle):
                        looping_path = True
                        break
                else:
                    guard_path.extend(
                        [
                            ((guard_coords[0], y), Problem2024Day06.Direction.NORTH)
                            for y in range(guard_coords[1] - 1, -1, -1)
                        ]
                    )
                    break
            elif guard_direction == Problem2024Day06.Direction.SOUTH:
                obstacles = self.add_extra_obstacle(guard_coords, guard_direction, extra_obstacle)
                obstacle = next((y for y in obstacles if y > guard_coords[1]), None)
                if obstacle is not None:
                    path_segment = [
                        ((guard_coords[0], y), Problem2024Day06.Direction.SOUTH)
                        for y in range(guard_coords[1] + 1, obstacle - 1)
                    ]
                    path_segment.append(((guard_coords[0], obstacle - 1), Problem2024Day06.Direction.WEST))
                    if self.finalize_path_segment(path_segment, guard_path, guard_path_set, extra_obstacle):
                        looping_path = True
                        break
                else:
                    guard_path.extend(
                        [
                            ((guard_coords[0], y), Problem2024Day06.Direction.SOUTH)
                            for y in range(guard_coords[1] + 1, self.max_y)
                        ]
                    )
                    break
            else:
                raise ValueError(f"Invalid Direction: {guard_direction}")

        return [path_segment[0] for path_segment in guard_path], looping_path

    def part_one(self) -> int:
        """Finds all the coordinates that the guard traverses along their predetermined path.

        :return: the total number of coordinates
        """
        return len(set(self.calculate_guard_path()[0]))

    def part_two(self) -> int:
        """Finds all the possible coordinates where a single obstacle can be placed that would trick the guard to get
        caught in a looping path.

        :return: the total number of possible coordinates
        """
        loop_obstacles = set()
        for coords in self.calculate_guard_path()[0][1:]:
            if coords not in loop_obstacles:
                guard_path, is_loop = self.calculate_guard_path(coords)
                if is_loop:
                    loop_obstacles.add(coords)

        return len(loop_obstacles)


if __name__ == "__main__":
    ProblemRunner(Problem2024Day06).run()
