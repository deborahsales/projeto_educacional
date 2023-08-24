import psycopg2
from flask import jsonify, request
from flask_restx import Resource
from src.server.instance import connection
from src.server.instance import server
from server.models.escola import escola, Escola

app, api = server.app, server.api

CREATE_ESCOLA = '''INSERT INTO projeto_educacional.escola (inep, nome, ano_entrada, status, tipo, 
                        dependencia, latitude, longitude, endereco, id_rede)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
READ_ESCOLA = 'SELECT * FROM projeto_educacional.escola WHERE inep = %s'
DELETE_ESCOLA = 'DELETE FROM projeto_educacional.escola WHERE inep = %s'
UPDATE_ESCOLA = '''UPDATE projeto_educacional.escola SET nome = %s, ano_entrada = %s, status = %s,
                    tipo = %s, dependencia = %s, latitude = %s, longitude = %s, endereco = %s, id_rede = %s WHERE inep = %s'''