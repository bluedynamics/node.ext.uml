from zope.interface import implements
from node.ext.uml.interfaces import ModelIllFormedException

from node.ext.uml.interfaces import IUMLElement

from node.ext.uml.core import UMLElement

from node.ext.uml.interfaces import IAction
from node.ext.uml.interfaces import IActivity
from node.ext.uml.interfaces import IActivityEdge
from node.ext.uml.interfaces import IActivityFinalNode
from node.ext.uml.interfaces import IActivityNode
from node.ext.uml.interfaces import IBehavior
from node.ext.uml.interfaces import IConstraint
from node.ext.uml.interfaces import IControlNode
from node.ext.uml.interfaces import IDecisionNode
from node.ext.uml.interfaces import IFinalNode
from node.ext.uml.interfaces import IFlowFinalNode
from node.ext.uml.interfaces import IForkNode
from node.ext.uml.interfaces import IInitialNode
from node.ext.uml.interfaces import IJoinNode
from node.ext.uml.interfaces import IMergeNode
from node.ext.uml.interfaces import IOpaqueAction
from node.ext.uml.interfaces import IPreConstraint
from node.ext.uml.interfaces import IPostConstraint

from node.ext.uml.interfaces import IPackage


class ActivityNode(UMLElement):
    implements(IActivityNode)

    def check_model_constraints(self):
        super(ActivityNode, self).check_model_constraints()
        try:
            assert self.__parent__ is not None
            assert IActivity.providedBy(self.__parent__)
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  "An ActivityNode must have an Activity as parent"

    @property
    def activity(self):
        return self.__parent__

    # cache this
    @property
    def incoming_edges(self):
        for obj in self.activity.filtereditervalues(IActivityEdge):
            if obj.target.uuid == self.uuid:
                yield obj

    # cache this
    @property
    def outgoing_edges(self):
        for obj in self.activity.filtereditervalues(IActivityEdge):
            if obj.source.uuid == self.uuid:
                yield obj


class Action(ActivityNode):
    implements(IAction)

    # TODO: leave or remove?
    @property
    def context(self):
        return self.activity.context

    @property
    def preconditions(self):
        return self.filtereditervalues(IPreConstraint)

    @property
    def postconditions(self):
        return self.filtereditervalues(IPostConstraint)


class Behavior(UMLElement):
    implements(IBehavior)

    def __init__(self, name=None, context=None):
        self.context = context
        super(Behavior, self).__init__(name)

    @property
    def preconditions(self):
        return self.filtereditervalues(IPreConstraint)

    @property
    def postconditions(self):
        return self.filtereditervalues(IPostConstraint)


class ControlNode(ActivityNode):
    implements(IControlNode)

class FinalNode(ControlNode):
    implements(IFinalNode)

    def check_model_constraints(self):
        super(FinalNode, self).check_model_constraints()
        try:
            assert list(super(FinalNode, self).outgoing_edges) == []
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  u"FinalNode cannot have outgoing edges"

### CONCRETE CLASSES
class Activity(Behavior):
    implements(IActivity)
    abstract = False

    def check_model_constraints(self):
        super(Activity, self).check_model_constraints()
        try:
            assert(IPackage.providedBy(self.package))
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  "An activity must have exactly one package as parent."

    @property
    def package(self):
        return self.__parent__

    @property
    def nodes(self):
        return self.filtereditervalues(IActivityNode)

    @property
    def edges(self):
        return self.filtereditervalues(IActivityEdge)

    # Convinience method, not defined by UML 2.2 specification
    @property
    def actions(self):
        return self.filtereditervalues(IAction)


class OpaqueAction(Action):
    implements(IOpaqueAction)
    abstract = False


