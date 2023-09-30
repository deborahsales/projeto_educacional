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
SQL_UPDATE = 'UPDATE projeto_educacional.escolas_prof SET '

@api.route('/escola_prof')
class Escola_Prof(Resource):
    def post(self):
        dados = request.get_json()
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
            return f'Vinculo cadastrado na tabela escola_prof com sucesso.'
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
        
    def get(self):
        dados = request.get_json()
        inep_escola = dados['inep_escola']      
        cpf_professor = dados['cpf_professor']
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(READ_ESCOLA_PROF, (cpf_professor, inep_escola))
                    escola_prof = cursor.fetchone()
            if escola_prof == None:
                return f'Vinculo do professor {cpf_professor} na escola {inep_escola} não encontrado.'
            else:
                return jsonify(escola_prof)
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
        
    def delete(self):
        dados = request.get_json()
        inep_escola = dados['inep_escola']      
        cpf_professor = dados['cpf_professor']
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(DELETE_ESCOLA_PROF, (cpf_professor, inep_escola))
            return "Vinculo excluído com sucesso da tabela escola_prof."
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
        
    def put(self):
        dados = request.get_json()
        inep_escola = dados['inep_escola']      
        cpf_professor = dados['cpf_professor']
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(READ_ESCOLA_PROF, (cpf_professor, inep_escola))
                    escola = cursor.fetchone()
                if escola == None:
                    return f'Vinculo do professor {cpf_professor} na escola {inep_escola} não encontrado.'
                else:
                    primeiro = True
                    sql = SQL_UPDATE
                    if 'vinculo' in dados:
                        sql += f"vinculo = '{dados.get('vinculo')}'"
                        primeiro = False
                    if 'usuario_plataforma' in dados:
                        if (not primeiro) :
                            sql += ", "
                        sql += f"usuario_plataforma = '{dados.get('usuario_plataforma')}'"
                        primeiro = False
                    if 'ch_trabalho' in dados:
                        if (not primeiro) :
                            sql += ", "
                        sql += f"ch_trabalho = {dados.get('ch_trabalho')}"
                        primeiro = False
                    if 'matutino' in dados:
                        if (not primeiro):
                            sql += ', '
                        sql += f"matutino = {dados.get('matutino')}"
                        primeiro = False
                    if 'vespertino' in dados:
                        if (not primeiro):
                            sql += ', '
                        sql += f"vespertino = {dados.get('vespertino')}"
                        primeiro = False
                    if 'noturno' in dados:
                        if (not primeiro) :
                            sql += ", "
                        sql += f"noturno = {str(dados.get('noturno'))}"

                    sql += f" WHERE cpf_professor = {dados.get('cpf_professor')} AND inep_escola = {dados.get('inep_escola')}"
                    with connection.cursor() as cursor:
                        cursor.execute(sql)
                    
            return jsonify(f'Vínculo atualizado na tabela escola_prof com sucesso.')
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'

