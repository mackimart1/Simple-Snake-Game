# Improved Snake Game Implementation with fixes and optimizations.

import pygame
import sys
import random
import logging
import os

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Pygame
pygame.init()

class SnakeGame:
    """
    The Snake game implementation.

    Args:
    grid_size (int): The size of the grid. Defaults to 20.
    """

    def __init__(self, grid_size=20):
        self.grid_size = grid_size
        self.width, self.height = grid_size * 20, grid_size * 20  # Window size
        self.black, self.white, self.red = (0, 0, 0), (255, 255, 255), (255, 0, 0)  # Colors
        self.snake_start_length = 5  # Initial length of the snake
        self.fps = 10  # Frames per second
        self.snake_skin = pygame.Surface((20, 20))
        self.snake_skin.fill(self.white)
        self.food_skin = pygame.Surface((20, 20))
        self.food_skin.fill(self.red)
        self.snake = [(self.width // 2, self.height // 2) for _ in range(self.snake_start_length)]
        self.direction = (1, 0)  # Start moving to the right
        self.food = self.get_random_food_position()

    def display_game(self):
        """
        Display the Snake game.
        """
        # Set up the display
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        clock = pygame.time.Clock()

        # Game loop
        while True:
            # Get keyboard input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event.key)

            # Update snake body
            self.update_snake()

            # Check for collisions
            if self.check_collision():
                logger.error("Game Over!")
                pygame.quit()
                sys.exit()

            # Draw everything
            screen.fill(self.black)
            for pos in self.snake:
                screen.blit(self.snake_skin, pos)
            screen.blit(self.food_skin, self.food)
            pygame.display.update()

            clock.tick(self.fps)

    def get_random_food_position(self):
        """
        Get a random food position.

        Returns:
        tuple: A random food position.
        """
        return (random.randint(0, self.grid_size - 1) * 20, random.randint(0, self.grid_size - 1) * 20)

    def handle_keydown(self, key):
        """
        Handle keydown events.

        Args:
        key: The key pressed.
        """
        if key == pygame.K_UP and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == pygame.K_DOWN and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key == pygame.K_LEFT and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == pygame.K_RIGHT and self.direction != (-1, 0):
            self.direction = (1, 0)

    def update_snake(self):
        """
        Update the snake body.
        """
        new_head = (self.snake[0][0] + self.direction[0] * 20, self.snake[0][1] + self.direction[1] * 20)
        self.snake.insert(0, new_head)

        if self.snake[0] == self.food:
            self.food = self.get_random_food_position()
        else:
            self.snake.pop()

    def check_collision(self):
        """
        Check for collisions with the wall or itself.

        Returns:
        bool: True if a collision occurred, False otherwise.
        """
        if (self.snake[0][0] < 0 or self.snake[0][0] >= self.width or
            self.snake[0][1] < 0 or self.snake[0][1] >= self.height or
            self.snake[0] in self.snake[1:]):
            return True
        return False

if __name__ == "__main__":
    if not os.path.exists('logs'):
        os.makedirs('logs')
    game = SnakeGame(20)
    game.display_game()