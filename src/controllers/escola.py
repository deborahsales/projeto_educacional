import psycopg2
from flask import jsonify, request
from flask_restx import Resource
from src.server.instance import connection
from src.server.instance import server
from src.server.models.escola import escola, Escola

app, api = server.app, server.api

CREATE_ESCOLA = '''INSERT INTO projeto_educacional.escola (inep, nome, ano_entrada, status_escola, tipo, 
                        dependência, latitude, longitude, endereco, id_rede)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
READ_ESCOLA = 'SELECT * FROM projeto_educacional.escola WHERE inep = %s'
DELETE_ESCOLA = 'DELETE FROM projeto_educacional.escola WHERE inep = %s'
SQL_UPDATE = 'UPDATE projeto_educacional.escola SET '

@api.route('/escola')
class Escola(Resource):
    def post(self):
        try:
            dados = request.get_json()
            inep = dados.get('inep')
            nome = dados.get('nome')
            ano_entrada = dados.get('ano_entrada')
            status  = dados.get('status_escola')
            tipo = dados.get('tipo')
            dependencia = dados.get('dependencia')
            latitude = dados.get('latitude')
            longitude = dados.get('longitude')
            endereco = dados.get('endereco')
            id_rede = dados.get('id_rede')
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_ESCOLA, (inep, nome, ano_entrada, status, tipo, dependencia, latitude, longitude, endereco, id_rede))
            return f'Escola cadastrada com sucesso.'
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'

    def get(self):
        try:
            dados = request.get_json()
            inep = dados['inep']
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(READ_ESCOLA, (inep,))
                    escola = cursor.fetchone()
            if escola == None:
                return f'Escola {inep} não encontrada.'
            else:
                return jsonify(escola)
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
        
    def delete(self):
        try:
            dados = request.get_json()
            inep = dados.get('inep')
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(DELETE_ESCOLA, (inep,))
            return "Escola excluída com sucesso."
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
        
    def put(self):
        try:
            dados = request.get_json()
            inep = dados.get('inep')
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(READ_ESCOLA, (inep,))
                    escola = cursor.fetchone()
                if escola == None:
                    return f'Escola {inep} não encontrada.'
                else:
                    primeiro = True
                    sql = SQL_UPDATE
                    if 'nome' in dados:
                        sql += f"nome = '{dados.get('nome')}'"
                        primeiro = False
                    if 'ano_entrada' in dados:
                        if (not primeiro) :
                            sql += ", "
                        sql += f"ano_entrada = '{str(dados.get('ano_entrada'))}'"
                        primeiro = False
                    if 'status_escola' in dados:
                        if (not primeiro) :
                            sql += ", "
                        sql += f"status_escola = '{dados.get('status_escola')}'"
                        primeiro = False
                    if 'tipo' in dados:
                        if (not primeiro):
                            sql += ', '
                        sql += f"tipo = '{dados.get('tipo')}'"
                        primeiro = False
                    if 'dependencia' in dados:
                        if (not primeiro):
                            sql += ', '
                        sql += f"dependência = '{str(dados.get('dependencia'))}'"
                        primeiro = False
                    if 'latitude' in dados:
                        if (not primeiro):
                            sql += ', '
                        sql += f"latitude = '{str(dados.get('latitude'))}'"
                        primeiro = False
                    if 'longitude' in dados:
                        if (not primeiro):
                            sql += ', '
                        sql += f"longitude = '{str(dados.get('longitude'))}'"
                        primeiro = False
                    if 'endereco' in dados:
                        if (not primeiro):
                            sql += ', '
                        sql += f"endereco = '{dados.get('endereco')}'"
                        primeiro = False
                    if 'id_rede' in dados:
                        if (not primeiro) :
                            sql += ", "
                        sql += f"id_rede = '{str(dados.get('id_rede'))}'"

                    sql += "WHERE inep = " + dados.get('inep')
                    with connection.cursor() as cursor:
                        cursor.execute(sql)
                    
            return jsonify("Cadastro da escola atualizado com sucesso.")
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}, {sql}'
        except Exception as e:
            return f'Erro inesperado: {e}'