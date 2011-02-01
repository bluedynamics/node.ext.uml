from zope.interface import implements
from node.ext.uml.core import (
    UMLElement,
    NODEFAULTMARKER,
)
from node.ext.uml.interfaces import (
    IClass,
    IInterface,
    IProperty,
    IOperation,
    IParameter,
    IGeneralization,
    IInterfaceRealization,
    IAssociation,
    IAssociationEnd,
    IDependency,
)


class Class(UMLElement):
    implements(IClass)

    isAbstract = False

    @property
    def operations(self):
        return self.filtereditervalues(IOperation)


class Interface(UMLElement):
    implements(IInterface)

    @property
    def operations(self):
        return self.filtereditervalues(IOperation)


class _TypedElement(UMLElement):

    def __init__(self, name=None):
        super(_TypedElement, self).__init__(name)
        self._type = None

    def _gettype(self):
        if self._type is not None:
            return  self.node(self._type)
        return None

    def _settype(self, typeinstance):
        self._type = typeinstance.uuid

    type = property(_gettype, _settype)


class Property(_TypedElement):
    implements(IProperty)

    def __init__(self, name=None):
        super(Property, self).__init__(name)
        self.default = NODEFAULTMARKER


class Operation(UMLElement):
    implements(IOperation)

    @property
    def parameter(self):
        return self.filtereditervalues(IParameter)


class Parameter(_TypedElement):
    implements(IParameter)

    def __init__(self, name=None):
        super(Parameter, self).__init__(name)
        self.default = NODEFAULTMARKER
        self.direction = 'in'


###############################################################################
# Elements connecting two elements below here
###############################################################################


class Generalization(UMLElement):
    implements(IGeneralization)

    def __init__(self, name=None):
        super(Generalization, self).__init__(name)
        self._general = None

    @property
    def specific(self):
        return self.__parent__

    def _getgeneral(self):
        if self._general is not None:
            return  self.node(self._general)
        return None

    def _setgeneral(self, instance):
        self._general = instance.uuid

    general = property(_getgeneral, _setgeneral)


class InterfaceRealization(UMLElement):
    implements(IInterfaceRealization)

    def __init__(self, name=None):
        super(InterfaceRealization, self).__init__(name)
        self._contract = None

    @property
    def implementingClassifier(self):
        return self.__parent__

    def _getcontract(self):
        if self._contract is not None:
            return  self.node(self._contract)
        return None

    def _setcontract(self, instance):
        self._contract = instance.uuid

    contract = property(_getcontract, _setcontract)


class Association(UMLElement):
    implements(IAssociation)

    def __init__(self, name=None):
        super(Association, self).__init__(name)
        self._memberEnds = list()

    def _getmemberEnds(self):
        return [self.node(uuid) for uuid in self._memberEnds]

    def _setmemberEnds(self, instances):
        self._memberEnds = [i.uuid for i in instances]

    memberEnds = property(_getmemberEnds, _setmemberEnds)

    @property
    def ownedEnds(self):
        return self.filtereditervalues(IAssociationEnd)


class AssociationEnd(UMLElement):
    implements(IAssociationEnd)

    SHARED = 'shared'
    COMPOSITE = 'composite'
    AGGREGATIONS = [SHARED, COMPOSITE]

    def __init__(self, name=None):
        super(AssociationEnd, self).__init__(name)
        self._type = None
        self._association = None
        self.lowervalue = None
        self.uppervalue = None
        self.aggregationkind = None
        self.navigable = False

    def _gettype(self):
        if self._type is not None:
            return self.node(self._type)
        return None

    def _settype(self, instance):
        self._type = instance.uuid

    type = property(_gettype, _settype)

    def _getassociation(self):
        if self._association is not None:
            return self.node(self._association)
        return None

    def _setassociation(self, instance):
        self._association = instance.uuid

    association = property(_getassociation, _setassociation)


class Dependency(UMLElement):
    implements(IDependency)

    def __init__(self, name=None):
        super(Dependency, self).__init__(name)
        self._client = None
        self._supplier = None

    def _getclient(self):
        if self._client is not None:
            return  self.node(self._client)
        return None

    def _setclient(self, instance):
        self._client = instance.uuid

    client = property(_getclient, _setclient)

    def _getsupplier(self):
        if self._supplier is not None:
            return  self.node(self._supplier)
        return None

    def _setsupplier(self, instance):
        self._supplier = instance.uuid

    supplier = property(_getsupplier, _setsupplier)
