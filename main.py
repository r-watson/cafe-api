from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # # Make sure to have this method indneted insid the Cafe class if you want to
        # # call if correctly below instead of passing the cafe object into the function.
        # # Method 1 using a for loop.
        # dictionary = {}
        # # Loop through each column in the data record
        # for column in self.__table__.columns:
        #     ## Create a new dictionary entry;
        #     ## where the key ist he name of the column
        #     ## and the value is the value of the column
        #     dictionary[column.name] = getattr(self, column.name)
        # return dictionary
        ## Method 2 using dictionary comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")

## HTTP GET - Read Record

# Get is allowed by default on all routes. Function to get random cafe. Return JSON of selected cafe.
@app.route("/random")
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    ## manually format your db object as a json
    # return jsonify(cafe={
    #         "id": random_cafe.id,
    #         "name": random_cafe.name,
    #         "map_url": random_cafe.map_url,
    #         "img_url": random_cafe.img_url,
    #         "location": random_cafe.location,
    #         "seats": random_cafe.seats,
    #         "has_toilet": random_cafe.has_toilet,
    #         "has_wifi": random_cafe.has_wifi,
    #         "has_sockets": random_cafe.has_sockets,
    #         "can_take_calls": random_cafe.can_take_calls,
    #         "coffee_price": random_cafe.coffee_price,
    #     })
    ## instead of typing it all out you can convert the object to a dict and then convert to json.
    ## use a separate function for dict conversion
    return jsonify(cafe=random_cafe.to_dict())

@app.route("/all")
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])

@app.route("/search")
def search_for_cafe():
    search_location = request.args.get('loc')
    search_results = Cafe.query.filter_by(location=search_location).all()
    # cafe_list = [cafe.to_dict() for cafe in search_results]
    if search_results:
        return jsonify(cafe=[cafe.to_dict() for cafe in search_results])
    return jsonify(error={"Not found": "Sorry, we don't have a cafe at that location."})


## HTTP POST - Create Record

@app.route("/add", methods=["POST"])
def add_cafe():
    if request.method == "POST":
        # db_remove = Cafe.query.get(22)
        # db.session.delete(db_remove)
        # db.session.commit()
        data = request.form
        print(request.form.get("name"))
        # can use request.form["name"] or request.form.get("name")
        new_cafe = Cafe(
            name=data["name"],
            map_url=data["map_url"],
            img_url=data["img_url"],
            location=data["location"],
            seats=data["seats"],
            has_toilet=bool(data["has_toilet"]),
            has_wifi=bool(data["has_wifi"]),
            has_sockets=bool(data["has_sockets"]),
            can_take_calls=bool(data["can_take_calls"]),
            coffee_price=data["coffee_price"],
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})
    return jsonify(error={"failed": "Sorry, you failed to add that cafe."})

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
