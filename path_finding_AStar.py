import pygame
import math
from queue import PriorityQueue
import random
import time

WIDTH = 350
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("CS361 project")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

                        # وضع الالوان
	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_obstacle(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_obstacle(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle():  # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():  # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_obstacle():  # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():  # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

		# Check for diagonal neighbors
		if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][
			self.col + 1].is_obstacle():  # DOWN-RIGHT
			self.neighbors.append(grid[self.row + 1][self.col + 1])

		if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][
			self.col + 1].is_obstacle():  # UP-RIGHT
			self.neighbors.append(grid[self.row - 1][self.col + 1])

		if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][
			self.col - 1].is_obstacle():  # DOWN-LEFT
			self.neighbors.append(grid[self.row + 1][self.col - 1])

		if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_obstacle():  # UP-LEFT
			self.neighbors.append(grid[self.row - 1][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2

	if x1 != x2 and y1 != y2:  # diagonal move
		return int(1.5 * (abs(x1 - x2) + abs(y1 - y2)))
	else:                      # horizontal/vertical move
		return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			# Calculate g_score
			if neighbor.row == current.row or neighbor.col == current.col:  # حركة افقيه او عامودية
				temp_g_score = g_score[current] + 1
			else:  # حركة قطريه
				temp_g_score = g_score[current] + math.sqrt(2)

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

# المربعات
def make_grid(rows, width, num_obstacles):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    # set the start and end spots
    start = grid[0][0]
    end = grid[-1][-1]
    start.make_start()
    end.make_end()

    # set a fixed number of obstacles
    obstacle_spots = random.sample([spot for row in grid for spot in row if not (spot.is_start() or spot.is_end())], num_obstacles)
    for spot in obstacle_spots:
        spot.make_obstacle()

    return grid


                          # شكل الصفحة
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

# استجابة النقر
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

                      #شكل الصفحة
def main(win, width):
	ROWS = 10                          #عدد المربعات
	grid = make_grid(ROWS, width,20)   # عدد الحواجز

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

            # اليسار
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end: # اختيار مكان البداية
					start = spot
					start.make_start()

				elif not end and spot != start: #اختيار مكان النهاية
					end = spot
					end.make_end()

				# elif spot != end and spot != start: #اختيار اماكن الحواجز
				# 	spot.make_obstacle()

            # اليمين
			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					# حساب وقت عملية البحث
					start_time = time.time()
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
					end_time = time.time()
					elapsed_time = end_time - start_time

					print("Time: ", elapsed_time)
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()



main(WIN, WIDTH)