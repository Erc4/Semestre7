from flask import Flask
from models import db
from routes import usuarios_bp, alimentos_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(usuarios_bp)
app.register_blueprint(alimentos_bp)

if __name__ == '__main__':
    app.run(debug=True)
