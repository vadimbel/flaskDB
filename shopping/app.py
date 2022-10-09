from flask import Flask, render_template, g, request, flash, redirect, url_for
import sqlite3
from database import connect_db, get_db, add_item, get_item, delete_item, check_both_fields, check_username\
    , check_username_in_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismysecretkey!'


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/', methods=['GET', 'POST'])
def login_page():
    db = get_db()

    if request.method == 'POST':
        # get the user input from login page :
        user_name = request.form['username']
        password = request.form['password']

        # check if user_name & password is in the db :
        result = db.execute(f"SELECT * FROM users WHERE username='{user_name}' AND password='{password}'").fetchall()

        # if not -> show error message to the user & stay in that page
        if len(result) == 0:
            flash("Invalid username/password", "error")
            return redirect(url_for("login_page"))

        # else -> move to next page
        return render_template('main_page.html')

    return render_template('login.html')


@app.route('/main', methods=['GET', 'POST'])
def main_page():
    db = get_db()

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if request.form['btn'] == "ADD":
            # check if both text-fields are not empty & if provided username is not in db
            if not check_both_fields(username, password):
                flash("All text-fields must be filled", "error")
            elif not check_username(username, db):
                flash("username is already in use", "error")
            else:
                # get the values from text fields & pass them to function from database.py
                add_item(username, password, db)

                # send valid message to user
                flash(f"New data with values : {username} , {password} - has been added successfully", "info")

        elif request.form['btn'] == "GET":
            # check if username & password fields are not empty
            if not check_both_fields(username, password):
                flash("All text-fields must be filled", "error")
            # check if provided username is in db
            elif not check_username_in_db(username, db):
                flash("provided username is not found", "error")
            else:
                # valid input , get user from db
                data = get_item(username, password, db)

                # display to user
                flash(f"Data is : {data}", "info")

        elif request.form['btn'] == "DELETE":
            # check if username & password fields are not empty
            if not check_both_fields(username, password):
                flash("All text-fields must be filled", "error")
            # check if provided username is in db
            elif not check_username_in_db(username, db):
                flash("provided username is not found", "error")
            else:
                # delete item from db
                delete_item(username, db)

                # display message to user
                flash(f"Item with username: {username} - was deleted successfully")

        return redirect(url_for('main_page'))

    return render_template('main_page.html')


if __name__ == '__main__':
    app.run(debug=True)
