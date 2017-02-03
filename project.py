from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurantId>/')
def restaurantMenu(restaurantId):
    restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurantId)

    return render_template('menu.html', restaurant = restaurant, items = items)


@app.route('/restaurant/<int:restaurantId>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurantId):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurantId)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurantId = restaurantId))
    else:
        return render_template('newmenuItem.html', restaurantId = restaurantId)


@app.route('/restaurant/<int:restaurantId>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurantId, menu_id):
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
        return redirect(url_for('restaurantMenu', restaurantId = restaurantId))
    else:
        return render_template('editmenuItem.html', item = item)


@app.route('/restaurant/<int:restaurantId>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurantId, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Menu Item Deleted!")
        return redirect(url_for('restaurantMenu', restaurantId = restaurantId))
    else:
        return render_template('deletemenuItem.html', restaurantId = restaurantId, menu_id = menu_id, item = item)


if __name__ == '__main__':
    app.secret_key = 'itsasecret'
    app.debug = True
    app.run(host = '', port = 5000)