class ActivityEdge(UMLElement):
    implements(IActivityEdge)
    abstract = False

    def check_model_constraints(self):
        super(ActivityEdge, self).check_model_constraints()
        try:
            assert self.source or self.target is not None
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  "An ActivityEdge must have source and target set"

        # [1]
        try:
            assert self.source.activity is self.target.activity
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  "Source and target must be in the same activity"

        # [2]
        try:
            assert self.__parent__ is not None
            assert IActivity.providedBy(self.__parent__)
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  "An ActivityEdge must have an Activity as parent"

        try:
            assert IActivityNode.providedBy(self.source)
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  "An ActivityEdge must have an ActivityNode as source"

        try:
            assert IActivityNode.providedBy(self.target)
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  "An ActivityEdge must have an ActivityNode as target"

    source_uuid = None
    target_uuid = None

    def __init__(self, name=None, source=None, target=None, guard=None):
        # TODO: bool(source) evals to False if IControlNode.providedBy(source)
        if IActivityNode.providedBy(source):
            self.source = source
        if IActivityNode.providedBy(target):
            self.target = target
        self.guard = guard
        super(ActivityEdge, self).__init__(name)

    @property
    def activity(self):
        return self.__parent__

    def get_source(self):
        return self.node(self.source_uuid)
    def set_source(self, source):
        # TODO: invalidate cache key for target's outgoingEdges method
        self.source_uuid = source.uuid
    source = property(get_source, set_source)

    def get_target(self):
        return self.node(self.target_uuid)
    def set_target(self, target):
        # TODO: invalidate cache key for target's incomingEdges method
        self.target_uuid = target.uuid
    target = property(get_target, set_target)


### Initial and final
class InitialNode(ControlNode):
    implements(IInitialNode)
    abstract = False

    def check_model_constraints(self):
        super(InitialNode, self).check_model_constraints()
        # [1]
        try:
            assert list(super(InitialNode, self).incoming_edges) == []
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  u"InitialNode cannot have incoming edges"

class ActivityFinalNode(FinalNode):
    implements(IActivityFinalNode)
    abstract = False

class FlowFinalNode(FinalNode):
    implements(IFlowFinalNode)
    abstract = False

### More control nodes
class DecisionNode(ControlNode):
    implements(IDecisionNode)
    abstract = False

    def check_model_constraints(self):
        super(DecisionNode, self).check_model_constraints()
        # [1]
        try:
            assert len(list(self.incoming_edges)) is 1
            assert len(list(self.outgoing_edges)) >= 1
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  "A DecisionNode has one incoming edge and at least"\
                  "one outgoing edge."


class ForkNode(ControlNode):
    implements(IForkNode)
    abstract = False

    def check_model_constraints(self):
        super(ForkNode, self).check_model_constraints()
        # [1]
        try:
            assert len(list(self.incoming_edges)) is 1
            assert len(list(self.outgoing_edges)) >= 1
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  "A ForkNode has one incoming edge and at least "\
                  "one outgoing edge."


class JoinNode(ControlNode):
    implements(IJoinNode)
    abstract = False

    def check_model_constraints(self):
        super(JoinNode, self).check_model_constraints()
        # [1]
        try:
            assert len(list(self.incoming_edges)) >= 1
            assert len(list(self.outgoing_edges)) is 1
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  u"A join node has one outgoing edge and at least "\
                  u"one incoming edge."


# TODO: UML2's MergeNode behavior does not reduce concurrency
# here the concurrency is reduced if 2 tokens come into the node
# at a time. THIS SHOULD BE CHANGED...
class MergeNode(ControlNode):
    implements(IMergeNode)
    abstract = False

    def check_model_constraints(self):
        super(MergeNode, self).check_model_constraints()
        # [1]
        try:
            assert len(list(self.incoming_edges)) >= 1
            assert len(list(self.outgoing_edges)) is 1
        except AssertionError:
            raise ModelIllFormedException,\
                  str(self) +  " " +\
                  u"A merge node has one outgoing edge and at least"\
                  u"one incoming edge."


### Constraints
class Constraint(UMLElement):
    implements(IConstraint)
    abstract = False

    def __init__(self, name=None, specification=None):
        self.specification = specification
        super(Constraint, self).__init__(name)

    @property
    def constrained_element(self):
        return self.__parent__

class PreConstraint(Constraint):
    implements(IPreConstraint)
    abstract = False

class PostConstraint(Constraint):
    implements(IPostConstraint)
    abstract = False


def validate(node):
    """Recursive model validation
    """
    if IUMLElement.providedBy(node):
        node.check_model_constraints()
    for sub in node.filtereditervalues(IUMLElement):
        validate(sub)

def get_element_by_xmiid(node, xmiid):
    if node.xmiid == xmiid:
        return node
    # TODO: may not get all elements if an INode but not IUMLElement providing
    # element sits within the hierachy
    for el in node.filtereditervalues(IUMLElement):
        ele = get_element_by_xmiid(el, xmiid)
        if ele is not None:
            return ele
    return None
