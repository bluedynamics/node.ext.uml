Literature:
[1] OMG Unified Modeling LanguageTM (OMG UML), Superstructure. Version 2.2.
[2] The Unified Modeling Language Reference Manual Second Edition.
    James Rumbaugh, Ivar Jacobson, Grady Booch. Addison-Wesley, 2005


class IActivityEdge
===================


Generalizations not covered
---------------------------

-  RedefinableElement (from Kernel)


Associations not covered
------------------------

- /inGroup : ActivityGroup[0..*]
- redefinedEdge: ActivityEdge [0..*]
- inPartition : Partition [0..*]
- inStructuredNode : StructuredActivityNode [0..1]
- interrupts : InterruptibleActivityRegion [0..1]
- weight : ValueSpecification [1..1] = 1 (weight always 1)


Associations
------------

- source : ActivityNode [1..1]
  source : IActivityNode [1..1]
- target : ActivityNode [1..1]
  target : IActivityNode [1..1]


Associations different from specification
-----------------------------------------

- activity : Activity[0..1]
  activity : IActivity [1]
- guard : ValueSpecification [1..1] = true
  #guard : IConstraint[0..1] = true
  guard : String[0..1]


Constraints not covered
-----------------------

Package CompleteStructuredActivities: [1]


Constraints
-----------

[1] The source and target of an edge must be in the same activity as the edge.


Constraints different from specification
----------------------------------------

[2] Activity edges must be owned by activities and only by them.


class IActivityNode
===================


Associations not covered
------------------------

- /inGroup : Group [0..*]
- redefinedNode : ActivityNode [0..*]
- inPartition : Partition [0..*]
- inInterruptibleRegion : InterruptibleActivityRegion [0..*]
- inStructuredNode : StructuredActivityNode [0..1]


Associations different from specification
-----------------------------------------

- activity : Activity[0..1]
  activity : Activity [1]
- incoming : ActivityEdge [0..*]
  incoming_edges : IActivityEdge [0..*]
- outgoing : ActivityEdge [0..*]
  outgoing_edges : IActivityEdge [0..*]


Constraints different from specification
----------------------------------------
[1] Activity nodes can only be owned by activities.


class IAction
=============


Generalizations not covered
---------------------------
- ExecutableNode (from ExtraStructuredActivities, StructuredActivities)
  Exception handler usage not covered yet.


Associations not covered
------------------------

- /input : InputPin [*]
- /output : OutputPin [*]


Associations different from specification
-----------------------------------------

- /context : Classifier [0..1]
  context : object [0..1]
- localPreconditions : Constraint [0..*]
  preconditions : IPreConstraint [0..*]
- localPostconditions : Constraint [0..*]
  postconditions : IPostConstraint [0..*]


class IBehavior
===============


Attributes not covered
----------------------

- isReentrant: Boolean [1]
  Invocation while still executing from previous invocation not allowed.


Associations not covered
------------------------

- specification: BehavioralFeature [0..1]
  There is always a special invocation of behavior. Passing parameters
  through the calling method is not supported and not needed because the
  behavior has access to any attribute of it's context.
- ownedParameter: Parameter
  Parameters are available by the context.
- redefinedBehavior: Behavior


Associations different from specification
-----------------------------------------

- /context: BehavioredClassifier [0..1]
  /context: object[0..1]
- precondition: Constraint
  preconditions: IPreConstraint
- postcondition: Constraint
  postconditions: IPostConstraint


Constraints not covered
-----------------------

[1], [2], [3], [4]


class IControlNode
==================


class IFinalNode
================


class IPackage
==============


Generalizations not covered
---------------------------

- Namespace (from Kernel)
- PackageableElement (from Kernel)


Assoziations not covered
------------------------

- /nestedPackage
- /packagedElement
- /ownedType
- packageMerge
- nestingPackage


Constraints not covered
-----------------------

- [1] If an element that is owned by a package has visibility, it is public
or private.


