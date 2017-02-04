from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# Making API endpointss for the json
@app.route('/restaurants.json')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu.json')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[item.serialize for item in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>.json')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem = menuItem.serialize)


@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html", restaurants = restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['newRestaurantName'])
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant Created!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template("newRestaurant.html")

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        editedName = request.form['restaurantName']
        if editedName:
            restaurant.name = editedName
            flash("Restaurant Edited")
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template("editRestaurant.html", restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant Deleted!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template("deleteRestaurant.html", restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant = restaurant, items = items)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        course = request.form['course']
        newItem = MenuItem(name = name, description = description, price = price, course = course, restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuItem.html', restaurant_id = restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        editedName = request.form['name']
        editedDescription = request.form['description']
        editedPrice = request.form['price']
        editedCourse = request.form['course']
        if editedName:
            item.name = editedName

        if editedDescription:
            item.description = editedDescription

        if editedPrice:
            item.price = editedPrice

        if editedCourse:
            item.course = editedCourse

        session.add(item)
        session.commit()
        flash("Menu Item Edited!")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuItem.html', item = item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Menu Item Deleted!")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = item)


if __name__ == '__main__':
    app.secret_key = 'itsasecret'
    app.debug = True
    app.run(host = '', port = 5000)
