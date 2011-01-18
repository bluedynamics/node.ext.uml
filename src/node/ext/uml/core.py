from zope.interface import implements
from zodict.node import Node
from zodict.interfaces import IRoot
from zodict.interfaces import ICallableNode
from node.ext.uml.interfaces import ModelIllFormedException
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
    IActivity,
)

import logging
log = logging.getLogger('node.ext.uml')

NODEFAULTMARKER = object()
INFINITE = object()

class UMLElement(Node):
    implements(IUMLElement, ICallableNode)

    abstract = True
    xmiid = None
    XMI = None

    def __call__(self):
        """Does nothing but fullfill contract.
        """
        pass

    @property
    def name(self):
        return self.__name__

    @property
    def normalizedname(self):
        # TODO: implement me
        # TODO: @property ok here? this returns another property...
        raise NotImplementedError

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

    def check_model_constraints(self):
        try:
            assert(not self.abstract)
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  "Cannot directly use abstract base classes"


class Profile(UMLElement):
    implements(IProfile)
    abstract = False

    # TODO: check these TODO items if they still apply

    ### TODO: let owned_stereotypes return the stereotypes defined in profile
    #def __init__(self, name):
    #    super(Profile,self).__init__(name)
    #    owned_stereotypes = dict()

    #def add_stereotype(self, name, extentended):
    #    owned_stereotypes['name'] = type(name,
    #                                     (Stereotype,),
    #                                     {'extended': extended})

    # TODO: Add check_model_constraints - profile only part of package

    # TODO: Let Profile be a Package (without attribute "activities") and let
    # profiles applied to profile to distinguish between execution-loading
    # profiles and profiles other ones.


class Stereotype(UMLElement):
    implements(IStereotype)
    abstract = False

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

    def check_model_constraints(self):
        try:
            assert(IProfile.providedBy(self.profile))
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  u"Stereotype must have a reference to its Profile"


class TaggedValue(UMLElement):
    implements(ITaggedValue)
    abstract = False

    value = None

class Datatype(UMLElement):
    implements(IDatatype)


class Package(UMLElement):
    implements(IPackage)
    abstract = False

    @property
    def packages(self):
        return self.filtereditems(IPackage)

    @property
    def classes(self):
       return self.filtereditems(IClass)

    @property
    def interfaces(self):
        return self.filtereditems(IInterface)

    @property
    def profiles(self):
        return self.filtereditems(IProfile)

    @property
    def activities(self):
        return self.filtereditems(IActivity)


class Model(Package):
    implements(IModel, IRoot)
    abstract = False

    @property
    def datatypes(self):
        return self.filtereditems(IDatatype)
