from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app(config_class_name):
    """
    Initialise the Flask application.
    :type config_classname: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class_name)
    csrf.init_app(app)

    from volcano_stats_flask.main.routes import main_bp
    app.register_blueprint(main_bp)

    from volcano_stats_flask.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app