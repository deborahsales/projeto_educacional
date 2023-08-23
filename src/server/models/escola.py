from flask_restx import fields
from server.instance import server

escola = server.api('Escola', {

    'inep': fields.Integer(description='Código da instituição de ensino da escola', required=True),
    'nome': fields.String(description='Nome da escola', required=True),
    'ano_entrada': fields.String(description='Ano em que a escola deu entrada no projeto', requred=True),
    'status_escola': fields.String(description='Estado em que a escola se encontra', required=True, max=1),
    'tipo': fields.String(description='Tipo da escola: 1 - urbana, 2 - rural', required=True, max=1),
    'dependencia': fields.String(description='Tipo de dependência da escola', required=True, max=1),
    'latitude': fields.Decimal(description='Latitude da escola'),
    'longitude': fields.Decimal(description='Longitude da escola'),
    'endereco': fields.String(description='Endereço da escola', max=300),
    'id_rede': fields.Integer(description='identificador da rede em que a escola está associada', required=True)

})