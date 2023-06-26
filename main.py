
from flask import *
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy # pip install flask_sqlalchemy
import random
import os


#______________ Configuration DB
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quote.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


#________________ Creating DB Table
with app.app_context():
    class Quote(db.Model):
        id=db.Column(db.Integer, primary_key=True)
        quote = db.Column(db.String(500), nullable=False)
        author = db.Column(db.String(120), nullable=False)

        def to_dic(self):
            return {c.name : getattr(self, c.name) for c in self.__table__.columns}

    # db.create_all()

    # new_quote = Quote(
    #     quote = "Bcz Sky is not that High!",
    #     author = "Ali Jafarbeglou"
    # )
    # db.session.add(new_quote)
    # db.session.commit()


    @app.route('/', methods=["GET", "POST"])
    def home():

        if request.method == "POST":
            all_quotes = db.session.query(Quote).all()
            random_quote = (random.choice(all_quotes)).to_dic()
            quote = random_quote["quote"]
            author = random_quote["author"]
            return render_template('index.html', quote=quote, author=author)

        all_quotes = db.session.query(Quote).all()
        random_quote = (random.choice(all_quotes)).to_dic()
        quote = random_quote["quote"]
        author = random_quote["author"]
        return render_template('index.html', quote=quote, author=author)

    @app.route('/all')
    def get_all_quotes():
        # all_quotes = db.session.query(Quote).all()
        all_quotes = Quote.query.all()
        return jsonify([c.to_dic() for c in all_quotes])

    @app.route('/random')
    def get_random_quote():
        all_quotes = db.session.query(Quote).all()
        random_quote = random.choice(all_quotes)
        # return jsonify(quote=random_quote.__dict__)
        return jsonify(quote=random_quote.to_dic())



    @app.route('/add', methods=['GET', 'POST'])
    def add_quote():

        if request.method == 'POST':
            new_quote = Quote(
                author=request.form['author'],
                quote=request.form['quote']
            )
            db.session.add(new_quote)
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('add.html')


    @app.route('/delete', methods=['GET', 'POST'])
    def delete_quote():
        if request.method == 'POST':
            id_to_delete = int(request.form['quoteId'])
            quote = Quote.query.get(id_to_delete)
            if quote:
                db.session.delete(quote)
                db.session.commit()
                return redirect(url_for('delete_quote', text="Quote has been deleted!"))

            return redirect(url_for('delete_quote', text="ID not found"))
        return render_template('delete.html')


    @app.route("/report-delete/<int:quote_id>", methods=["DELETE"])
    def delete(quote_id):
        api_key = request.args.get("api-key")
        if api_key == "TopSecretAPIKey":
            cafe = db.session.query(Quote).get(quote_id)
            if cafe:
                db.session.delete(Quote)
                db.session.commit()
                return jsonify(response={"success": "Successfully deleted the Quote from the database."}), 200
            else:
                return jsonify(error={"Not Found": "Sorry a Quote with that id was not found in the database."}), 404
        else:
            return jsonify(
                error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


    # Press the green button in the gutter to run the script.
    if __name__ == '__main__':
        app.run(debug=True)
#
# ----------------------- OPENAI CHATGPT -----------
#
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# from flask import jsonify, request
#
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdb.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# db = SQLAlchemy(app)
#
# with app.app_context():
#     class User(db.Model):
#         id = db.Column(db.Integer, primary_key=True)
#         name = db.Column(db.String(100), nullable=False)
#         email = db.Column(db.String(100), nullable=False)
#
#     db.create_all()
#
#
#     new_user = User(
#         name="Ali25",
#         email="zilo@live.com5"
#     )
#     db.session.add(new_user)
#     db.session.commit()
#
#
#
#     @app.route('/users')
#     def get_users():
#         users = User.query.all()
#         return jsonify([u.__dict__ for u in users])
#
#     @app.route('/users', methods=['POST'])
#     def create_user():
#         data = request.get_json()
#         user = User(name=data['name'], email=data['email'])
#         db.session.add(user)
#         db.session.commit()
#         return jsonify(user.__dict__)
#
#
#     if __name__ == '__main__':
#         app.run(debug=True)
