# Implementation of John Conway's famous "Game of Life" celular automata algorithm
# See here for sample starting configurations: http://www.radicaleye.com/lifepage/picgloss/picgloss.html

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
import numpy as np
import sys

class Universe:

    def __init__(self, starting_configuration, geometry, fig):

        self.geometry = geometry
        self.configuration = {index: Cell(index, lambda x: self.geometry.neighbours(x), value=1)
                             for index in starting_configuration}

        if fig is not None:
            self.geometry.init_plot_data()
            self.plot_canvas = fig.gca().imshow(self.geometry.plot_data, vmin=0, vmax=1, animated=True, cmap='Greys')#'gist_gray'
            self.geometry.update_plot_data(self.configuration)
            self.plot_canvas.set_data(self.geometry.plot_data)
        else:
            self.plot_canvas = None
        
    def update(self):
        populated_indexes = list(self.configuration.keys())
        for index in populated_indexes:
            self.configuration[index].update_adjacent(self.configuration)
        for index in self.configuration:
            self.configuration[index].update_value()

        if self.plot_canvas is not None:
            self.geometry.update_plot_data(self.configuration)
            self.plot_canvas.set_data(self.geometry.plot_data)
    
    def purge(self):
        populated_indexes = list(self.configuration.keys())
        for index in populated_indexes:
            if self.configuration[index].ready_to_purge():
                del self.configuration[index]
        print(len(self.configuration))

    def is_empty(self):
        return len(self.configuration) == 0


class Cell:

    def __init__(self, index, neighbours, value=0):
        self.did_update_neighbours_sum = False
        self.value = value
        self.delta_value = value
        self.neighbours_sum = 0
        self.neighbours = neighbours
        self.neighbours_at = self.neighbours(index)

    def update_neighbours_sum(self, other_value):
        if other_value != 0:
            self.did_update_neighbours_sum = True
            self.neighbours_sum += other_value

    def update_value(self):
        # main rules implemented here
        if self.did_update_neighbours_sum:
            old_value = self.value
            if self.neighbours_sum==2:
                self.value = self.value & 1
            elif self.neighbours_sum==3:
                self.value = 1
            else: 
                self.value = 0
            self.delta_value = self.value - old_value
            self.did_update_neighbours_sum = False

    def update_adjacent(self, configuration):
        self.did_update_neighbours_sum = True
        if self.delta_value != 0:
            for index in self.neighbours_at:
                if not index in configuration.keys():
                    configuration[index] = Cell(index, self.neighbours, value=0)
                configuration[index].update_neighbours_sum(self.delta_value)

    def ready_to_purge(self):
        return self.value==0 and self.neighbours_sum==0 and self.delta_value==0


class RectangularTorus:

    def __init__(self, dimension, dimension1=None):
        self.dimension = dimension

        if dimension1 is None:
            self.dimension1 = dimension
        else:
            self.dimension1 = dimension1

        self.plot_data = None

    def neighbours(self, origin):
        return set([(i % self.dimension, j % self.dimension1) 
                    for i in range(origin[0]-1, origin[0]+2)
                    for j in range(origin[1]-1, origin[1]+2) 
                    if not (i==origin[0] and j==origin[1])])

    def init_plot_data(self):
        self.plot_data = np.zeros((self.dimension, self.dimension1))

    def update_plot_data(self, configuration):
        for point in configuration.keys():
            self.plot_data[point] = configuration[point].value
          
            
class Rectangle:

    def __init__(self, dimension, dimension1=None):
        self.dimension = dimension

        if dimension1 is None:
            self.dimension1 = dimension
        else:
            self.dimension1 = dimension1

        self.plot_data = None

    def neighbours(self, origin):
        return set([(i, j) 
                    for i in range(origin[0]-1, origin[0]+2)
                    for j in range(origin[1]-1, origin[1]+2) 
                    if (not (i==origin[0] and j==origin[1])) and i>=0 and j>=0 and i<self.dimension and j<self.dimension1])

    def init_plot_data(self):
        self.plot_data = np.zeros((self.dimension, self.dimension1))

    def update_plot_data(self, configuration):
        for point in configuration.keys():
            self.plot_data[point] = configuration[point].value


