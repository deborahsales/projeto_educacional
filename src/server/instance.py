from flask import Flask
from flask_restx import Api

class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app,
                       version='1.0',
                       title='API Projeto Educacional',
                       description='Parte 3 | Etapa 2 - para a disciplina de Banco de Dados I',
                       doc='/docs',default="Documentação", default_label="api")
    
    def run(self):
        self.app.run(host='0.0.0.0', port=8000)

server = Server()