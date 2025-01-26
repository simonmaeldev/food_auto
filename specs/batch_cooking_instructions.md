# Batch cooking instruction generator

> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- Create a cli python program that generate a grocery list and cooking instructions for batch cooking based on selected recipes

## Mid-Level Objective

- Accept an optional path to a dir as an argument : it's the dir where all recipes are stored.
- List all the recipes available using fzf, ask the user which recipe he wants to add
- Display the total number of servings currently selected
- Repeat until user wants to generate grocery list and cooking instructions.
- Generate a grocery_list.md containing all the ingredients required
- Generate a cooking_instructions.md, divided per recipe, containing ingredients, cookware and instructions

## Implementation Notes

- Use only the dependencies listed in `pyproject.toml`
- Comment every function thoroughly
- Carefully review each low-level task for precise code changes
- Use pydantic to manage datatypes

## Context

### Beginning Context

- `recipes/example_recipe.md` (readonly)
- `pyproject.toml` (readonly)

### Ending Context

- `recipes/example_recipe.md` (readonly)
- `pyproject.toml` (readonly)
- `src/main.py` (new)
- `src/recipe_reader.py` (new)
- `src/batch_cooking.py` (new)
- `src/datatypes.py` (new)

## Low-Level Tasks

> Ordered from start to finish

1. Create the datatypes in `datatypes.py`

```aider
CREATE src/datatypes.py:
    ADD Ingredient(BaseModel): {url: Optional[str], name: str, quantity: Optional[float], unit: Optional[str]}: represent an ingredient, will be used in the grocery_list.md and cooking_instructions.md
    ADD Macros(BaseModel): {kcal: int, proteins:float, carbs: float, fat: float}
    ADD Recipe(BaseModel): {name: str, absolute_path:str, nb_portions: int, prep_time: timedelta, cooking_time: timedelta, ingredients: List[Ingredient], ustensiles: List[str], instructions: List[str], macros: Macros}
    ADD GroceryItem(BaseModel): {name: str, url: Optional[str], quantities: Dict[unit: str, quantity: float]}
```

2. Create `recipe_reader.py`

```aider
CREATE src/recipe_reader.py:

    ADD function `load_ingredient(str) -> Ingredient`:
        All ingredients are formated the same way, like in `recipes/example_recipe.md`:
        - [ ] quantity unit : [name](url) the name continue here
        - [ ] quantity : name
        - [ ] quantity : [name](url)
        If you can't parse because it's missing `:`, put all the line in `name`, without the `- [ ]`
        Explaination: this formatage is useful because the recipe comes from my obsidian vault, so I'm using it's syntax markdown. - [ ] is for a checkbox, [text](url) is to make the text have an hyperlink
        In some case, because it's a recipe, it may happen that there is no quantity involve, nor unit, link... It makes sense for the recipe. So the default is to have an ingredient with just the name. It may also happen that only a part of the name have an hyperlink, extract the full name. Example : `[poudre de curry](http://link.com) (+ pour garnir)` would give the name `poudre de curry (+ pour garnir)`
        Quantity and units may be stuck together, or separated by a space. Examples : '1 cuillère à café', '400g', '180ml'... the quantity is the number, the unit is the rest ('cuillère à café', 'g', 'ml')
```

3. Modify `recipe_reader.py`

```aider
MODIFY src/recipe_reader.py:

    ADD function `load_recipes(path_dir:str) -> List[Recipe]` :
        load all recipes in path_dir. a recipe is a markdown file. return all the recipes in this dir
        Open the markdown file, they are all formated like `recipes/example_recipe.md`.
        'temps préparation' is `prep_time`, 'temps cuisson' is `cooking_time`
        For the macros, `kcal` could be 'calories' or 'kcal', `proteins` is one of ['protéines', 'proteins', 'prots'], `carbs` is one of ['glucides', 'carbs'] and fat is one of ['lipides', 'fat']
        To load the ingredients, use `load_ingredient(str)`
        Ignore all the `- [ ]`: they are the symbol for a checkbox in md/obsidian. It's useful for the reader when reading the recipe but it's just formating, we can safely ignore them
```

4. Create `batch_cooking.py`

````aider
CREATE src/batch_cooking.py:
    ADD function `generate_grocery_list(recipes:List[Recipe], output_path="output")
        the goal is to generate a grocery list with all the ingredients needed for all the recipes
        grocery_list = Set(GroceryItem)
        The key is the url, but it is optional. So if your item don't have an url, fall back to the name as secondary key for identification. If the units are the same, add the quantity. Otherwise, add it to the quantities Dict. If there is no unit, default to "". If there is no quantity, default to 0
        Then print in the file output_path/groceries_{date as YYYY-MM-DD}.md, for each item:
        `- [ ] [name](url) if url provided else name : qtt, unit for each units you have`

    ADD function `generate_cooking_instructions(recipes: List[Recipe], output_path="output")
        the goal is to generate a comprehensive and easy to follow set of instructions to do batch cooking for all this recipes
        for each recipe, print in output_path/instructions_{date as YYYY-MM-DD}.md as follow:
            ```markdown
# Recipe name

## Ingredients
- [ ] quantity unit : name
- [ ] quantity unit : name
- [ ] quantity unit : name
- [ ] quantity unit : name

## Ustensiles

- [ ] ustensile 1
- [ ] ustensile 2
- [ ] ustensile 3

## Instructions

- [ ] instruction 1
- [ ] instruction 2
- [ ] instruction 3
- [ ] instruction 4
            ```
````

5. Create `main.py`

````aider
CREATE src/main.py:

    ADD def `recipe_selection_loop(recipe_list:List[Recipe]) -> List[Recipe]`:
        use pyfzf to do the selection:
        ```python
        from pyfzf.pyfzf import FzfPrompt
        foo = ["first recipe name\tnumber of portions: 6", "an other recipe\tnumber of portions: 2", "generate\tselect to select all the options and quit"]
        lst = fzf.prompt(foo, '--multi --cycle --preview="echo {2}" --delimiter "\t" --with-nth=1 --header$"Use arrow keys to navigate\nEnter to validate\nTab to select, Shift-Tab to unselect\nEsc to quit\nYou can also type to filter\n\nCurrent number of portions selected: <current_number_of_portions>" --header-first --layout=reverse')
        ```
        The goal is to display the name of the recipe on the left of `\t`, and useful information on the right.
        Add each selected recipe to a list, and display the total number of portions in the header. If the `generate` is in the list, add all the other options to your list of selected recipes, then exit the loop.

    ADD def `main(path:str)`:
        from cli get the path as argument. If it is not given, use the default_path given at the top of the script
        load all the recipes in this dir using `load_recipes`
        loop the recipe_selection_loop
        generate the batch cooking grocery list and cooking instructions
````
