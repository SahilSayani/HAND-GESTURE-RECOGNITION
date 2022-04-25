from flask import Flask
from flask.helpers import url_for


def create_app():
    from .views import views
    app=Flask(__name__,template_folder="templates")
    app.config['SECRET_KEY']="abcd"  
    app.register_blueprint(views,url_prefix='/')
    return app
