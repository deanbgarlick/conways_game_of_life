import time


class Cell:

    def __init__(self, x, y, x_lim, y_lim):

        self.x = x
        self.y = y
        self.status = 'dead'
        self.adjacent_cells_list = self._get_adjacent_cells_list(x_lim, y_lim)
        self.next_status = ''

    def _get_adjacent_cells_list(self, x_lim, y_lim):
        adjacent_cells_list = []
        for x_increment in [-1, 0, 1]:
            for y_increment in [-1, 0, 1]:
                if x_increment !=0  or y_increment !=0:
                    if (self.x + x_increment < x_lim) and (self.x + x_increment > 0):
                        if (self.y + y_increment < y_lim) and (self.y + y_increment > 0):
                            adjacent_cells_list.append((self.x + x_increment, self.y + y_increment))
        return adjacent_cells_list


class Matrix:

    def __init__(self, x_lim, y_lim):

        self.x_lim = x_lim
        self.y_lim = y_lim
        self.cell_grid = [[Cell(x, y, x_lim, y_lim) for y in range(y_lim)] for x in range(y_lim)]

    def get_cell_from_coordinate(self, cell_coordinate):
        return self.cell_grid[cell_coordinate[0]][cell_coordinate[1]]

    def check_status_of_cell(self, cell_coordinate):
        return self.get_cell_from_coordinate(cell_coordinate).status

    def count_alive_adjacent_cells(self, cell_coordinate):
        count = 0
        for cell_coordinate in self.get_cell_from_coordinate(cell_coordinate).adjacent_cells_list:
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
                self.count_alive_adjacent_cells(cell_coordinate) < 2
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


class Interface:

    def __init__(self, x_lim, y_lim):
        self.view = View()
        self.matrix = Matrix(x_lim, y_lim)

    def change_matrix(self, x_lim, y_lim):
        self.matrix = Matrix(x_lim, y_lim)

    def change_view(self, alive_token=None, dead_token=None):
        self.view.set_display_tokens(alive_token, dead_token)

    def play_conways_game_of_life(self, n_epocs, alive_coordinates_list, time_interval=4):
        self.matrix.set_initial_state(alive_coordinates_list)
        self.view.print_matrix_state(self.matrix, 0)
        for epoc in range(1, n_epocs+1):
            self.matrix.run_for_n_epocs(1, time_interval)
            self.view.print_matrix_state(self.matrix, epoc)


class View:

    def __init__(self, alive_token='X', dead_token='O'):
        self.display_token_dict = {'alive': alive_token, 'dead': dead_token}

    def set_display_tokens(self, alive_token, dead_token):
        self.display_token_dict = {'alive': alive_token, 'dead': dead_token}

    def print_matrix_state(self, matrix, epoc):
        top_row = ['|'+str(n) for n, _ in enumerate(matrix.cell_grid[0])]
        top_row = ''.join(top_row)
        top_row = '-' + top_row + '|'
        row_divider = '|-'*len(matrix.cell_grid[0]) + '|'
        print('\n\n\n Epoc: '+str(epoc) + '\n')
        print(top_row)
        print('-'+row_divider)
        for rowno, cell_row in enumerate(matrix.cell_grid):
            cell_row_view = ['|'+str(self.display_token_dict[cell.status]) for cell in cell_row]
            cell_row_view = ''.join(cell_row_view) + '|'
            print(str(rowno) + cell_row_view)
            print('-'+row_divider)
