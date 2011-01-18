"""Literature:
[1] OMG Unified Modeling LanguageTM (OMG UML), Superstructure. Version 2.2.

[2] The Unified Modeling Language Reference Manual Second Edition.
James Rumbaugh, Ivar Jacobson, Grady Booch. Addison-Wesley, 2005

[3] Unified Modeling Language Specification (version 2.1)
"""

from zope.interface import Attribute
from zodict.interfaces import INode
from zodict.interfaces import ILeaf
from zodict.interfaces import IRoot

###############################################################################
# Base Element
###############################################################################

class IUMLElement(INode):
    """An XMI Element.
    """
    XMI = Attribute(u"the current IXMIFlavor instance")
    xmiid = Attribute(u"XMI identifier as string")
    normalizedname = Attribute(u"Cleaned name of UML element name consists "
                                "of [a..z A..Z 0..9 _] and does not start with "
                                "[0..9].")
    name = Attribute(u"The name under which the Element is known")
    maxoccurs = Attribute(u"UML: maximum occurencies. integer expected.")
    iscomplex = Attribute(u"UML: complex or not. boolean expected")

    # convenience
    stereotypes = Attribute(u'list of INode filtered contained stereotypes')

    def stereotype(name):
        """returns stereotype by name."""

###############################################################################
# Generic elements specific to profile
###############################################################################

class IProfile(IUMLElement):
    """UML Profile
    """

class IDatatype(IUMLElement, ILeaf):
    """UML datatype.
    """

class IStereotype(IUMLElement):
    """UML stereotype
    """
    profile = Attribute(u"UID of UML profile this stereotype belongs to.")
    taggedvalue = Attribute(u"List of ITaggedvalue  filtered contained tagged"
                             "values.")

    def taggedvalue(name):
        """returns tagged value by tag name.
        """

class ITaggedValue(IUMLElement, ILeaf):
    """UML tagged value.
    """

    value = Attribute(u"The value")


###############################################################################
# Elements for Class Diagram
###############################################################################

class IPackage(IUMLElement):
    """An UML Package element.
    """
    umlprofile = Attribute(u"list of UML profiles loaded with this package")

    # convenience
    packages = Attribute(u'list of INode filtered contained packages')
    classes = Attribute(u'list of INode filtered contained classes')
    interfaces = Attribute(u'list of INode filters contained classes')

class IModel(IPackage, IRoot):
    """UML Model Element.
    """
    # convenience
    datatypes = Attribute(u'list of (INode filtered) contained datatypes')

class IClass(IUMLElement):
    """UML Class Element.

    A class describes a set of objects that share the same specifications of\
    features, constraints, and semantics. ([1], pg. 49)

    ================================ ===================================
    UML2.2 Associations              AGX implementation
    -------------------------------- -----------------------------------
    nestedClassifier: Classifier [*] none
    ownedAttribute : Property [*]    attributes
    ownedOperation : Operation [*]   operations/ methods/ other behavior
    / superClass : Class [*]         i.e. python: __class__.__bases__
    ================================ ===================================

    From Classifier (from Kernel, Dependencies, PowerTypes):
    isAbstract: Boolean
    """
    isAbstract = Attribute(u'If true, the Classifier does not provide a\
                             complete declaration and can typically not be\
                             instantiated.')
    operations = Attribute(u'list of INode filters contained operation')
    attributes = Attribute(u'list of INode filters contained attributes')

class IInterface(IUMLElement):
    """UML Interface Element.
    """
    # convenience
    operations = Attribute(u'list of INode filters contained operation')

class IProperty(IUMLElement):
    """UML Attribute Element
    """
    type = Attribute(u'Type of the element - usally referenced')

class IOperation(IUMLElement):
    """UML Operation Element.
    """
    parameter = Attribute(u'IOperationParameter implementing Element')

class IParameter(IUMLElement, ILeaf):
    """UML Parameter Element of Operation.
    """
    default = Attribute(u'Default value of the element, optional')
    type = Attribute(u'Type of the element - usally referenced')

###############################################################################
# Connecting Elements for Class Diagram
###############################################################################

