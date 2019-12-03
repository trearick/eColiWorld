from random import randint
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as ani
import numpy as np


class World:
	"""
	This class defines a world that contains 1) a landscape containing varying concentrations of food,
	2) eColi that move on that landscape, 3) time that advances with each call to ticktock(), 4) a
	way to visualize eColi on the landscape
	"""
	POPULATION_SIZE = 1000
	WORLD_SPAN = 600

	def __init__(self):
		# create the landscape and dump food on two locations
		self.landscape = np.zeros([self.WORLD_SPAN, self.WORLD_SPAN])
		self.landscape[200, 200] = 7000000
		self.landscape[400, 400] = 5000000
		# spread the food around so the germs can find the highest concentration
		self.landscape = gaussian_filter(self.landscape, (100, 100))
		self.population = []
		self.animation = []
		self.fig, self.ax = plt.subplots()
		self.ax.axis('off')
		# create germs with random locations
		self.nrows, self.ncols = self.landscape.shape
		for i in range(self.POPULATION_SIZE):
			c = randint(0, self.ncols - 1)
			r = randint(0, self.nrows - 1)
			self.population.append(eColi(self, i, r, c))  # create individual E coli bacteria at random locations

	def ticktock(self):
		for germ in self.population:
			germ.sense_respond()

	def gods_eye_view(self):
		view = self.landscape.copy()
		for germ in self.population:
			view[germ.c, germ.r] = 255
		im = self.ax.imshow(view, animated=True, cmap=cm.CMRmap)
		self.animation.append([im])


class eColi:
	"""
	This class defines a single eColi organism. Each organism can sense concentration of food and compare it to a
	prior concentration. If concentration is increasing, the eColi continues in the same direction. Otherwise, it
	tumbles and resumes in a different direction.
	"""
	TRAVEL_MULTIPLIER = 2
	DIRECTIONS = {  # this dictionary is used because python lacks a switch/case statement
		0: (-1, 0),  # North
		1: (-1, 1),  # NE
		2: (0, 1),  # East
		3: (1, 1),  # SE
		4: (1, 0),  # South
		5: (1, -1),  # SW
		6: (1, -1),  # West
		7: (-1, -1)}  # NW

	def __init__(self, world, count, row, column):
		self.r = row
		self.c = column
		self.count = count
		self.world = world
		self.direction = randint(0, 7)  # starts with a random direction
		self.concentration = 0

	def sense_respond(self):
		self.r += self.TRAVEL_MULTIPLIER * eColi.DIRECTIONS[self.direction][0]
		self.c += self.TRAVEL_MULTIPLIER * eColi.DIRECTIONS[self.direction][1]
		self.c = self.c % self.world.ncols		# eColi cannot fall off
		self.r = self.r % self.world.nrows		# because the world is not flat!
		conc_now = self.world.landscape[self.c, self.r]
		if conc_now <= self.concentration:
			self.direction = randint(0, 7)					# Change direction
		self.concentration = self.world.landscape[self.c, self.r]


# Main program
W = World()						# Create the world
TIME_STEPS = 400
for j in range(TIME_STEPS):		# Iterate over time and view results
	W.ticktock()
	W.gods_eye_view()

ani = ani.ArtistAnimation(W.fig, W.animation, interval=10, repeat=True, blit=True)
# To save the animation to a movie, uncomment the next line
#ani.save("c:\movie.mp4")
plt.show()
