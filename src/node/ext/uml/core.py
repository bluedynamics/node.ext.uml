import logging
from plumber import plumber
from zope.interface import implementer
from node.base import OrderedNode
from node.interfaces import (
    IRoot,
    ICallable,
)
from node.behaviors import (
    Reference,
    Order,
)
from node.ext.uml.interfaces import (
    ModelIllFormedException,
    IUMLElement,
    IClass,
    IInterface,
    IProfile,
    IDatatype,
    IStereotype,
    ITaggedValue,
    IPackage,
    IModel,
    IActivity,
)


log = logging.getLogger('node.ext.uml')


NODEFAULTMARKER = object()
INFINITE = object()


@implementer(IUMLElement, ICallable)
class UMLElement(OrderedNode):
    __metaclass__ = plumber
    __plumbing__ = Reference, Order
    abstract = True
    xmiid = None
    XMI = None
    xminame=None

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
        return self.filtereditervalues(IStereotype)

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


@implementer(IProfile)
class Profile(UMLElement):
    abstract = False

    # TODO: check these TODO items if they still apply

    ### TODO: let owned_stereotypes return the stereotypes defined in profile
    #def __init__(self, name):
    #    super(Profile, self).__init__(name)
    #    owned_stereotypes = dict()

    #def add_stereotype(self, name, extentended):
    #    owned_stereotypes['name'] = type(name,
    #                                     (Stereotype,),
    #                                     {'extended': extended})

    # TODO: Add check_model_constraints - profile only part of package

    # TODO: Let Profile be a Package (without attribute "activities") and let
    # profiles applied to profile to distinguish between execution-loading
    # profiles and profiles other ones.


@implementer(IStereotype)
class Stereotype(UMLElement):
    abstract = False

    def __init__(self, name=None):
        super(Stereotype, self).__init__(name)
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
        return self.filtereditervalues(ITaggedValue)

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


@implementer(ITaggedValue)
class TaggedValue(UMLElement):
    abstract = False
    value = None


@implementer(IDatatype)
class Datatype(UMLElement):
    pass


@implementer(IPackage)
class Package(UMLElement):
    abstract = False

    @property
    def packages(self):
        return self.filtereditervalues(IPackage)

    @property
    def classes(self):
       return self.filtereditervalues(IClass)

    @property
    def interfaces(self):
        return self.filtereditervalues(IInterface)

    @property
    def profiles(self):
        return self.filtereditervalues(IProfile)

    @property
    def activities(self):
        return self.filtereditervalues(IActivity)


@implementer(IModel, IRoot)
class Model(Package):
    abstract = False

    @property
    def datatypes(self):
        return self.filtereditervalues(IDatatype)
