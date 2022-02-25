from flask import Flask
from volcano_stats_flask import create_app
from volcano_stats_flask.config import Config

app = create_app(Config.DevelopmentConfig)


@app.route('/')
def index():
    return 'This is the home page for my_flask_app'


if __name__ == '__main__':
    app.run(debug=True)
