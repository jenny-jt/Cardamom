from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

db = SQLAlchemy()


class Ingredient(db.Model):
    """list of ingredients that will be searched for/used in recipes """

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    created = db.Column(db.TIMESTAMP(timezone=True), nullable=False, default=datetime.now(tz=timezone.utc))
    updated = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    deleted = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    name = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(20), nullable=False)

    recipes_r = db.relationship("Recipe", secondary="ingredients_recipes", backref="ingredients_r")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<ingredient ingredient_id={self.id} name={self.name} location={self.location}>"


class Recipe(db.Model):
    """unique table created for each recipe """

    __tablename__ = "recipes"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    created = db.Column(db.TIMESTAMP(timezone=True), nullable=False, default=datetime.now(tz=timezone.utc))
    updated = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    deleted = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    name = db.Column(db.String(), nullable=False)
    ingredients = db.Column(db.String(), nullable=False)
    cook_time = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=True)

    # ingredients_r = db.relationship("Ingredient", secondary="ingredients_recipes", backref="recipes_r")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Recipe name={self.name} ingredients={self.ingredients}>"


class MealPlan(db.Model):
    """unique table created for each recipe """

    __tablename__ = "mealplans"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    created = db.Column(db.TIMESTAMP(timezone=True), nullable=False, default=datetime.now(tz=timezone.utc))
    updated = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    deleted = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    recipes_r = db.relationship('Recipe', secondary='recipes_mealplans', backref="mealplans_r")
    altrecipes_r = db.relationship('Recipe', secondary='altrecipes_mealplans')
    # user = db.relationship('User')

    def __repr__(self):
        """Provide helpful representation when printed."""
        return f"<Mealplan id={self.id} date={self.date}>"

    def add_recipe_to_mealplan(self, recipe):
        """Add recipe to mealplan"""
        self.recipes_r.append(recipe)

    def add_altrecipe_to_mealplan(self, recipe):
        """Add altrecipe to mealplan"""
        self.altrecipes_r.append(recipe)


class User(db.Model):
    """user logging into app"""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

    mealplans = db.relationship('MealPlan')

    def __repr__(self):
        return f'<User user_id={self.id} email={self.email}>'

    def add_mealplan_to_user(self, mealplan):
        """Add mealplan object to user"""
        self.mealplans.append(mealplan)


##########################relationships###############################


class Ingredient_Recipe(db.Model):
    """association table between ingredient and recipe """

    __tablename__ = "ingredients_recipes"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))


class Recipe_MealPlan(db.Model):
    """association table between recipe and mealplan """

    __tablename__ = "recipes_mealplans"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))
    mealplan_id = db.Column(db.Integer, db.ForeignKey("mealplans.id"))

    recipe_r = db.relationship("Recipe")


class AltRecipe_MealPlan(db.Model):
    """association table between alternate recipes and mealplan"""

    __tablename__ = "altrecipes_mealplans"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))
    mealplan_id = db.Column(db.Integer, db.ForeignKey("mealplans.id"))


##########################relationships###############################


class Inventory(db.Model):
    """inventory to be updated at each shopping trip """

    __tablename__ = "inventories"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    created = db.Column(db.TIMESTAMP(timezone=True), nullable=False, default=datetime.now(tz=timezone.utc))
    updated = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    deleted = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"))
    mealplan_id = db.Column(db.Integer, db.ForeignKey("mealplans.id"))
    in_stock = db.Column(db.Boolean)
    use_this_week = db.Column(db.Boolean)
    bought = db.Column(db.TIMESTAMP(timezone=True), nullable=False, default=datetime.now(tz=timezone.utc))
    quantity = db.Column(db.Integer)

    ingredient_r = db.relationship('Ingredient', backref='inventories_r')
    mealplan_r = db.relationship('MealPlan', backref='inventories_r')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Ingredient id={self.ingredient_id} in_stock:{self.in_stock} bought:{self.bought} quantity:{self.quantity}>"


def connect_to_db(app):
    """Connect the database to our Flask app."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///meals'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

    print('Connected to the db!')


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    os.system('createdb meals')
    db.create_all()
