import logging
from flask_restplus import Resource
from restplus import api

log = logging.getLogger(__name__)
ns1 = api.namespace('EnergySystemStats', description='ESDL EnergySystem Statistics')

# @ns1.route('/<area_type>/<area_id>')
@ns1.route('/')
class EnergySystem_Statistics(Resource):
    #def get(self, area_type, area_id):
    def get(self):
        """
        Gives statistics about an energy system
        :return: Welcome message
        """
        # :param area_type: the area type (e.g. municipality)

        return 'Hello world'


