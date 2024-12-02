from flask import Flask
from routes.user_routes import user_bp
from routes.auth_routes import login_bp
from routes.article_routes import article_bp

app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(login_bp)
app.register_blueprint(article_bp)


if __name__ == '__main__':
    app.run(debug=True)
