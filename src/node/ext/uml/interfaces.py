"""Literature:
[1] OMG Unified Modeling LanguageTM (OMG UML), Superstructure. Version 2.2.

[2] The Unified Modeling Language Reference Manual Second Edition.
James Rumbaugh, Ivar Jacobson, Grady Booch. Addison-Wesley, 2005

[3] Unified Modeling Language Specification (version 2.1)
"""
from zope.interface import Attribute
from node.interfaces import (
    INode,
    ILeaf,
    IRoot,
)


class UMLException(Exception):
    """Generic UML Exception.
    """


class ModelIllFormedException(UMLException):
    """UML Exception for invalid models.
    """


###############################################################################
# Base Element
###############################################################################


class IUMLElement(INode):
    """An XMI Element.
    """
    XMI = Attribute(u"the current IXMIFlavor instance")
    xmiid = Attribute(u"XMI identifier as string")
    xminame=Attribute(u"XMI name, should be used as canonical name for code generation")
    normalizedname = Attribute(u"Cleaned name of UML element name consists "
                                "of [a..z A..Z 0..9 _] and does not start with "
                                "[0..9].")
    maxoccurs = Attribute(u"UML: maximum occurencies. integer expected.")
    iscomplex = Attribute(u"UML: complex or not. boolean expected")
    # convenience
    stereotypes = Attribute(u'list of INode filtered contained stereotypes')

    def stereotype(name):
        """returns stereotype by name."""

    def check_model_constraints(self):
        """Since some rules cannot be evaluated at instantiation time this
        function should be called on model elements by the interpreter when
        building the concrete model.

        Don't confuse this with "Constraint" from UML specification

        All "check_model_constraints" methods  through the whole inheritance
        hierarchy should be called. It's up to the implementation to call the
        superclass' "check_model_constraints" implementation.

        For example, consider a model element which must have a parent:
            node['element'] = Element()
        Element does not have a parent at instatiation time.
        """
        # TODO: adapterize, utilitize or do anythin' or leave me as is.


###############################################################################
# Generic elements specific to profile
###############################################################################


class IProfile(IUMLElement):
    """UML Profile.
    """


class IDatatype(IUMLElement, ILeaf):
    """UML datatype.
    """


