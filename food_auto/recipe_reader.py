import re
from datetime import timedelta
from pathlib import Path
from typing import List

from food_auto.datatypes import Ingredient, Macros, Recipe


def load_ingredient(line: str) -> Ingredient:
    """Parse an ingredient line from markdown format to Ingredient object"""
    # Remove checkbox
    line = line.replace("- [ ] ", "").strip()

    # If no colon, return just the name
    if ":" not in line:
        return Ingredient(name=line)

    # Split into quantity/unit part and name part
    qty_part, name_part = line.split(":", 1)

    # Parse name and url
    name = name_part.strip()
    url = None
    if "[" in name and "]" in name:
        match = re.search(r"\[(.*?)\]\((.*?)\)(.*)", name)
        if match:
            name = match.group(1) + (match.group(3) or "")
            url = match.group(2)
            name = name.strip()

    # Parse quantity and unit
    qty_part = qty_part.strip()
    quantity = None
    unit = None

    # Try to extract number and unit
    number_match = re.search(r"^(\d+(?:\.\d+)?)\s*(.*)", qty_part)
    if number_match:
        quantity = float(number_match.group(1))
        unit = number_match.group(2).strip() or None

    return Ingredient(name=name, url=url, quantity=quantity, unit=unit)


def load_recipes(path_dir: str) -> List[Recipe]:
    """Load all recipes from markdown files in the given directory"""
    recipes = []
    path = Path(path_dir)

    # Check if directory exists
    if not path.exists():
        raise FileNotFoundError(f"Recipe directory does not exist: {path_dir}")

    # Get all markdown files
    recipe_files = list(path.rglob("*.md"))

    # Check if directory contains any markdown files
    if not recipe_files:
        raise ValueError(f"No markdown files found in recipe directory: {path_dir}")

    for recipe_file in recipe_files:
        try:
            current_section = None
            ingredients = []
            ustensiles = []
            instructions = []
            recipe_data = {"kcal": 0, "proteins": 0, "carbs": 0, "fat": 0}

            with open(recipe_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Parse headers
                if line.startswith("# "):
                    recipe_data["name"] = line[2:].strip()
                elif line.startswith("- nb portions :"):
                    recipe_data["nb_portions"] = int(line.split(":")[-1].strip())
                elif line.startswith("- temps préparation :"):
                    mins = int(line.split(":")[1].strip().replace("min", ""))
                    recipe_data["prep_time"] = timedelta(minutes=mins)
                elif line.startswith("- temps cuisson :"):
                    mins = int(line.split(":")[1].strip().replace("min", ""))
                    recipe_data["cooking_time"] = timedelta(minutes=mins)
                elif line.startswith("## "):
                    current_section = line[3:].lower().strip()
                elif line.startswith("- [ ]"):
                    if current_section == "ingrédients":
                        ingredients.append(load_ingredient(line))
                    elif current_section == "ustensiles":
                        ustensiles.append(line.replace("- [ ]", "").strip())
                    elif current_section == "instructions":
                        instructions.append(line.replace("- [ ]", "").strip())
                elif current_section == "macronutriments":
                    try:
                        if "calories" in line or "kcal" in line:
                            match = re.search(r"(\d+)", line)
                            if match:
                                recipe_data["kcal"] = int(match.group(1))
                        elif any(x in line for x in ["protéines", "proteins", "prots"]):
                            match = re.search(r"(\d+)", line)
                            if match:
                                recipe_data["proteins"] = float(match.group(1))
                        elif any(x in line for x in ["glucides", "carbs"]):
                            match = re.search(r"(\d+)", line)
                            if match:
                                recipe_data["carbs"] = float(match.group(1))
                        elif any(x in line for x in ["lipides", "fat"]):
                            match = re.search(r"(\d+)", line)
                            if match:
                                recipe_data["fat"] = float(match.group(1))
                    except Exception:
                        # Skip malformed macro lines
                        continue

            macros = Macros(
                kcal=recipe_data["kcal"],
                proteins=recipe_data["proteins"],
                carbs=recipe_data["carbs"],
                fat=recipe_data["fat"],
            )

            recipes.append(
                Recipe(
                    name=recipe_data["name"],
                    absolute_path=str(recipe_file.absolute()),
                    nb_portions=recipe_data["nb_portions"],
                    prep_time=recipe_data["prep_time"],
                    cooking_time=recipe_data["cooking_time"],
                    ingredients=ingredients,
                    ustensiles=ustensiles,
                    instructions=instructions,
                    macros=macros,
                )
            )

        except Exception as e:
            print(f"Error loading recipe {recipe_file}: {str(e)}")
            continue

    return recipes
