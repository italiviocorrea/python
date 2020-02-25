from flask_restplus import fields, reqparse, inputs
from api_paises.db import db

PaisSchema = {
    'codigo': fields.Integer(required=True, description='Código identificador do país'),
    'nome': fields.String(required=True, description='Nome do País'),
    'sigla': fields.String(required=True, description='Sigla do País'),
    'dataInicio': fields.Date(required=True, description='Data de Início de Vigência'),
    'dataFim': fields.Date(required=False, description='Data Fim da vigência'),
}

Put_parser = reqparse.RequestParser()
Put_parser.add_argument('nome',
                        type=str,
                        required=True,
                        help='Nome do País',
                        location='form')
Put_parser.add_argument('sigla',
                        type=str,
                        required=True,
                        help='Sigla do País',
                        location='form')
Put_parser.add_argument('dataInicio',
                        type=inputs.date_from_iso8601,
                        required=True,
                        help='Data de inicio de vigência',
                        location='form')
Put_parser.add_argument('dataFim',
                        type=inputs.date_from_iso8601,
                        required=False,
                        help='Data Final de vigência',
                        location='form')

Post_parser = Put_parser.copy()
Post_parser.add_argument('codigo', type=int,
                         required=True,
                         help='Código de identificação do País',
                         location='form')


class Paises(db.Model):
    __tablename__ = 'paises'

    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(32), nullable=False)
    sigla = db.Column(db.String(3), nullable=False)
    dataInicio = db.Column(db.Date(), nullable=False)
    dataFim = db.Column(db.Date(), nullable=True)

    @classmethod
    def get(cls, codigo):
        return cls.query.filter_by(codigo=codigo).first()

    @classmethod
    def getAll(cls, page_size, page_current):
        return cls.query.paginate(page_size, page_current)
    
    @classmethod
    def save(cls):
        """
        Insere a entidade passada como parametro no banco de dados.
        :param cls: Entidade a ser inserido no banco de dados.
        :return: retorna a entidade inserida com todos os dados, em caso de sucesso.
        """

        db.session.add(cls)
        db.session.commit()

        return cls

    @classmethod
    def update(cls,entity):
        """
        Confirma a atualizacao da entidade no banco de dados.
        """
        db.session.merge(entity)
        db.session.commit()

        return entity

    @classmethod
    def rollback(cls):
        """
        Cancela a atualizacao da entidade no banco de dados, caso ocorra algum erro.
        """
        db.session.rollback()

    @staticmethod
    def delete(entity):
        """
        Remove a entidade no banco de dados.
        """
        db.session.delete(entity)
        db.session.commit()
