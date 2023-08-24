import psycopg2
from flask import jsonify, request
from flask_restx import Resource
from src.server.instance import connection
from src.server.instance import server
from server.models.escola_prof import escola_prof, EscolaProf

app, api = server.app, server.api

CREATE_ESCOLA_PROF = '''INSERT INTO projeto_educacional.escolas_prof (inep_escola, cpf_professor, vinculo, usuario_plataforma, ch_trabalho, 
                        matutino, vespertino, noturno) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
READ_ESCOLA_PROF = 'SELECT * FROM projeto_educacional.escolas_prof WHERE cpf_professor = %s AND inep_escola = %s'
DELETE_ESCOLA_PROF = 'DELETE FROM projeto_educacional.escolas_prof WHERE cpf_professor = %s AND inep_escola = %s'
UPDATE_ESCOLA_PROF = '''UPDATE projeto_educacional.escolas_prof SET vinculo = %s, usuario_plataforma = %s, ch_trabalho = %s
                        matutino = %s, vespertino = %s, noturno = %s WHERE cpf_professor = %s AND inep_escola = %s'''

@api.route('/escola_prof')
class Escola_Prof(Resource):
    def create_escola_prof(self):
        dados = request.json()
