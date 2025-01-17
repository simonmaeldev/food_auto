# Food Auto

A batch cooking helper that generates grocery lists and cooking instructions from recipes.

## Prerequisites

- Python 3.x
- fzf (fuzzy finder) must be installed on your system

### Installing fzf

- **macOS** (using Homebrew):
  ```bash
  brew install fzf
  ```

- **Linux** (Debian/Ubuntu):
  ```bash
  sudo apt install fzf
  ```

- **Other systems**: See [fzf installation guide](https://github.com/junegunn/fzf#installation)

## Usage

Run the program using:

```bash
uv run python food_auto/main.py
```

By default, it looks for recipes in a `recipes` directory. You can specify a different path:

```bash
uv run python food_auto/main.py --path /path/to/recipes
```

### Interactive Selection

- Use arrow keys to navigate recipes
- Press Tab to select recipes
- Press Enter to validate
- Type to filter recipes
- Select "generate" option when done to create output files
- Press Esc to quit

### Output

The program generates two files in the `output` directory:
- A grocery list (`groceries_YYYY-MM-DD.md`)
- Cooking instructions (`instructions_YYYY-MM-DD.md`)

### Ideas to go further

code recette -> llm qui extrait ingrédients solides (en dehors des épices) -> fais une requete à une [bdd](https://www.nutritionix.com/) pour récup les macros, multiplie par qtt -> permet d'avoir les macros pour une recette
