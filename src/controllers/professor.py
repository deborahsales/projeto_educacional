import psycopg2
from flask import jsonify, request
from flask_restx import Resource
from src.server.instance import connection
from src.server.instance import server
from src.server.models.professor import professor, Professor

app, api = server.app, server.api

CREATE_PROFISSIONAL = '''INSERT INTO projeto_educacional.profissional (cpf, nome, cargo, data_nascimento, ano_entrada) 
                        VALUES (%s, %s, %s, %s, %s)'''
CREATE_PROFESSOR = 'INSERT INTO projeto_educacional.professor VALUES (%s)'
READ_PROFESSOR = '''SELECT profi.* FROM projeto_educacional.professor profe 
                    INNER JOIN projeto_educacional.profissional profi USING (cpf) WHERE profe.cpf = %s'''
DELETE_PROFISSIONAL = 'DELETE FROM projeto_educacional.profissional WHERE cpf = %s'
SQL_UPDATE = 'UPDATE projeto_educacional.profissional SET '


@api.route('/prof')
class Prof(Resource):
    def post(self):
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
                    connection.autocommit = False
                    cursor.execute(CREATE_PROFISSIONAL, (cpf, nome, cargo, data_nascimento, ano_entrada))
                    cursor.execute(CREATE_PROFESSOR, (cpf,))
                    connection.commit
            return f'Professor cadastrado com sucesso.'
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'

    def get(self):
        dados = request.get_json()
        cpf = dados['cpf']
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(READ_PROFESSOR, (cpf,))
                    professor = cursor.fetchone()
            if professor == None:
                return f'Professor {cpf} não encontrado.'
            else:
                return jsonify(professor)
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
        
    def delete(self):
        dados = request.get_json()
        cpf = dados.get('cpf')
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(DELETE_PROFISSIONAL, (cpf,))
            return 'Professor excluído com sucesso.'
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
        
    def put(self):
        dados = request.get_json()
        cpf = dados.get('cpf')
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(READ_PROFESSOR, (cpf,))
                    professor = cursor.fetchone()
                if professor == None:
                    return f'Professor {cpf} não encontrado.'
                else:
                    primeiro = True
                    sql = SQL_UPDATE
                    if 'nome' in dados:
                        sql += f"nome = '{dados.get('nome')}'"
                        primeiro = False
                    if 'telefone' in dados:
                        if (not primeiro):
                            sql += ', '
                        sql += "telefone = '{" + dados.get('telefone') + "}'"
                        primeiro = False
                    if 'email' in dados:
                        if (not primeiro):
                            sql += ', '
                        sql += "email = '{" + dados.get('email') + "}'"
                        primeiro = False
                    if 'cargo' in dados:
                        if (not primeiro):
                            sql += ', '     
                        sql += f"cargo = '{dados.get('cargo')}'"
                        primeiro = False
                    if 'data_nascimento' in dados:
                        if (not primeiro):
                            sql += ', '
                        sql += f"data_nascimento = '{dados.get('data_nascimento')}'"
                        primeiro = False
                    if 'ano_entrada' in dados:
                        if (not primeiro):
                            sql += ', '
                        sql += f"ano_entrada =  '{str(dados.get('ano_entrada'))}'"

                    sql += ' WHERE cpf = ' + dados.get('cpf')
                    with connection.cursor() as cursor:
                        cursor.execute(sql)
            return jsonify("Cadastro do professor atualizado com sucesso.")
        except psycopg2.IntegrityError as e:
            return f'Erro de integridade: {e}'
        except psycopg2.Error as e:
            return f'Erro no banco de dados: {e}'
        except Exception as e:
            return f'Erro inesperado: {e}'
    
