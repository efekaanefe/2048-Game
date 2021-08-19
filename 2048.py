import pygame
import sys, os
import numpy as np
import pygame.font

pygame.init()
pygame.font.init()

NUMBER_FONT = pygame.font.SysFont('Clear Sans', 40)
GAMEOVER_FONT = pygame.font.SysFont('Comicsans', 50)

WIDTH, HEIGHT = 400, 400

DIMENSION = 4
SQ_SIZE = WIDTH//DIMENSION

COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 219),
    4: (240, 226, 202),
    8: (242, 177, 121),
    16: (236, 141, 85),
    32: (250, 123, 92),
    64: (234, 90, 56),
    128: (237, 207, 114),
    256: (242, 208, 75),
    512: (237, 200, 80),
    1024: (227, 186, 19),
    2048: (236, 196, 2),
    4096: (96, 217, 146)}

BG_COLOR = (205, 193, 180)
LINE_COLOR = (187, 173, 160)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
DARK_VALUE = (101, 90, 85)
LIGHT_VALUE = WHITE


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
WIN.fill(BG_COLOR)

class Board_2048:
	def __init__(self):
		self.score = 0
		self.board_log = []
		self.rotation_amounts  = {
								"left" : 0,
								"right":2,
								"up":1,
								"down":3
								}

		self.board = np.array([[0 for _ in range(DIMENSION)] for _ in range(DIMENSION)])

		self.place_2(2)

	def place_2(self, times = 1):
		try:
			for _ in range(times):
				empty_coordinates = np.argwhere(self.board == 0)
				random_row = np.random.choice(empty_coordinates.shape[0], replace = False)
				i, j = empty_coordinates[random_row]
				self.board[i][j] = 2
		except Exception:
			self.gameover()

	def move(self, direction, checking_for_possible_moves = False):

		first_board = np.copy(self.board) 

		self.board = np.rot90(self.board, (self.rotation_amounts[direction]))

		def slide(row):
			new_row = []
			for i in range(0,DIMENSION):
				value = row[i]
				if value != 0:
					new_row.append(value)
			length = len(new_row)
			zero_needed = DIMENSION - length
			for _ in range(zero_needed):
				new_row.append(0)
			return np.array(new_row)

		def combine(row):
			combined_indexs = []
			for i in range(1, DIMENSION):
				if row[i] != 0:
					if row[i-1] == row[i]:
						row[i-1] *= 2
						row[i] = 0
						if not checking_for_possible_moves:
							self.score += row[i-1]
			return row

		for i in range(DIMENSION):
			row = self.board[i]
			row = slide(row)
			row = combine(row)
			row = slide(row)
			self.board[i] = row

		self.board = np.rot90(self.board, (4-self.rotation_amounts[direction]))

		if not np.array_equal(first_board, self.board):
			if not checking_for_possible_moves:
				self.place_2()
			else:
				self.board = first_board
			return True
		return False

	def draw(self):

		def draw_grid():
			for x in range(0,WIDTH, SQ_SIZE-1):
				pygame.draw.line(WIN, color=LINE_COLOR,start_pos=(x, 0), end_pos=(x, HEIGHT), width = 12)
				y = x
				pygame.draw.line(WIN, color=LINE_COLOR,start_pos=(0, y), end_pos=(WIDTH, y), width = 12)

		def draw_board():
			for i in range(DIMENSION):
				for j in range(DIMENSION):
					value = self.board[i][j]
					x = j*SQ_SIZE
					y = i*SQ_SIZE
					bg_color = COLORS[value]
					value_color = DARK_VALUE if value <= 4 else LIGHT_VALUE
					surface = pygame.Surface((SQ_SIZE-1, SQ_SIZE-1))
					surface.fill(color = bg_color)
					text = NUMBER_FONT.render(str(value), True, value_color)
					surface.blit(text, (SQ_SIZE//2-text.get_width()//2, SQ_SIZE//2-text.get_height()//2))
					WIN.blit(surface, (x, y))

		draw_board()
		draw_grid()

	def check_for_possible_move(self):
		conditions = []
		directions = ["left", "right", "up", "down"]
		for direction in directions:
			conditions.append(self.move(direction, checking_for_possible_moves = True))
		if True not in conditions:
			return False
		else: return True

	def check_for_win(self):
		if 1 == np.count_nonzero(self.board == 4096):
			text = GAMEOVER_FONT.render("You Won!!", True, BLACK)
			WIN.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2-text.get_height()//2-75))
			text = GAMEOVER_FONT.render(f"Score: {self.score}", True, BLACK)
			WIN.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2-text.get_height()//2+0))
			text = GAMEOVER_FONT.render("Press R to restart", True, BLACK)
			WIN.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2-text.get_height()//2+75))

	def gameover(self):
		text = GAMEOVER_FONT.render("Gameover!!!", True, BLACK)
		WIN.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2-text.get_height()//2-75))
		text = GAMEOVER_FONT.render(f"Score: {self.score}", True, BLACK)
		WIN.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2-text.get_height()//2+0))
		text = GAMEOVER_FONT.render("Press R to restart", True, BLACK)
		WIN.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2-text.get_height()//2+75))

def main():
	run = True
	clock = pygame.time.Clock()
	board = Board_2048()
	while run:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False; sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					run = False
					main()
					break

				if event.key == pygame.K_ESCAPE:
					run = False; sys.exit()
				
				if event.key == pygame.K_LEFT:
					board.move("left")

				if event.key == pygame.K_RIGHT:
					board.move("right")
				
				if event.key == pygame.K_UP:
					board.move("up")
				
				if event.key == pygame.K_DOWN:
					board.move("down")

		board.draw()
		if 0 == np.count_nonzero(board.board == 0):
			if not board.check_for_possible_move():
				board.gameover()
		board.check_for_win()
		pygame.display.update()

if __name__ == '__main__':
	main()