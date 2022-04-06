from volcano_stats_flask import create_app
from volcano_stats_flask.config import DevelopmentConfig



app = create_app(DevelopmentConfig)


if __name__ == '__main__':
    app.run(debug=True)


