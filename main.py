
import pygame
import random

# Ініціалізація Pygame
pygame.init()

# Розміри вікна гри
width, height = 300, 600
cell_size = 30

# Створення вікна гри
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

# Кольори
colors = [
    (0, 0, 0),
    (255, 85, 85),
    (100, 200, 115),
    (120, 108, 245),
    (255, 140, 50),
    (50, 120, 52),
    (146, 202, 73),
    (150, 161, 218),
]

# Форми фігур
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]]
]

class Tetris:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [[0] * width for _ in range(height)]
        self.gameover = False
        self.score = 0
        self.new_piece()

    def new_piece(self):
        self.piece = random.choice(shapes)
        self.piece_color = random.randint(1, len(colors) - 1)
        self.piece_x = width // cell_size // 2 - len(self.piece[0]) // 2
        self.piece_y = 0

    def rotate_piece(self):
        # Збереження поточного стану фігури для можливого відкату
        old_piece = self.piece
        self.piece = [list(row) for row in zip(*self.piece[::-1])]
        if not self.valid_space():
            self.piece = old_piece  # Відкат обертання, якщо воно недійсне

    def valid_space(self, offset_x=0, offset_y=0):
        for y, row in enumerate(self.piece):
            for x, cell in enumerate(row):
                if cell:
                    new_x = x + self.piece_x + offset_x
                    new_y = y + self.piece_y + offset_y
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return False
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return False
        return True

    def place_piece(self):
        for y, row in enumerate(self.piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[y + self.piece_y][x + self.piece_x] = self.piece_color
        self.clear_lines()
        self.new_piece()
        if not self.valid_space():
            self.gameover = True

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.board) if all(row)]
        for i in lines_to_clear:
            del self.board[i]
            self.board.insert(0, [0] * self.width)
        self.score += len(lines_to_clear)

    def draw_board(self, screen):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                pygame.draw.rect(screen, colors[cell], (x * cell_size, y * cell_size, cell_size, cell_size))
        for y, row in enumerate(self.piece):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, colors[self.piece_color], ((x + self.piece_x) * cell_size, (y + self.piece_y) * cell_size, cell_size, cell_size))

def main():
    clock = pygame.time.Clock()
    game = Tetris(height // cell_size, width // cell_size)
    fall_time = 0

    while not game.gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.gameover = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.piece_x -= 1
                    if not game.valid_space():
                        game.piece_x += 1
                if event.key == pygame.K_RIGHT:
                    game.piece_x += 1
                    if not game.valid_space():
                        game.piece_x -= 1
                if event.key == pygame.K_DOWN:
                    game.piece_y += 1
                    if not game.valid_space():
                        game.piece_y -= 1
                        game.place_piece()
                if event.key == pygame.K_UP:
                    game.rotate_piece()

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= 0.5:
            fall_time = 0
            game.piece_y += 1
            if not game.valid_space():
                game.piece_y -= 1
                game.place_piece()

        screen.fill((0, 0, 0))
        game.draw_board(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
