import time


class Cell:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.status = 'dead'
        self.adjacent_cells_list = self._get_adjacent_cells_list()
        self.next_status = ''

    def _get_adjacent_cells_list(self):
        adjacent_cells_list = []
        for x_increment in [-1, 0, 1]:
            for y_increment in [-1, 0, 1]:
                if x_increment!=0 and y_increment!=0:
                    adjacent_cells_list.append((self.x + x_increment, self.y + y_increment))
        return adjacent_cells_list


class Matrix:

    def __init__(self, x_lim, y_lim):

        self.x_lim = x_lim
        self.y_lim = y_lim
        self.cell_grid = ((Cell(x, y) for x in range(x_lim)) for y in range(y_lim))

    def get_cell_from_coordinate(self, cell_coordinate):
        return self.cell_grid[cell_coordinate[0]][cell_coordinate[1]]

    def check_status_of_cell(self, cell_coordinate):
        return self.get_cell_from_coordinate(cell_coordinate).status

    def count_alive_adjacent_cells(self, cell_coordinate):
        count = 0
        for cell_coordinate in self.cell_grid[cell_coordinate[0]][cell_coordinate[1]].adjacent_cells_list:
            if self.check_status_of_cell(cell_coordinate) == 'alive':
                count += 1
        return count

    def update_next_epoc_matrix_status(self):
        for x in range(0, self.x_lim):
            for y in range(0, self.y_lim):
                self.update_next_epoc_cell_status((x, y))

    def update_next_epoc_cell_status(self, cell_coordinate):
        if (
                self.count_alive_adjacent_cells(cell_coordinate) > 2
        ) | (
                self.count_alive_adjacent_cells(cell_coordinate) < 1
        ):
            self.get_cell_from_coordinate(cell_coordinate).next_status = 'dead'

        else:
            self.get_cell_from_coordinate(cell_coordinate).next_status = 'alive'

    def enter_next_epoc(self):
        for cell_row in self.cell_grid:
            for cell in cell_row:
                cell.status = cell.next_status
                cell.next_status = ''

    def set_initial_state(self, alive_coordinates_list):
        for coordinate_pair in alive_coordinates_list:
            self.get_cell_from_coordinate(coordinate_pair).status = 'alive'

    def run_for_n_epocs(self, n, time_interval):
        for _ in range(1, n+1):
            self.update_next_epoc_matrix_status()
            self.enter_next_epoc()
            time.sleep(time_interval)

    def play_conways_game_of_life(self, n, time_interval, alive_coordinates_list):
        self.set_initial_state(alive_coordinates_list)
        self.run_for_n_epocs(n, time_interval)

