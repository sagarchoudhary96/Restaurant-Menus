from flask import Flask, render_template, request, redirect, url_for
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
        return redirect(url_for('restaurantMenu', restaurantId = restaurantId))
    else:
        return render_template('newmenuItem.html', restaurantId = restaurantId)


@app.route('/restaurant/<int:restaurantId>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurantId, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        editedName = request.form['name']
        if editedName:
            item.name = editedName
        session.add(item)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurantId = restaurantId))
    else:
        return render_template('editmenuItem.html', restaurantId = restaurantId, menu_id = menu_id, item = item)

@app.route('/restaurant/<int:restaurantId>/<int:menu_id>/delete/')
def deleteMenuItem(restaurantId, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host = '', port = 5000)
