from flask import Flask

def create_app():
    app = Flask(__name__)
    # ...

    repo = MemoryRepository()
    populate(...,repo)

    @app.route('/')
    def index():
        return 'Index page'

    @app.route('/hello')
    def hello():
        return 'Hello World!'
    return app