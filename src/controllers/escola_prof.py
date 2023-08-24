import psycopg2
from flask import jsonify, request
from flask_restx import Resource
from src.server.instance import connection
from src.server.instance import server
from server.models.escola_prof import escola_prof, EscolaProf

app, api = server.app, server.api

CREATE_PROFISSIONAL = 'INSERT INTO projeto_educacional.profissional (cpf, nome, telefone, email, cargo, data_nascimento, ano_entrada) VALUES (%s, %s, %s, %s, %s, %s, %s)'
CREATE_PROFESSOR = 'INSERT INTO projeto_educacional.professor VALUES (%s)'
READ_PROFESSOR = 'SELECT * FROM projeto_educacional.professor WHERE cpf = %s'
DELETE_PROFISSIONAL = 'DELETE FROM projeto_educacional.profissional WHERE cpf = %s'