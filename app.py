from base import app, api
from views import SearchView

api.add_resource(SearchView, '/search')

if __name__ == '__main__':
    app.run()
