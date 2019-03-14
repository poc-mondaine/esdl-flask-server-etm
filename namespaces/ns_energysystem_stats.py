import logging
from flask import request
from flask_restplus import Resource
from namespaces import api

# ESDL modules
from energy_system_handler import EnergySystemHandler

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


@ns1.route('/count_pv_parcs')
class Count_PV_parcs(Resource):
    def post(self):
        request_data = request.get_data()
        request_data_string = request_data.decode()

        es = EnergySystemHandler(request_data_string)
        pv_parc_list = es.get_assets_of_type(es.esdl.PVParc)
        number_of_PV_parcs = len(pv_parc_list)

        return('Number of PV parcs: {}'.format(number_of_PV_parcs))

