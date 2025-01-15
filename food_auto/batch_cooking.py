from typing import List
from datetime import date
from pathlib import Path
from food_auto.datatypes import Recipe, GroceryItem

def generate_grocery_list(recipes: List[Recipe], output_path="output"):
    """
    Generate a grocery list markdown file from a list of recipes.
    Combines similar ingredients and handles different units.
    """
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # Dictionary to store grocery items, keyed by url or name
    grocery_dict = {}
    
    for recipe in recipes:
        for ingredient in recipe.ingredients:
            # Use url as key if available, otherwise use name
            key = ingredient.url if ingredient.url else ingredient.name
            
            if key not in grocery_dict:
                grocery_dict[key] = GroceryItem(
                    name=ingredient.name,
                    url=ingredient.url,
                    quantities={}
                )
            
            # Add quantities
            if ingredient.quantity:
                unit = ingredient.unit or ""
                if unit in grocery_dict[key].quantities:
                    grocery_dict[key].quantities[unit] += ingredient.quantity
                else:
                    grocery_dict[key].quantities[unit] = ingredient.quantity
    
    # Generate markdown file
    output_file = Path(output_path) / f"groceries_{date.today().strftime('%Y-%m-%d')}.md"
    
    with open(output_file, "w") as f:
        for item in grocery_dict.values():
            # Format quantities string
            quantities = ", ".join(f"{qty if qty is not None else ''} {unit if unit is not None else ''}" for unit, qty in item.quantities.items())
            
            # Format line based on whether URL exists
            if item.url:
                f.write(f"- [ ] [{item.name}]({item.url}) : {quantities}\n")
            else:
                f.write(f"- [ ] {item.name} : {quantities}\n")

def generate_cooking_instructions(recipes: List[Recipe], output_path="output"):
    """
    Generate cooking instructions markdown file from a list of recipes.
    Creates a comprehensive guide for batch cooking.
    """
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    output_file = Path(output_path) / f"instructions_{date.today().strftime('%Y-%m-%d')}.md"
    
    with open(output_file, "w") as f:
        for recipe in recipes:
            f.write(f"# {recipe.name}\n\n")
            
            # Ingredients section
            f.write("## Ingredients\n")
            for ingredient in recipe.ingredients:
                qty_str = f"{ingredient.quantity if ingredient.quantity is not None else ''} {ingredient.unit if ingredient.unit is not None else ''}" if ingredient.quantity is not None else ""
                if qty_str.strip():
                    f.write(f"- [ ] {qty_str} : {ingredient.name}\n")
                else:
                    f.write(f"- [ ] {ingredient.name}\n")
            f.write("\n")
            
            # Ustensils section
            f.write("## Ustensiles\n")
            for ustensil in recipe.ustensiles:
                f.write(f"- [ ] {ustensil}\n")
            f.write("\n")
            
            # Instructions section
            f.write("## Instructions\n")
            for instruction in recipe.instructions:
                f.write(f"- [ ] {instruction}\n")
            f.write("\n\n")
