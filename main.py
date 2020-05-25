import click

from game_of_life import game_of_life


@click.command()
@click.option('--x_lim', default=9, help='Length of x-axis.')
@click.option('--y_lim', default=9, help='Length of y-axis.')
@click.option('--num_epocs', default=15, help='Number of epocs for Conway\'s game of life.')
@click.option('--alive_coordinates', default=[(1, 2), (0, 3), (1, 4), (2, 3)], help='List of coordinate tuples of initial alive points.')
def main(x_lim, y_lim, num_epocs, alive_coordinates):
    interface = game_of_life.Interface(x_lim, y_lim)
    interface.play_conways_game_of_life(num_epocs, alive_coordinates)


if __name__ == '__main__':
    main()