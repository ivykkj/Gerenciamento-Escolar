from flask import Flask
from flask_cors import CORS
from config import Config
from flasgger import Swagger
from controllers.nota_controller import nota_bp
from controllers.atividade_controller import atividade_bp
from models import db

app = Flask(__name__)
CORS(app)
swagger = Swagger(app, template_file='swagger.yml')

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(atividade_bp, url_prefix='/api')
app.register_blueprint(nota_bp, url_prefix='/api')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8083)