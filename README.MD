# Django project for the CodeCademy course web apps with django
I’ve been asked by a restaurant owner to build an application 
that will help keep track of how much food they have throughout the day. The owner starts the day with:

- An inventory of different Ingredients, their available quantity, and their prices per unit
- A list of the restaurant’s MenuItems, and the price set for each entry
- A list of the ingredients that each menu item requires (RecipeRequirements)
- A log of all Purchases made at the restaurant

### To run the project install the virtual environment and the dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Run the migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
This creates the database and the tables needed for the project.
### Then run the server:
```bash
python manage.py runserver
```
- finally create an account