class IStereotype(IUMLElement):
    """UML stereotype

    From uml reference book "tagged value: A tag-value pair attached to a
    modeling element to hold some piece of information. Each tagged value
    is shown in the form tag = value. it always is part of a stereotype.
    """
    profiles = Attribute(u"UID of UML profile this stereotype belongs to.")
    taggedvalues = Attribute(u"List of ITaggedvalue  filtered contained tagged"
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
    profiles = Attribute(u"list of UML profiles loaded with this package")
    # convenience
    packages = Attribute(u'list of INode filtered contained packages')
    classes = Attribute(u'list of INode filtered contained classes')
    interfaces = Attribute(u'list of INode filters contained classes')
    activities = Attribute(u'List of IActivities defined in the package')


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


class IActivityEdge(IUMLElement):
    """Abstract Base Class
    An activity edge is an abstract class for directed connections between two
    activity nodes. ([1], pg. 325)

    A sequencing relationship between two activity nodes, possibly including
    data. ([2], pg. 157)
    """
    activity = Attribute(u'Activity containing the edge. Computed property')
    source = Attribute(u'Node from which tokens are taken when they traverse '
                       u'the edge. Provices IActivityNode objects.')
    target = Attribute(u'Node to which tokens are put when they traverse the '
                       u'edge. Provices IActivityNode objects.')
    guard = Attribute(u'Specification evaluated at runtime to determine if '
                      u'the edge can be traversed. A python expression which '
                      u'must evaluate to True')


class IActivityNode(IUMLElement):
    """Abstract Base Class
    An activity node is an abstract class for points in the flow of an
    activity connected by edges. ([1], 333)

    A kind of element in an activity that can be connected by flows. This
    is an abstract element type whose specific varieties include actions,
    control nodes, object nodes (including pins and parameter nodes), and
    structured nodes. ([2], 159ff)
    """
    activity = Attribute(u'Activity the ActivityNode belongs to. Computed '
                         u'property')
    incoming_edges = Attribute(u'Edges that have the node as target. Computed '
                               u'property')
    outgoing_edges = Attribute(u'Edges that have the node as source. Computed '
                               u'property')


class IAction(IActivityNode):
    """Abstract Base Class
    A primitive activity node whose execution results in a change in the
    state of the system or the return of a value. ([2], pg.136)
    """
    context = Attribute(u'The classifier that owns the behavior of which this '
                        u'action is a part. Computed.')
    preconditions = Attribute(u'Constraint that must be satisfied when '
                              u'execution is started. List of IConstraints.')
    postconditions = Attribute(u'Constraint that must be satisfied when '
                               u'execution is completed. List of IConstraints.')


class IBehavior(IUMLElement):
    """Abstract Base Class
    Behavior is a specification of how its context classifier changes state
    over time. ([1], 430)

    A specification of how the state of a classifier changes over time. Behavior
    is specialized into activity, interaction, and state machine. A behavior
    describes the dynamics of an entire classifier as a unit. ([2], 190)
    """
    context = Attribute(u'The classifier that is the context for the '
                        u'execution of the behavior.')
    preconditions = Attribute(u'List of IConstraints which must evaluate '
                              u'to True when the behavior is invoked.')
    postconditions = Attribute(u'List of IConstraints which must evaluate '
                               u'to True when the behavior is completed.')


class IControlNode(IActivityNode):
    """Abstract Base Class
    A control node is an abstract activity node that coordinates flows in an
    activity. ([1], pg.356)
    """


class IFinalNode(IControlNode):
    """Abstract Base Class
    A final node is an abstract control node at which a flow in an activity
    stops. ([1], pg.373)
    """
    outgoing_edges = Attribute(u'Is always empty.')


class IActivity(IBehavior):
    """An activity is the specification of parameterized behavior as the
    coordinated sequencing of subordinate units whose individual elements are
    actions. ([1], 315)

    A specification of executable behavior as the coordinated sequential and
    concurrent execution of subordinate units, including nested activities and
    ultimately individual actions connected by flows from outputs of one node
    to inputs of another. Activities can be invoked by actions and as
    constituents of other behaviors, such as state machine transitions.
    ([2], 149ff)
    """
    nodes = Attribute(u'Nodes coordinated by the activity. List of '
                      u'IActivityNode providing objects, Owned.')
    edges = Attribute(u'Edges expressing flow between nodes of the activity.'
                      u'List of IEdge providing objects, Owned.')
    # convinience accessor
    actions = Attribute(u'List of IAction providing objects, Owned')


class IOpaqueAction(IAction):
    """An action with implementation-specific semantics. ([1], pg.262)

    A primitive activity node whose execution results in a change in the
    state of the system or the return of a value. ([2], pg.136)
    """


class IInitialNode(IControlNode):
    """An initial node is a control node at which flow starts when the activity
    is invoked. ([1], pg.378)

    [1], pg. 378 does not define the constraint that initial nodes can only have
    one outgoing edge but [2], pg. 392 makes such a definition.
    """
    incoming_edges = Attribute(u'Is always empty.')


class IActivityFinalNode(IFinalNode):
    """An activity final node is a final node that stops all flows in an
    activity. ([1], pg. 330)

    A node in an activity specification whose execution causes the forced
    termination of all flows in the activity and the termination of execution
    of the activity. ([2], pg.158)
    """


class IFlowFinalNode(IFinalNode):
    """A flow final node is a final node that terminates a flow. ([1], pg.375)
    """


class IDecisionNode(IControlNode):
    """A decision node is a control node that chooses between outgoing flows.
    ([1], pg. 360)
    """


class IForkNode(IControlNode):
    """A fork node is a control node that splits a flow into multiple concurrent
    flows. ([1], pg. 376)
    """


class IJoinNode(IControlNode):
    """A join node is a control node that synchronizes multiple flows. ([1],
    pg. 381)
    """


class IMergeNode(IControlNode):
    """A merge node is a control node that brings together multiple alternate
    flows. It is not used to synchronize concurrent flows but to accept one
    among several alternate flows. ([1], pg. 387)
    """


# TODO: decide wether to use IConstraint for guard conditions or not
class IConstraint(IUMLElement):
    """UML: A constraint is a condition or restriction expressed in natural
    language text or in a machine readable language for the purpose of declaring
    some of the semantics of an element. ([1], pg. 58)

    A constraint is a condition or restriction expressed as Python code.
    The constraint's expression must evaluate to Boolean True to fullfill the
    constraint. The context of the constraint is the element which references
    the constraint and for which the rule apply. A constraint has access to all
    Attributes the context provides.
    """
    specification = Attribute(u"The python expression which must be fulfilled.")
    constrained_element = Attribute(u"The element which references the "
                                    u"constraint. This element is the "
                                    u"constraint's context.")


class IPreConstraint(IConstraint):
    """Marker interface for conditions which must be evaluated before any other
    operations.
    """


class IPostConstraint(IConstraint):
    """Marker interface for conditions which must be evaluated at the end of
    an Activity or after an actions was executed.
    """
