from flask import Flask
from flask_restx import Api
import psycopg2

# Conexão à instância RDS na AWS
url = 'postgresql://postgres:Isac$&62513@db-isac-rds1.ccjja7bteogf.us-east-1.rds.amazonaws.com:5432/db_isac'
connection = psycopg2.connect(url)

class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app,
                       version='1.0',
                       title='API Projeto Educacional',
                       description='Parte 3 | Etapa 2 - para a disciplina de Banco de Dados I',
                       doc='/docs',default="Documentação", default_label="api")
    
    def run(self):
        self.app.run(host='0.0.0.0', port=8000, debug=True)

server = Server()