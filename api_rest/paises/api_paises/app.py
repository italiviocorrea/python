from flask import Flask
from flask_migrate import Migrate
from api_paises.db import db, db_config
from api_paises.resources.paises import api_v1


def create_app():

    api = Flask(__name__)
    api.config['RESTPLUS_MASK_SWAGGER'] = False
    api.register_blueprint(api_v1)

    api.config.update(db_config)

    register_db(api)

    return api


def register_db(api):
    db.init_app(api)
    migrate = Migrate(api, db)


if __name__ == '__main__':
    api = create_app()
    api.app_context().push()
    api.run(host='0.0.0.0')
