from http import HTTPStatus
from flask import Blueprint
from flask_restplus import Api, Resource
from api_paises.models.paises import Paises, PaisSchema, Post_parser, Put_parser

api_v1 = Blueprint('api', __name__, url_prefix='/api/1')

api = Api(api_v1, version='1.0', title='País API', description='País API', )

ns = api.namespace('paises', description='Operações relacionadas a Países')

pais = api.model('Pais', PaisSchema)


@ns.route('/')
class PaisListaCreate(Resource):

    @api.doc('lista_paises')
    @api.marshal_list_with(pais)
    @api.response(404, 'Países não encontrados')
    def get(self):
        """
        Recupera todos os paises
        :return:
        """

        paises = (
            Paises.query.order_by('codigo').all()
        )
        return paises

    @api.doc('País salvo com sucesso')
    @api.expect(Post_parser)
    @api.marshal_with(pais, code=HTTPStatus.CREATED)
    def post(self):

        args = Post_parser.parse_args()

        novo_pais = Paises(
            codigo=args['codigo'],
            nome=args['nome'],
            sigla=args['sigla'],
            dataInicio=args['dataInicio'],
            dataFim=args['dataFim']
        )

        try:

            novo_pais.save()
            result = api.marshal(novo_pais, pais)

        except Exception as e:
            Paises.rollback()
            api.abort(409, 'País já existe')

        return result, HTTPStatus.CREATED


@ns.route('/<int:codigo>')
@api.doc(responses={404: 'País não encontrado'}, params={'codigo': 'Código de identificação do País'})
class PaisesBuscar(Resource):

    @api.doc(description='Busca país pelo código')
    @api.marshal_with(pais)
    def get(self, codigo):
        """
            Buscar país pelo código
        """
        pais = Paises.get(codigo)
        if not pais:
            # O país não foi encontrado
            api.abort(404)

        return pais

    @api.doc(responses={204: 'País excluído'})
    def delete(self, codigo):
        """
        Remove o pais
        """
        pais = Paises.get(codigo)
        if not pais:
            # O país não foi encontrado
            api.abort(404, "País {} não existe".format(codigo))

        try:

            pais.delete(pais)

        except Exception as e:
            Paises.rollback()
            api.abort(500, 'Não foi possível excluir o país')

        return '', HTTPStatus.NO_CONTENT

    @api.doc(parser=Put_parser)
    @api.marshal_with(pais)
    def put(self, codigo):
        """
        Modifica os dados do país informado
        :param codigo: Código do país a ser modificado
        :return: Retorna os dados do país com as modificações
        """
        pais_busca = Paises.get(codigo)
        if not pais_busca:
            # O país não foi encontrado
            api.abort(404, "País {} não foi encontrado".format(codigo))

        args = Put_parser.parse_args()

        _pais = Paises(
            codigo=codigo,
            nome=args['nome'],
            sigla=args['sigla'],
            dataInicio=args['dataInicio'],
            dataFim=args['dataFim']
        )

        try:

            _pais.update(_pais)

        except Exception as e:
            Paises.rollback()
            api.abort(500, 'País não foi atualizado')

        return _pais
