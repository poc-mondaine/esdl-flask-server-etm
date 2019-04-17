import logging
from flask import request
from flask_restplus import Resource
from namespaces import api

# ESDL modules
from esdl_handler import energy_system_handler

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

        return 'Hello, world!'


@ns1.route('/total_costs')
class Total_Costs(Resource):
    def post(self):
        request_data = request.get_data()
        request_data_string = request_data.decode()

        es = energy_system_handler.EnergySystemHandler()
        es.load_from_string(request_data_string)
        total_costs = es.get_kpi_by_name('KPI Total costs')

        return('Total costs: {}'.format(total_costs.value))

@ns1.route('/co2_emissions')
class Co2_Emissions(Resource):
    def post(self):
        request_data = request.get_data()
        request_data_string = request_data.decode()

        es = energy_system_handler.EnergySystemHandler()
        es.load_from_string(request_data_string)
        co2_emissions = es.get_kpi_by_name('KPI CO2-emissions')

        return('CO2-emissions: {}'.format(co2_emissions.value))
