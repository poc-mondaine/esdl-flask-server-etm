from time import sleep

from pyecore.resources import ResourceSet, URI
from pyecore.utils import DynamicEPackage, alias
from pyecore.resources.resource import HttpURI
from .xmlresource import XMLResource
from pyecore.notification import EObserver
import uuid
from io import BytesIO


class EnergySystemHandler:
    """Class to handle (load, read, and update) an ESDL Energy System"""

    def __init__(self):
        self.esdl, self.rset = self.init_model()
        print('\nEnergy system initialized!')


    # Creates a dict of all the attributes of an ESDL object
    @staticmethod
    def attr_to_dict(esdl_object):
        d = dict()
        d['esdlType'] = esdl_object.eClass.name
        for attr in dir(esdl_object):
            attr_value = esdl_object.eGet(attr)
            if attr_value is not None:
                d[attr] = attr_value
        return d


    # Creates a uuid: useful for generating unique IDs
    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())


    def init_model(self):
        # create a resourceSet that hold the contents of the esdl.ecore model and the instances we use/create
        rset = ResourceSet()

        # Assign files with the .esdl extension to the XMLResource instead of default XMI
        rset.resource_factory['esdl'] = lambda uri: XMLResource(uri)

        # Read the lastest esdl.ecore from github
        esdl_model_resource = rset.get_resource(HttpURI('https://raw.githubusercontent.com/EnergyTransition/ESDL/master/esdl/model/esdl.ecore'))

        esdl_model = esdl_model_resource.contents[0]
        # print('Namespace: {}'.format(esdl_model.nsURI))
        rset.metamodel_registry[esdl_model.nsURI] = esdl_model

        # Create a dynamic model from the loaded esdl.ecore model, which we can use to build Energy Systems
        esdl = DynamicEPackage(esdl_model)

        # fix python buildin 'from' that is also used in ProfileElement as attribute
        # use 'start' instead of 'from' when using a ProfileElement
        alias('start', esdl.ProfileElement.findEStructuralFeature('from'))

        # have a nice __repr__ for some ESDL classes when printing ESDL objects (includes all Assets and EnergyAssets)
        esdl.Item.python_class.__repr__ = lambda x: '{}: ({})'.format(x.name, EnergySystemHandler.attr_to_dict(x))
        esdl.Carrier.python_class.__repr__ = lambda x: '{}: ({})'.format(x.name, EnergySystemHandler.attr_to_dict(x))
        esdl.Geometry.python_class.__repr__ = lambda x: '{}: ({})'.format(x.name, EnergySystemHandler.attr_to_dict(x))
        esdl.QuantityAndUnitType.python_class.__repr__ = lambda x: '{}: ({})'.format(x.id, EnergySystemHandler.attr_to_dict(x))
        esdl.QuantityAndUnitReference.python_class.__repr__ = lambda x: '{}: ({})'.format('QuantityAndUnitReference', EnergySystemHandler.attr_to_dict(x))
        esdl.KPI.python_class.__repr__ = lambda x: '{}: ({})'.format(x.name, EnergySystemHandler.attr_to_dict(x))
        esdl.ProfileElement.python_class.__repr__ = lambda x: 'ProfileElement ({})'.format(EnergySystemHandler.attr_to_dict(x))

        return esdl, rset


    def load_energy_system(self, name):
        # create a resourceSet that hold the contents of the esdl.ecore model and the instances we use/create
        rset = ResourceSet()

        # Assign files with the .esdl extension to the XMLResource instead of default XMI
        rset.resource_factory['esdl'] = lambda uri: XMLResource(uri)

        # Read the lastest esdl.ecore from github
        esdl_model_resource = rset.get_resource(HttpURI('https://raw.githubusercontent.com/EnergyTransition/ESDL/master/esdl/model/esdl.ecore'))

        esdl_model = esdl_model_resource.contents[0]
        # print('Namespace: {}'.format(esdl_model.nsURI))
        rset.metamodel_registry[esdl_model.nsURI] = esdl_model

        # Create a dynamic model from the loaded esdl.ecore model, which we can use to build Energy Systems
        esdl = DynamicEPackage(esdl_model)

        # fix python buildin 'from' that is also used in ProfileElement as attribute
        # use 'start' instead of 'from' when using a ProfileElement
        alias('start', esdl.ProfileElement.findEStructuralFeature('from'))

        # have a nice __repr__ for some ESDL classes when printing ESDL objects (includes all Assets and EnergyAssets)
        esdl.Item.python_class.__repr__ = lambda x: '{}: ({})'.format(x.name, EnergySystemHandler.attr_to_dict(x))
        esdl.Carrier.python_class.__repr__ = lambda x: '{}: ({})'.format(x.name, EnergySystemHandler.attr_to_dict(x))
        esdl.Geometry.python_class.__repr__ = lambda x: '{}: ({})'.format(x.name, EnergySystemHandler.attr_to_dict(x))
        esdl.QuantityAndUnitType.python_class.__repr__ = lambda x: '{}: ({})'.format(x.id, EnergySystemHandler.attr_to_dict(x))
        esdl.QuantityAndUnitReference.python_class.__repr__ = lambda x: '{}: ({})'.format('QuantityAndUnitReference', EnergySystemHandler.attr_to_dict(x))
        esdl.KPI.python_class.__repr__ = lambda x: '{}: ({})'.format(x.name, EnergySystemHandler.attr_to_dict(x))
        esdl.ProfileElement.python_class.__repr__ = lambda x: 'ProfileElement ({})'.format(EnergySystemHandler.attr_to_dict(x))


        # load the ESDL file
        resource = rset.get_resource(URI(name))
        es = resource.contents[0]
        # At this point, the model instance is loaded!

        # get notifications of changes in the EnergySystem model
        #observer = PrintNotification(es)
        #observer2 = PrintNotification(es.instance[0].area)

        # also return the esdlm and rset reference, so we can create esdl classes and store them as strings
        return es, resource, esdl, rset


    # Add Energy System Information
    def add_energy_system_information(self):
        esi = self.esdl.EnergySystemInformation(id='energy_system_information')
        self.es.energySystemInformation = esi


    # Add energy system information to the energy system if it is not there yet
    # Energy System information can be used to globally define the quantity and units of this system,
    # instead of defining them manually per KPI in each area: this fosters reuse (but is not necessary)
    def get_quantity_and_units(self):
        q_and_u = None

        if self.get_by_id('energy_system_information') is None:
            self.add_energy_system_information()

            q_and_u = self.esdl.QuantityAndUnits(id='quantity_and_units')
            self.es.energySystemInformation.quantityAndUnits = q_and_u

        else:
            q_and_u = self.get_by_id('quantity_and_units')

        return q_and_u


    # Get a list of assets of a specific ESDL type in the main instance's area
    def get_assets_of_type(self, esdl_type):
        assets = []

        for current_asset in self.es.instance[0].area.asset:
            if isinstance(current_asset, esdl_type):
                assets.append(current_asset)
        return assets

    # Get a list of potentials of a specific ESDL type in the main instance's area
    def get_potentials_of_type(self, esdl_type):
        potentials = []

        for current_potential in self.es.instance[0].area.potential:
            if isinstance(current_potential, esdl_type):
                potentials.append(current_potential)
        return potentials

    # returns a generator of all assets of a specific type. Not only the ones defined in  the main Instance's Area
    # e.g. QuantityAndUnits can be defined in the KPI of an Area or in the EnergySystemInformation object
    # this function returns all of them at once
    def get_all_assets_of_type(self, esdl_type):
        return esdl_type.allInstances()


    # Using this function you can query for objects by ID
    # After loading an ESDL-file, all objects that have an ID defines are stored in resource.uuid_dict automatically
    # Note: If you add things later to the resource, it won't be added automatically to this dictionary though.
    # Use get_by_id_slow() for that
    def get_by_id(self, id):
        if id in self.resource.uuid_dict:
            return self.resource.uuid_dict[id]
        else:
            return None

    # This function iterates over all the contents of the Energy System and is much slower than get_by_id()
    def get_by_id_slow(self, id):
        for child in self.es.eAllContents():
            if hasattr(child, 'id'):
                if child.id == id:
                    return child

    # create a readable list of the attributes of an ESDL class
    def get_asset_attribute(self, esdl_type, attribute):
        asset_data = []

        for current_asset in self.es.instance[0].area.asset:

            if isinstance(current_asset, esdl_type):
                asset_data.append({
                    'name': current_asset.name,  # name
                    'attribute': {
                        'key': attribute,
                        'value': getattr(current_asset, attribute)
                    }
                })

        return asset_data


    # returns a specific KPI by id, see also get_by_id for a faster method
    def get_kpi_by_id(self, id):
        for kpi in self.es.instance[0].area.KPIs.kpi:
            if kpi.id == id:
                return kpi


    # returns a specific KPI by name
    def get_kpi_by_name(self, name):
        for kpi in self.es.instance[0].area.KPIs.kpi:
            if kpi.name == name:
                return kpi


    # save the resource
    def save(self, filename):
        uri = URI(filename)
        fileresource = self.rset.create_resource(uri)
        # add the current energy system
        fileresource.append(self.es)
        # save the resource
        fileresource.save()


    # get the energy system as a XML String
    # does not change the 'active' resource
    # so save() will still save as a file
    def get_as_string(self):
        # to use strings as resources, we simulate a string as being a file
        uri = StringURI('anyname.esdl')
        # create the string resource
        #stringresource = self.rset.create_resource(uri)
        # add the current energy system
        #stringresource.append(self.es)
        # save the resource
        self.resource.save(uri)
        # remove the temporary resource in the resource set
        #self.rset.remove_resource(stringresource)
        # return the string
        return uri.getvalue()

    # load an EnergySystem from a string (using UTF-8 encoding)
    def load_from_string(self, string):
        uri = StringURI('loadfromstring', string)
        # this overrides the current loaded resource
        self.resource = self.rset.create_resource(uri)
        self.resource.load()
        self.es = self.resource.contents[0]
        return self.es


class PrintNotification(EObserver):
    def __init__(self, notifier=None):
        super().__init__(notifier=notifier)

    def notifyChanged(self, notification):
        print('Notification: {}'.format(notification))


class StringURI(URI):
    def __init__(self, uri, text=None):
        super(StringURI, self).__init__(uri)
        if text is not None:
            self.__stream = BytesIO(text.encode('UTF-8'))

    def getvalue(self):
        readbytes = self.__stream.getvalue()
        # somehow stringIO does not work, so we use BytesIO
        string = readbytes.decode('UTF-8')
        return string

    def create_instream(self):
        return self.__stream

    def create_outstream(self):
        self.__stream = BytesIO()
        return self.__stream
