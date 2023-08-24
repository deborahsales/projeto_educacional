import psycopg2
from flask import jsonify, request
from flask_restx import Resource
from src.server.instance import connection
from src.server.instance import server
from server.models.professor import professor, Professor

app, api = server.app, server.api

CREATE_PROFISSIONAL = 'INSERT INTO projeto_educacional.profissional (cpf, nome, telefone, email, cargo, data_nascimento, ano_entrada) VALUES (%s, %s, %s, %s, %s, %s, %s)'
CREATE_PROFESSOR = 'INSERT INTO projeto_educacional.professor VALUES (%s)'
READ_PROFESSOR = 'SELECT * FROM projeto_educacional.professor WHERE cpf = %s'
DELETE_PROFISSIONAL = 'DELETE FROM projeto_educacional.profissional WHERE cpf = %s'

@api.route('/prof')
class prof(Resource):
    def create_prof(self):
        dados = request.get_json()
        cpf = dados.get('cpf')
        nome = dados.get('nome')
        telefone = [dados.get('telefone')]
        email  = [dados.get('email')]
        cargo = dados.get('cargo')
        data_nascimento = dados.get('data_nascimento')
        ano_entrada = dados.get('ano_entrada')
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_PROFISSIONAL, (cpf, nome, telefone, email, cargo, data_nascimento, ano_entrada))
                    cursor.execute(CREATE_PROFESSOR, (cpf,))
            return f'Professor cadastrado'
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
        
    def read_prof():
        dados = request.get_json()
        cpf = dados.get('cpf')
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(READ_PROFESSOR, (cpf,))
                    professor = cursor.fetchone()
            if professor == None:
                return f'professor {cpf} não encontrado'
            else:
                return jsonify(professor)
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
        
    def delete_prof():
        dados = request.get_json()
        cpf = dados.get('cpf')
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(DELETE_PROFISSIONAL, (cpf,))
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
        
    def update_prof():
        dados = request.get_json()
        cpf = dados.get('cpf')
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(READ_PROFESSOR, (cpf,))
                    professor = cursor.fetchone()
                if professor == None:
                    return f'professor {cpf} não encontrado'
                else:
                    # Ainda será necessário verificar funcionamento da variável 'professor', se é possível acessar dessa forma seus atributos
                    if 'nome' in dados:
                        professor.nome = dados['nome']
                    if 'telefone' in dados:
                        professor.telefone = dados['telefone']
                    if 'email' in dados:
                        professor.email = dados['email']
                    if 'data_nascimento' in dados:
                        professor.data_nascimento = dados['data_nascimento']
                    if 'ano_entrada' in dados:
                        professor.ano_entrada = dados['ano_entrada']
                    
                    return f'Professor atualizado.'
                    
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
    
