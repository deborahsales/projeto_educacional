from flask_restx import fields
from src.server.instance import server

professor = server.api('Professor', {

    'cpf': fields.Integer(description='CPF do professor', required=True),
    'nome': fields.String(description='Nome do professor', required=True),
    'telefone': fields.List(description='Telefones do professor', required=True),
    'email': fields.List(description='Emails do professor', required=True),
    #'cargo': fields.String(description='Cargo do profissional', required=True), // podemos passar sempre 'Professor' para o cargo, no insert
    'data_nacimento': fields.DateTime(description='Data de nascimento do professor', required=True, dt_format='iso8601'),
    'ano_entrada': fields.Integer(description='Ano de entrada no projeto pelo professor', required=True)

})

class Professor(fields.Raw):
    def format(self, value):
        return {'cpf': value.cpf, 'nome': value.nome, 'telefone': value.telefone,
                'email': value.email, 'data_nascimento': value.data_nascimento, 'ano_entrada': value.ano_entrada}