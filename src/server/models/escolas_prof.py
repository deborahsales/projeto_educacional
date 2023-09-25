from flask_restx import fields
from src.server.instance import server

escolas_prof = server.api.model('Escola_Professor', {

    'inep_escola': fields.Integer(description='Código da instituição de ensino', required=True),
    'cpf_professor': fields.Integer(description='CPF do professor', required=True),
    'vinculo': fields.String(description='Vinculo do professor com a escola'),
    'usuario_plataforma': fields.String(description='Identificação professor na plataforma'),
    'ch_trabalho': fields.Integer(description='Carga horária de trabalho do professor'),
    'matutino': fields.Integer(description='O professor trabalha no turno matutino? True or False', required=True),
    'vespertino': fields.Integer(description='O professor trabalha no turno vespertino? True or False', required=True),
    'noturno': fields.Integer(description='O professor trabalha no turno noturno? True or False', required=True)

})

class EscolasProf(fields.Raw):
    def format(self, value):
        return {'inep_escola': value.inep_escola, 'cpf_professor': value.cpf_professor, 
                'vinculo': value.vinculo, 'usuario_plataforma': value.usuario_plataforma, 
                'ch_trabalho': value.ch_trabalho, 'matutino': value.matutino, 'vespertino': value.vespertino, 'noturno': value.noturno}