from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Ingredient(db.Model):
    """list of ingredients that will be searched for/used in recipes """

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<ingredient ingredient_id={self.id} name={self.name}>"


class Inventory(db.Model):
    """inventory to be updated at each shopping trip """

    __tablename__ = "inventories"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.ingredient_id"))
    mealplan_id = db.Column(db.Integer, db.ForeignKey("mealplans.mealplan_id"))
    in_stock = db.Column(db.Boolean)
    use_this_week = db.Column(db.Boolean)
    bought = db.Column(db.TIMESTAMP(timezone=True), nullable=False, default=datetime.now(tz=timezone.utc))
    quantity = db.Column(db.Integer)

    ingredient = db.relationship('Ingredient', backref='inventories')
    mealplan = db.relationship('Mealplan', backref='inventories')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Ingredient id={self.ingredient_id} in_stock={self.in_stock} bought={self.bought} quantity={self.quantity}>"


class Recipe(db.Model):
    """unique table created for each recipe """ 

    __tablename__ = "recipe"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    required_ingredients = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Card card_id={self.card_id} name={self.name}>"


class MealPlan(db.Model):
    """unique table created for each recipe """ 

    __tablename__ = "mealplans"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Card card_id={self.card_id} name={self.name}>"
        

class Ingredients_Recipes(db.Model):
    """unique table created for each recipe """ 

    __tablename__ = "ingredients_recipes"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.ingredient_id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"))
    
    ingredient = db.relationship('Ingredient', backref='ingredients_recipes')
    recipe = db.relationship('Recipe', backref='ingredients_recipes')


class Recipe_MealPlan(db.Model):
    """unique table created for each recipe """ 

    __tablename__ = "recipes_mealplans"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"))
    mealplan_id = db.Column(db.Integer, db.ForeignKey("mealplans.mealplan_id"))

    recipe = db.relationship('Recipe', backref='recipes_mealplans')
    mealplan = db.relationship('MealPlan', backref='recipes_mealplans')
    

def connect_to_db(flask_app, db_uri='postgresql:///meals', echo=True):
    """Connect the database to our Flask app."""
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
 