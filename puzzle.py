import pygame
import sys
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class SlidePuzzle:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.tile_size = 300 // self.grid_size
        self.tiles = [[i + j * grid_size for i in range(grid_size)] for j in range(grid_size)]
        self.empty_tile = [grid_size - 1, grid_size - 1]
        self.shuffle()

    def shuffle(self, moves=1000):
        for _ in range(moves):
            self.perform_random_move()

    def perform_random_move(self):
        possible_moves = self.get_possible_moves()
        move = random.choice(possible_moves)
        self.swap_tiles(move)

    def get_possible_moves(self):
        moves = []
        x, y = self.empty_tile

        if x > 0:
            moves.append((x - 1, y))  
        if x < self.grid_size - 1:
            moves.append((x + 1, y))  
        if y > 0:
            moves.append((x, y - 1))  
        if y < self.grid_size - 1:
            moves.append((x, y + 1))  

        return moves

    def swap_tiles(self, move):
        x, y = move
        self.tiles[self.empty_tile[0]][self.empty_tile[1]], self.tiles[x][y] = (
            self.tiles[x][y],
            self.tiles[self.empty_tile[0]][self.empty_tile[1]],
        )
        self.empty_tile = [x, y]

    def is_solved(self):
        return all(self.tiles[i][j] == i + j * self.grid_size for i in range(self.grid_size) for j in range(self.grid_size))

    def draw(self, screen):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                tile_value = self.tiles[row][col]
                if tile_value != 0:
                    pygame.draw.rect(
                        screen,
                        WHITE,
                        (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size),
                    )
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(tile_value), True, BLACK)
                    screen.blit(
                        text,
                        (
                            col * self.tile_size + self.tile_size // 2 - text.get_width() // 2,
                            row * self.tile_size + self.tile_size // 2 - text.get_height() // 2,
                        ),
                    )

def get_grid_size_input(screen):
    input_text = ""
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    input_rect = pygame.Rect(150, 150, 200, 36)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
    text = ''
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            size = int(text)
                            if size > 1:
                                return size
                            else:
                                text = ''
                        except ValueError:
                            text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        width = max(200, font.size(input_text + text)[0]+10)
        input_rect.w = width
        pygame.draw.rect(screen, color, input_rect, 2)
        pygame.draw.rect(screen, color, input_rect)
        txt_surface = font.render(input_text + text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_rect.w = width
        screen.blit(txt_surface, (input_rect.x+5, input_rect.y+5))
        pygame.display.flip()
        clock.tick(30)

def main():
    screen_size = 300
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("Slide Puzzle")

    valid_input = False
    while not valid_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    valid_input = True

        try:
            grid_size = int(input("Entrez la taille du plateau (par exemple, 3 pour un plateau 3x3) : "))
            if grid_size > 1:
                valid_input = True
            else:
                print("La taille du plateau doit être supérieure à 1.")
        except ValueError:
            print("Veuillez entrer un nombre entier.")

    puzzle = SlidePuzzle(grid_size)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if puzzle.empty_tile[0] < grid_size - 1:
                        puzzle.swap_tiles((puzzle.empty_tile[0] + 1, puzzle.empty_tile[1]))
                elif event.key == pygame.K_DOWN:
                    if puzzle.empty_tile[0] > 0:
                        puzzle.swap_tiles((puzzle.empty_tile[0] - 1, puzzle.empty_tile[1]))
                elif event.key == pygame.K_LEFT:
                    if puzzle.empty_tile[1] < grid_size - 1:
                        puzzle.swap_tiles((puzzle.empty_tile[0], puzzle.empty_tile[1] + 1))
                elif event.key == pygame.K_RIGHT:
                    if puzzle.empty_tile[1] > 0:
                        puzzle.swap_tiles((puzzle.empty_tile[0], puzzle.empty_tile[1] - 1))

        screen.fill(BLACK)

        puzzle.draw(screen)

        if puzzle.is_solved():
            font = pygame.font.Font(None, 50)
            text = font.render("Félicitations ! Vous avez résolu le puzzle.", True, WHITE)
            screen.blit(text, (10, screen_size // 2 - 25))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()
