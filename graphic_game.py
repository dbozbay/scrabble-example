import pygame
import json
from board import Move, ScrabbleBoard

pygame.font.init()
TILEWIDTH = 600 / 15


def coord_to_px(coords: tuple[int, int]) -> tuple[int, int]:
    return tuple([int((TILEWIDTH) * coord) for coord in coords])


class ScrabbleSurface(pygame.Surface):
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((600, 800))
        self.fill("green")
        self.bg_image = pygame.image.load("images/scrabble_board_img.jpg")

    def populate_with_coords(self):
        for i in range(15):
            for j in range(15):
                coord_value = (i, j)
                px_value = coord_to_px(coord_value)
                pygame.draw.circle(self, (255, 0, 0), px_value, 10)

    def add_bg(self):
        self.blit(self.bg_image, (0, 0))

    def add_tile(self, pos: tuple[int, int]):
        """
        Adding the white scrabble tile to the point.
        """
        pygame.draw.rect(self, (255, 255, 255), (pos[0], pos[1], 40, 40))

    def add_letter(self, pos: tuple[int, int], letter: str):

        my_font = pygame.font.SysFont("Calibri", 36, bold=True)
        text_surface = my_font.render(letter, False, (0, 0, 0))
        letter_pos = (pos[0] + TILEWIDTH / 5, pos[1])
        self.blit(text_surface, letter_pos)

    def add_scrabble_tile(self, pos: tuple[int, int], letter: str):
        self.add_tile(pos)
        self.add_letter(pos, letter)

    def add_letters_from_board(
        self,
        board: ScrabbleBoard,
    ):
        for i, row in enumerate(board.board):
            for j, letter in enumerate(row):
                current_coord = (i, j)
                if not letter.isdigit():
                    self.add_scrabble_tile(current_coord, letter)


# Setting game window dimensions
game_display = ScrabbleSurface()
# bg_image = pygame.transform.scale(bg_image, (1, 1))
# Main game loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Drawing image at position (0,0)
    game_display.add_bg()

    game_display.populate_with_coords()
    game_display.add_tile(coord_to_px((0, 0)))
    game_display.add_letter(coord_to_px((0, 0)), "A")
    pygame.display.flip()
pygame.quit()
