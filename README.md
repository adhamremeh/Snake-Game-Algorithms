
# Clever Snake

A simple Snake game with a clever snake that uses various algorithms to find the best path to the apple. You can choose between different algorithms to control the snake's movement.

## Getting Started

Make sure you have Python and Pygame installed.

### Prerequisites

You need to have Python and Pygame installed. You can install Pygame using pip:

```
pip install pygame
```

### Usage

Run the `main.py` script to start the game. Use the following keys to interact with the game:

- Arrow keys: Control the snake's movement.
- `1`: Choose the BFS algorithm.
- `2`: Choose the A* algorithm.
- `3`: Choose the Hamiltonian Cycle algorithm.
- `4`: Choose the DFS algorithm.
- `r`: Restart the game.
- `UP`: Increase the game speed.
- `DOWN`: Decrease the game speed.
- `g`: End the game.

### Game Rules

1. The snake starts in the top-left corner of the screen.
2. The snake's goal is to eat the red apples that appear randomly on the screen.
3. You can choose from different algorithms to control the snake's movement to reach the apple.
4. The snake will find the best path to the apple using the selected algorithm.
5. If the snake grows to the size of the grid, you win the game.
6. If the snake collides with the game boundaries or itself, you lose the game.

