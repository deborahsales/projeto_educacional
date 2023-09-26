import psycopg2
from flask import jsonify, request
from flask_restx import Resource
from src.server.instance import connection
from src.server.instance import server

app, api = server.app, server.api

CREATE_ESCOLA_PROF = '''INSERT INTO projeto_educacional.escolas_prof (inep_escola, cpf_professor, vinculo, usuario_plataforma, ch_trabalho, 
                        matutino, vespertino, noturno) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
READ_ESCOLA_PROF = 'SELECT * FROM projeto_educacional.escolas_prof WHERE cpf_professor = %s AND inep_escola = %s'
DELETE_ESCOLA_PROF = 'DELETE FROM projeto_educacional.escolas_prof WHERE cpf_professor = %s AND inep_escola = %s'
SQL_UPDATE = '''UPDATE projeto_educacional.escolas_prof SET vinculo = %s, usuario_plataforma = %s, ch_trabalho = %s
                        matutino = %s, vespertino = %s, noturno = %s WHERE cpf_professor = %s AND inep_escola = %s'''

@api.route('/escola_prof')
class Escola_Prof(Resource):
    def post(self):
        dados = request.json()
        inep_escola = dados.get('inep_escola')
        cpf_professor = dados.get('cpf_professor')
        vinculo = dados.get('vinculo')
        usuario_plataforma = dados.get('usuario_plataforma')
        ch_trabalho = dados.get('ch_trabalho')
        matutino = dados.get('matutino')
        vespertino = dados.get('vespertino')
        noturno = dados.get('noturno')
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_ESCOLA_PROF, (inep_escola, cpf_professor, vinculo, usuario_plataforma, ch_trabalho, matutino, vespertino, noturno))
            return f'Escola_prof cadastrada'
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
