import sys
import argparse
from pathlib import Path
from typing import List
from pyfzf.pyfzf import FzfPrompt

from .recipe_reader import load_recipes
from .batch_cooking import generate_grocery_list, generate_cooking_instructions
from .datatypes import Recipe

DEFAULT_RECIPE_PATH = "recipes"

def recipe_selection_loop(recipe_list: List[Recipe]) -> List[Recipe]:
    """
    Interactive recipe selection using fzf.
    Returns list of selected recipes.
    """
    fzf = FzfPrompt()
    selected_recipes = []
    total_portions = 0
    
    while True:
        # Prepare recipe choices
        choices = []
        for recipe in recipe_list:
            if recipe not in selected_recipes:
                choices.append(f"{recipe.name}\tnumber of portions: {recipe.nb_portions}")
        choices.append("generate\tselect to generate output and quit")
        
        # Create header with current portions count
        header = (
            "Use arrow keys to navigate\n"
            "Enter to validate\n"
            "Tab to select, Shift-Tab to unselect\n"
            "Esc to quit\n"
            "You can also type to filter\n\n"
            f"Current number of portions selected: {total_portions}"
        )
        
        try:
            # Show fzf prompt
            selected = fzf.prompt(
                choices,
                '--multi --cycle --preview="echo {2}" --delimiter "\t" '
                '--with-nth=1 --header="' + header + '" '
                '--header-first --layout=reverse'
            )
        except:
            # Handle Esc key or other interruptions
            break
            
        if not selected:
            continue
            
        # Process selections
        for choice in selected:
            if choice.startswith("generate"):
                return selected_recipes
            
            # Find corresponding recipe
            recipe_name = choice.split("\t")[0]
            recipe = next(r for r in recipe_list if r.name == recipe_name)
            
            if recipe not in selected_recipes:
                selected_recipes.append(recipe)
                total_portions += recipe.nb_portions
    
    return selected_recipes

def main():
    """Main entry point for the batch cooking program."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate batch cooking instructions and grocery list")
    parser.add_argument("--path", type=str, default=DEFAULT_RECIPE_PATH,
                       help="Path to recipe directory")
    args = parser.parse_args()
    
    # Load recipes
    try:
        recipes = load_recipes(args.path)
    except Exception as e:
        print(f"Error loading recipes: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not recipes:
        print(f"No recipes found in {args.path}", file=sys.stderr)
        sys.exit(1)
    
    # Select recipes
    selected_recipes = recipe_selection_loop(recipes)
    
    if not selected_recipes:
        print("No recipes selected", file=sys.stderr)
        sys.exit(0)
    
    # Generate output
    try:
        generate_grocery_list(selected_recipes)
        generate_cooking_instructions(selected_recipes)
        print("Successfully generated grocery list and cooking instructions!")
    except Exception as e:
        print(f"Error generating output: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
