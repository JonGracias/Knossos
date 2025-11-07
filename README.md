# 🏛️ Knossos

**Knossos** is a classic-style labyrinth adventure written in **Python** using **Pygame**.
Step into the sandals of **Theseus** as you navigate the twisting corridors of the Labyrinth, **evade the Minotaur**, and uncover the secrets buried deep beneath Crete.

This project began as a **college-level final** exploring **maze generation algorithms** and evolved into a stylized game experiment mixing mythology, logic, and procedural design.

---

## ⚙️ Features

* **Dynamic Maze Generation** – Built using a **Depth-First Search (FILO)** algorithm for fresh labyrinths every run.
* **Retro Gameplay Loop** – Simple movement, collectible items, and enemy AI inspired by early dungeon crawlers.
* **Myth-Inspired Narrative** – Based on the tale of Theseus, Ariadne, and the Minotaur.
* **Pygame-Powered Graphics** – 2D rendering with animated sprites, tile-based collision, and event handling.
* **Win/Loss Conditions** – Escape the labyrinth or fall to the beast.

---

## 🧠 Gameplay Overview

* **Goal:** Find your way through the labyrinth, retrieve the **golden thread**, and face the **Minotaur**.
* **Controls:**

  * `↑`, `↓`, `←`, `→` — Move
  * `Esc` — Quit
* **Objective:** Survive, solve, and escape.
* **Hint:** Some walls may not be as solid as they seem…

---

## 🧩 Maze Generation

The labyrinth is built using a **recursive backtracking algorithm** that ensures a single, connected maze with no isolated chambers.
Each cell uses a stack-based **First-In, Last-Out (FILO)** traversal to carve unique paths — balancing randomness with structure.

```python
def generate_maze(grid):
    stack = []
    current = start_cell
    current.visited = True
    
    while True:
        next_cell = current.get_unvisited_neighbor()
        if next_cell:
            stack.append(current)
            remove_wall(current, next_cell)
            current = next_cell
            current.visited = True
        elif stack:
            current = stack.pop()
        else:
            break
```

---

## 🧰 Installation

### Prerequisites

* Python 3.8 or later
* Pygame library

### Setup

```bash
# Clone the repository
git clone https://github.com/JonGracias/knossos.git
cd knossos

# Install dependencies
pip install pygame

# Run the game
python main.py
```

---

## 🖼️ Screenshots

*(Add your screenshots here once available)*

| Maze Generation                         | Gameplay                                | Encounter                                     |
| --------------------------------------- | --------------------------------------- | --------------------------------------------- |
| ![Maze](resources/screenshots/maze.png) | ![Play](resources/screenshots/game.png) | ![Minotaur](resources/screenshots/battle.png) |

---

## 🏗️ Project Structure

```
knossos/
│
├── main.py                  # Entry point
├── maze.py                  # Maze generation logic
├── player.py                # Theseus character logic
├── minotaur.py              # Enemy AI
├── assets/                  # Sprites, sound, and tile graphics
└── README.md
```

---

## 🎓 Academic Note

Originally created as part of a **Computer Science project**, *Knossos* demonstrates practical use of recursion, stack-based algorithms, and Pygame event systems.
The codebase is commented for educational clarity and ideal for beginners studying **procedural content generation**.

---

## ⚔️ Future Plans

* Add sound effects and ambient music
* Implement scoring and time-based challenges
* Create an “Ariadne mode” with AI companion pathfinding
* Port to web using **Pyodide** or **Pygbag**

---

## 🧙 Author

**Jon Gracias Perez**
Solo Developer | Storyteller | Game Designer
[GitHub](https://github.com/JonGracias)

---