if __name__ == "__main__":

    fig = plt.figure()

    # Blinker
    # geometry = RectangularTorus(5)
    # starting_configuration = [(1, 1), (1, 2), (1, 3)]

    # Toad
    # geometry = RectangularTorus(6)
    # starting_configuration = [(2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3)]

    # Beacon
    # geometry = RectangularTorus(6)
    # starting_configuration = [(1, 1), (1, 2), (2, 1), (4, 3), (4, 4), (3, 4)]

    # Pulsar
    # geometry = RectangularTorus(17)
    # starting_configuration = [(2, 4), (2, 5), (2, 6), (2, 10), (2, 11), (2, 12), 
    #                           (4, 2), (5, 2), (6, 2), (4, 7), (5, 7), (6, 7), 
    #                           (4, 9), (5, 9), (6, 9), (4, 14), (5, 14), (6, 14), 
    #                           (7, 4), (7, 5), (7, 6), (7, 10), (7, 11), (7, 12), 
    #                           (9, 4), (9, 5), (9, 6), (9, 10), (9, 11), (9, 12), 
    #                           (10, 2), (11, 2), (12, 2), (10, 7), (11, 7), (12, 7), 
    #                           (10, 9), (11, 9), (12, 9), (10, 14), (11, 14), (12, 14), 
    #                           (14, 4), (14, 5), (14, 6), (14, 10), (14, 11), (14, 12)]

    # Penta-decathalon
    # geometry = RectangularTorus(11, 19)
    # starting_configuration = [()]

    # Glider
    # geometry = RectangularTorus(10)
    # geometry = Rectangle(10)
    # starting_configuration = [(2, 1), (3, 2), (3, 3), (2, 3), (1, 3)]
    # animation_path = r'C:\Users\Simon\Work\VisualStudioProjects\Game_of_Life_demo\Game_of_Life_demo\animations\rectangle_glider.mp4'

    # Gosper's Glider gun
    # animation_path = r'C:\Users\Simon\Work\VisualStudioProjects\Game_of_Life_demo\Game_of_Life_demo\animations\gosper_80_160.mp4'
    # geometry = RectangularTorus(80, 160)
    # starting_configuration = [(5, 1), (5, 2), (6, 1), (6, 2), 
    #                           (5, 11), (6, 11), (7, 11), (4, 12), (8, 12), 
    #                           (3, 13), (9, 13), (3, 14), (9, 14), (6, 15), 
    #                           (4, 16), (8, 16), (5, 17), (6, 17), (7, 17), 
    #                           (6, 18), 
    #                           (3, 21), (4, 21), (5, 21), (3, 22), (4, 22), 
    #                           (5, 22), (2, 23), (6, 23), 
    #                           (1, 25), (2, 25), (6, 25), (7, 25),
    #                           (3, 36), (4, 36), (3, 35), (4, 35)]

    # Puffer that creates gliding guns 
    # (taken from here https://commons.wikimedia.org/wiki/File:Conways_game_of_life_breeder.png)
    img = np.array(mpimg.imread( r'C:\Users\Simon\Work\VisualStudioProjects\Game_of_Life_demo\Game_of_Life_demo\input_configurations\Conways_game_of_life_breeder.png'))
    starting_configuration = [(point[0], point[1]) for point in np.argwhere(img==0.8117647) if point[2]==0]
    min_y = min([point[1] for point in starting_configuration])
    starting_configuration = [(point[0]+50, point[1] - min_y) for point in starting_configuration]
    min_dimensions = img.shape
    geometry = Rectangle(250, 1000)
    animation_path = r'C:\Users\Simon\Work\VisualStudioProjects\Game_of_Life_demo\Game_of_Life_demo\animations\gliding_gun_breeder.mp4'

    game = Universe(starting_configuration=starting_configuration, geometry=geometry, fig=fig)

    def animate(i):
        game.update()
        game.purge()
        return game.plot_canvas

    ani = animation.FuncAnimation(fig, animate, interval=10, blit=False, repeat=False, frames=2000)
    ani.save(animation_path)

    sys.exit(0)
   