class IGeneralization(IUMLElement):
    """UML Generalization Element.

    see [3], pg. 71

    A generalization is a taxonomic relationship between a more general
    classifier and a more specific classifier. Each instance of the specific
    classifier is also an indirect instance of the general classifier. Thus,
    the specific classifier inherits the features of the more general
    classifier.

    An owned element of of some classifier.
    """
    specific = Attribute(u'References the specializing classifier in the '
                          'Generalization relationship. Subsets '
                          'DirectedRelationship::source and Element::owner')
    general = Attribute(u'References the general classifier in the '
                         'Generalization relationship. Subsets '
                         'DirectedRelationship::target')

class IInterfaceRealization(IUMLElement):
    """UML InterfaceRealization Element.

    see [3], pg. 89

    An InterfaceRealization is a specialized Realization relationship between a
    Classifier and an Interface. This relationship signifies that the realizing
    classifier conforms to the contract specified by the Interface.
    """
    contract = Attribute(u'References the Interface specifying the conformance '
                          'contract. (Subsets Dependency::supplier).')
    implementingClassifier = Attribute(u'References the BehavioredClassifier '
                                        'that owns this Interfacerealization '
                                        '(i.e., the classifier that realizes '
                                        'the Interface to which it points). '
                                        '(Subsets Dependency::client, '
                                        'Element::owner.')


class IAssociation(IUMLElement):
    """ UML Association Element.

    see [3], pg. 39

    "An association describes a set of tuples whose values refer to typed
    instances. An instance of an association is called a link."

    The association itself is very general. It can be a simple association, a
    navigable association, a shared or composite aggregation (and more).

    It can be member of a classifier or part of a package, dependend on its
    usage.
    """

    memberEnds = Attribute(u"Each end represents participation of instances of "
                            "the classifier connected to the end in links of "
                            "the association. This is an ordered association. "
                            "Subsets Namespace::member.")

    ownedEnds = Attribute(u"The ends that are owned by the association itself. "
                           "This is an ordered association. Subsets"
                           "Association::memberEnd Classifier::feature, and"
                           "Namespace::ownedMember.")

class IAssociationEnd(IUMLElement):
    """OwnedElement of Associations or Classes."""

    type = Attribute(u'Element this end points to.')

    lowervalue = Attribute(u'Multiplicity lower range')

    uppervalue = Attribute(u'Multiplicity upper range')

    navigable = Attribute(u'Indicates wether the end is navigable or not, bool')

    aggregationkind = Attribute(u"see [3], pg. 38: AggregationKind is an "
                                 "enumeration type that specifies the literals "
                                 "for defining the kind of aggregation of a "
                                 "property. Its one of the following literal "
                                 "values. shared: Indicates that the property "
                                 "has shared aggregation. composite: Indicates "
                                 "that the property is aggregated compositely, "
                                 "i.e., the composite object has responsibility"
                                 "for the existence and storage of the composed"
                                 "objects (parts).")

class IDependency(IUMLElement):
    """ UML Dependency Element.

    see [3], pg. 62

    "A dependency is a relationship that signifies that a single or a set of
    model elements requires other model elements for their specification or
    implementation. This means that the complete semantics of the depending
    elements is either semantically or structurally dependent on the definition
    of the supplier element(s).

    """

    client = Attribute(u'The element(s) dependent on the supplier element(s). '
                        'In some cases (such as a Trace Abstraction) the '
                        'assignment of direction (that is, the designation of '
                        'the client element) is at the discretion of the ',
                        'modeler, and is a stipulation. Subsets '
                        'DirectedRelationship::source.')

    supplier = Attribute(u'The element(s) independent of the client element(s), '
                          'in the same respect and the same dependency '
                          'relationship. In some directed dependency '
                          'relationships (such as Refinement Abstractions), a '
                          'common convention in the domain of class-based OO '
                          'software is to put the more abstract element in '
                          'this role. Despite this convention, users of UML '
                          'may stipulate a sense of dependency suitable for '
                          'their domain, which makes a more abstract element '
                          'dependent on that which is more specific. Subsets '
                          'DirectedRelationship::target.')
