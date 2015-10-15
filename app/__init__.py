from flask import Flask, g, render_template, abort
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

@app.before_first_request
def before_first_request():
    try:
        db.create_all()
    except Exception, e:
        print e

from app.views import home
from app.views import user 

app.register_blueprint(home.mod)
app.register_blueprint(user.mod)

# @app.errorhandler(403)
# def forbidden_page(error):
#     return render_template('403.html'), 403

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404

# @app.errorhandler(500)
# def server_error_page(error):
#     return render_template('500.html'), 500
