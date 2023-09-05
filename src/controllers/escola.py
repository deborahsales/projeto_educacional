import psycopg2
from flask import jsonify, request
from flask_restx import Resource
from src.server.instance import connection
from src.server.instance import server
from src.server.models.escola import escola, Escola

app, api = server.app, server.api

CREATE_ESCOLA = '''INSERT INTO projeto_educacional.escola (inep, nome, ano_entrada, status, tipo, 
                        dependencia, latitude, longitude, endereco, id_rede)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
READ_ESCOLA = 'SELECT * FROM projeto_educacional.escola WHERE inep = %s'
DELETE_ESCOLA = 'DELETE FROM projeto_educacional.escola WHERE inep = %s'
UPDATE_ESCOLA = '''UPDATE projeto_educacional.escola SET nome = %s, ano_entrada = %s, status = %s,
                    tipo = %s, dependencia = %s, latitude = %s, longitude = %s, endereco = %s, id_rede = %s WHERE inep = %s'''

@api.route('/escola')
class Escola(Resource):
    def post(self):
        dados = request.get_json()
        inep = dados.get('inep')
        nome = dados.get('nome')
        ano_entrada = [dados.get('ano_entrada')]
        status  = [dados.get('status')]
        tipo = dados.get('tipo')
        dependencia = dados.get('dependencia')
        latitude = dados.get('latitude')
        longitude = dados.get('longitude')
        endereco = dados.get('endereco')
        id_rede = dados.get('id_rede')
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_ESCOLA, (inep, nome, ano_entrada, status, tipo, dependencia, latitude, longitude, endereco, id_rede))
            return f'Escola cadastrado'
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'

    def get(self):
        dados = request.get_json()
        inep = dados['inep']
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(READ_ESCOLA, (inep,))
                    escola = cursor.fetchone()
            if escola == None:
                return f'Escola {inep} não encontrado'
            else:
                return jsonify(escola)
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
        
    def delete(self):
        dados = request.get_json()
        inep = dados.get('inep')
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(DELETE_ESCOLA, (inep,))
            return "Escola excluído com sucesso."
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
        
    def put(self):
        dados = request.get_json()
        inep = dados.get('inep')
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(UPDATE_ESCOLA, (inep,))
                    escola = cursor.fetchone()
                if escola == None:
                    return f'Escola {inep} não encontrado'
                else:
                    # Ainda será necessário verificar funcionamento da variável 'professor', se é possível acessar dessa forma seus atributos
                    if 'nome' in dados:
                        escola.nome = dados.get('nome')
                    if 'telefone' in dados:
                        escola.telefone = dados['telefone']
                    if 'email' in dados:
                        escola.email = dados['email']
                    if 'cargo' in dados:
                        escola.cargo = dados['cargo']
                    if 'data_nascimento' in dados:
                        escola.data_nascimento = dados['data_nascimento']
                    if 'ano_entrada' in dados:
                        escola.ano_entrada = dados['ano_entrada']
                    
                    cursor.execute(UPDATE_ESCOLA, (escola.nome, escola.telefone, escola.email, escola.cargo, escola.data_nascimento, escola.ano_entrada))
            return jsonify({"mensagem" : "Cadastro do professor atualizado."}, escola)
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'