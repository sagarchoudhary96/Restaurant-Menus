from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'><h3>Make a New Restaurant Here</h3></a><br>"

                for restaurant in restaurants:
                    output += restaurant.name
                    output += "<br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a><br>" % str(restaurant.id)
                    output += "<a href='#'>Delete</a>"
                    output += "<br><br>"

                output += "</body></html>"

                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h2>Make a New Restaurant</h2><br>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input type ='text' name='newRestaurant' placeholder='new Restaurant Name'><input type='submit' value='create'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantId = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h2>%s</h2><br>" % restaurant.name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><input type ='text' name='restaurantName' placeholder='Restaurant Name'><input type='submit' value='Rename'></form>" % restaurantId
                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            seld.send_error(404,"File not found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):

                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newRestaurant = fields.get('newRestaurant')
                    # entry created to be inserted into the database
                    restaurant = Restaurant(name = newRestaurant[0])

                    # entry added to the session
                    session.add(restaurant)

                    # commit session to update the database
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

            if self.path.endswith("/edit"):

                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantName = fields.get('restaurantName')[0]
                    restaurantId = self.path.split('/')[2]

                    restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()
                    restaurant.name = restaurantName

                    # add updated values to the session
                    session.add(restaurant)

                    # commit the session
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                    return

        except:
            pass
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()
