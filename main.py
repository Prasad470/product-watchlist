
from flask import *
from flask import Flask,Blueprint
from path.path import path
app = Flask(__name__)

app.register_blueprint(path,url_prefix="")
app.secret_key = 'random string'


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@path.route("/")
@path.route("/add")
@path.route("/addItem", methods=["GET", "POST"])
@path.route("/remove")
@path.route("/removeItem")
@path.route("/displayCategory")
@path.route("/loginForm")
@path.route("/register", methods = ['GET', 'POST'])
@path.route("/registerationForm")
@path.route("/login", methods = ['POST', 'GET'])
@path.route("/productDescription")
@path.route("/cart")
@path.route("/addToCart")
@path.route("/removeFromCart")
@path.route("/logout")




def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)

	
