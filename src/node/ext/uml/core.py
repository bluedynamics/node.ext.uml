from zope.interface import implements
from zope.location import LocationIterator
from zodict.node import Node
from zodict.interfaces import IRoot
from zodict.interfaces import ICallableNode
from node.ext.uml.interfaces import IClass
from node.ext.uml.interfaces import IInterface
from node.ext.uml.interfaces import (
    IUMLElement,
    IProfile,
    IDatatype,
    IStereotype,
    ITaggedValue,
    IPackage,
    IModel,
)

import logging
log = logging.getLogger('node.ext.uml')

NODEFAULTMARKER = object()
INFINITE = object()

class UMLElement(Node):
    implements(IUMLElement, ICallableNode)

    def __call__(self):
        """Does nothing but fullfill contract.
        """
        pass

    @property
    def name(self):
        return self.__name__

    @property
    def maxoccurs(self):
        return 1

    @property
    def stereotypes(self):
        return self.filtereditems(IStereotype)

    def stereotype(self, stereotypename):
        for stereotype in self.stereotypes:
            if stereotype.name == stereotypename:
                return stereotype
        return None

class Profile(UMLElement):
    implements(IProfile)

class Stereotype(UMLElement):
    implements(IStereotype)

    def __init__(self, name=None):
        super(UMLElement, self).__init__(name)
        self._profile = None

    def _getprofile(self):
        if self._profile is not None:
            return  self.node(self._profile)
        return None

    def _setprofile(self, profileinstance):
        self._profile = profileinstance.uuid

    profile = property(_getprofile, _setprofile)

    @property
    def taggedvalues(self):
        return self.filtereditems(ITaggedValue)

    def taggedvalue(self, taggedvaluename):
        for tgv in self.taggedvalues:
            if tgv.name == taggedvaluename:
                return tgv
        return None


class TaggedValue(UMLElement):
    implements(ITaggedValue)

    """from uml reference book "tagged value: A tag-value pair attached to a
    modeling element to hold some piece of information. Each tagged value
    is shown in the form tag = value. it always is part of a stereotype."""
    value = None

class Datatype(UMLElement):
    implements(IDatatype)


class Package(UMLElement):
    implements(IPackage)

    @property
    def packages(self):
        return self.filtereditems(IPackage)

    @property
    def classes(self):
       return self.filtereditems(IClass)

    @property
    def interfaces(self):
        return self.filtereditems(IInterface)

class Model(Package):
    implements(IModel, IRoot)

    @property
    def datatypes(self):
        return self.filtereditems(IDatatype)
