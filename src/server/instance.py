from flask import Flask
from flask_restx import Api
import psycopg2

# Conexão à instância RDS na AWS
url = 'postgres://postgres:postgres@deborah-rds.c6u7sarwqno4.us-east-1.rds.amazonaws.com:5432/postgres'
connection = psycopg2.connect(url)

class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app,
                       version='1.0',
                       title='API Projeto Educacional',
                       description='Parte 4 | Etapa 2 - para a disciplina de Banco de Dados I',
                       doc='/docs',default="Documentação", default_label="api")
    
    def run(self):
        self.app.run(host='0.0.0.0', port=8000, debug=True)

server = Server()