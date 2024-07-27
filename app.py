from flask import Flask
from os import getenv
import routes
from db import db

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db.init_app(app)

routes.create_routes(app)

with app.app_context(): 
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