class IActivity
===============


Attributes not covered
----------------------

- isReadOnly : Boolean = false
- isSingleExecution : Boolean = false


Associations not covered
------------------------

- group : ActivityGroup [0..*]
- partition : ActivityPartition [0..*]
- /structuredNode : StructuredActivityNode [0..*]
- variable : Variable [0..*]


Associations different from specification
-----------------------------------------

- node : ActivityNode [0..*]
  nodes : IActivityNode [0..*]
- edge : ActivityEdge [0..*]
  edges : IActivityEdge [0..*]
- package : IPackage [1]


Constraints not covered
-----------------------

[1] The nodes of the activity must include one ActivityParameterNode for
    each parameter.
[2] An activity cannot be autonomous and have a classifier or behavioral
    feature context at the same time.
[3] The groups of an activity have no supergroups.


Constraints different from specification
----------------------------------------

[4] An activity must have exactly one package as parent.


class IOpaqueAction
===================


Associations not covered
------------------------

- language : String [0..*]
  Always Python.
- inputValue : InputPin [0..*]
  InputValues can be passed by input_pins.
- outputValue : OutputPin [0..*]
  OutputValues can be passed by output_pins.
- body : String [0..*]. Different semantics in activities.metamodel.


class IInitialNode
==================


Constraints not covered
-----------------------

[2] Only control edges can have initial nodes as source.


class IActivityFinalNode
========================


class IFlowFinalNode
====================


class IDecisionNode
===================


Associations not covered
------------------------

- decisionInput : Behavior [0..1]
  Decicions are made through guard specifications on edges.
- decisionInputFlow : ObjectFlow [0..1]
  Input values are only accessed through the activities' context.


Constraints not covered
-----------------------

[3], [4], [5], [6], [7], [8]
[2] The edges coming into and out of a decision node must be either all
    object flows or all control flows.


Constraints different from specification
----------------------------------------

[1] A decision node has one incoming edge and at least one outgoing edge.


Semantics
---------

- A decision node has XOR semantics


class IForkNode
---------------


Constraints different from specification
----------------------------------------

[1] A fork node has one incoming edge and at least one outgoing edge.


Constraints not covered
-----------------------

[2] The edges coming into and out of a fork node must be either all object
    flows or all control flows.


class IJoinNode
===============


Attributes not covered
----------------------

- isCombineDuplicate : Boolean [1..1]
  Tokens with same identity will always be combined.


Associations not covered
------------------------

- joinSpec : ValueSpecification [1..1]
  Default is "and". Use merge node for "or" semantic.


Constraints different from specification
----------------------------------------

[1] A join node has one outgoing edge and at least one incoming edge.


Constraints not covered
-----------------------

[2] If a join node has an incoming object flow, it must have an outgoing
    object flow, otherwise, it must have an outgoing control flow.


class IMergeNode
================


Constraints different from specification
----------------------------------------

[1] A merge node has one outgoing edge and at least one incoming edge.


Constraints not covered
-----------------------

[2] The edges coming into and out of a merge node must be either all object
    flows or all control flows.


class IConstraint
=================


Generalizations not covered
---------------------------

- PackageableElement (from Kernel)


Associations not covered
------------------------

- / context: Namespace [0..1]
  The context is the element which refers to this constraint.


Associations different from specification
-----------------------------------------

- constrainedElement: Element[*]
  constrained_element: object[1]
- specification: ValueSpecification[1]
  specification: String[1]


Constraints
-----------

[1] The value specification for a constraint must evaluate to a Boolean
    value.
[2] Evaluating the value specification for a constraint must not have side
    effects.


Constraints not covered
-----------------------

[3] A constraint cannot be applied to itself. (IConstraint does not have
    the ability to contain something. It does not derive from Node)


class IPreConstraint
====================


class IPostConstraint
=====================


class IProfile
==============


class IStereotype
=================


class ITaggedValue
==================
