import sys


class Maze:
    """
    Attributes:
    size: length of the Alice Maze
    start: tuple representing coordinates of start cell
    goal: tuple representing coordinates of goal cell
    grid: 2D array representing te actual grid
    """

    def __init__(self):
        self.size = 0
        self.start = None
        self.goal = None
        self.grid = []

    def set_size(self, new_size):
        self.size = new_size

    # Initialize the lists representing each row in grid
    def initialize_rows(self):
        for i in range(self.size):
            self.grid.append([])

    def append_cell(self, cell, row):
        self.grid[row].append(cell)

    def set_goal(self, goal):
        self.goal = goal

    def set_start(self, start):
        self.start = start

    def solve(self):
        # Initialize attributes for BFS
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j].all_distances = []
        # Initialize Empty "Queue"
        queue = []
        (x, y) = self.start
        queue.append((x, y, 1, [self.start]))

        while len(queue) != 0:
            (x, y, dist, curr_path) = queue.pop(0)
            # Update distance value
            if self.grid[x][y].arrow_colour == "Red":
                dist += 1
            elif self.grid[x][y].arrow_colour == "Yellow":
                dist -= 1
            # Traverse through "adjacent" edges
            if dist != 0:
                for direction in self.grid[x][y].directions:
                    next_path = curr_path[:]
                    # Calculate next cell
                    next_x = x + dist * direction[0]
                    next_y = y + dist * direction[1]
                    # Check if new cell is in grid
                    if 0 <= next_x < self.size and 0 <= next_y < self.size:
                        if dist not in self.grid[next_x][next_y].all_distances:
                            self.grid[next_x][next_y].all_distances.append(dist)
                            next_path.append((next_x, next_y))
                            # Check to make sure if we have hit the goal
                            if (next_x, next_y) == self.goal:
                                return next_path
                            queue.append((next_x, next_y, dist, next_path))
        return []


class Cell:
    """
    Attributes:
    arrow_colour: colour of arrows in cell
    directions: list of valid directions from this cell
    all_distances: all step_sizes encountered by this cell
    """

    def __init__(self, arrow_colour):
        self.directions = []
        self.arrow_colour = arrow_colour
        self.all_distances = []

    def set_directions(self, directions):
        numerical = {"S": (0, 1), "N": (0, -1), "W": (-1, 0), "E": (1, 0),
                     "NW": (-1, -1), "NE": (1, -1), "SW": (-1, 1), "SE": (1, 1)}

        for direction in directions:
            self.directions.append(numerical[direction])

if __name__ == "__main__":
    # You do NOT need to include any error checking. I found this particular
    # check personally helpful, when I forgot to provide a filename.
    if len(sys.argv) != 2:
        print("Usage: python3 Alice.py <inputfilename>")
        sys.exit()

    # Here is how you open a file whose name is given as the first argument
    f = open(sys.argv[1])
    # Initialize a new Maze Object
    maze = Maze()

    # SET UP DATA STRUCTURES
    file_info = f.readline().strip()
    size = int(file_info)
    maze.set_size(size)
    # initialize rows for maze
    maze.initialize_rows()
    # Read each cell
    curr_row = 0
    curr_col = 0
    file_info = f.readline().strip()
    while file_info != '':
        cell_info = file_info.split(",")
        # Set Cell info
        new_cell = Cell(cell_info[0])
        if cell_info[1] != "NULL":
            direction = cell_info[1].split()
            new_cell.set_directions(direction)

        # Append Cell to Maze
        maze.append_cell(new_cell, curr_row)
        # update start/goal accordingly in maze
        if len(cell_info) == 3:
            if cell_info[2] == "Initial":
                maze.set_start((curr_row, curr_col))
            elif cell_info[2] == "Goal":
                maze.set_goal((curr_row, curr_col))

        # Update counters of current coordinate
        if curr_row == maze.size - 1:
            curr_row = 0
            curr_col += 1
        else:
            curr_row += 1
        file_info = f.readline().strip()

    a = maze.solve()
    #Format response
    if len(a) == 0:
        print(f'{a}, {len(a)}')
    else:
        print(f'{a}, {len(a) - 1}')
