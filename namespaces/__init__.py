import logging

from flask_restplus import Api
from flask_restplus import reqparse
# import settings

log = logging.getLogger(__name__)

api = Api(version='0.1', title='ESDL EnergySystem API',
          description='A first implementation of an ESDL EnergySystem webservice')

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('bool', type=bool, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page {error_msg}')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    # if not settings.FLASK_DEBUG:
    return {'message': message}, 500

