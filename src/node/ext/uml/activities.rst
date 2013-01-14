node.ext.uml activities.py test
===============================

Start this test like so::
    ./bin/test -s node.ext.uml -t activities.rst

We cannot instantiate abstract base classes::

    >>> from node.ext.uml.activities import Behavior
    >>> behavior = Behavior()
    >>> behavior.check_model_constraints()
    Traceback (most recent call last):
    ...
    ModelIllFormedException: <Behavior...> Cannot directly use abstract base classes

Import the model.

If you want to know how to create a model, look into testing/env.py::

    >>> from node.ext.uml.testing.env import model

Validate the model::

    >>> from node.ext.uml.activities import validate
    >>> validate(model)

Test if the model provides us with all the elements and methods we expect...::

    >>> model
    <Package object 'testmodel'...>
    >>> list(model.activities)
    [<Activity object 'main'...>]
    >>> list(model.profiles)
    [<Profile object 'pr' ...>]
    >>> list(model.stereotypes)
    []

    >>> act = model['main']
    >>> act
    <Activity object 'main'...>
    >>> list(act.preconditions)
    [<PreConstraint object 'pc1'...>]
    >>> list(act.postconditions)
    [<PostConstraint object 'po1'...>]
    >>> act.package
    <Package object 'testmodel'...>

    >>> list(act.nodes)
    [<...'start'...'fork'...'action1'...'action2'...'action3'...'join'...'decision'...'merge'...'flow end'...'end'...>]

    >>> list(act.edges)
    [<ActivityEdge object '1'...'2'...'3'...'4'...'5'...'6'...'7'...'8'...'9'...'10'...'11'...>]

    >>> list(act.actions)
    [<...'action1'...'action2'...'action3'...>]

    >>> act['action1'].activity
    <Activity object 'main'...>
    >>> list(act['action1'].incoming_edges)
    [<ActivityEdge object '2'...>]
    >>> list(act['action1'].outgoing_edges)
    [<ActivityEdge object '4'...>]
    >>> list(act['action1'].stereotypes)
    [<Stereotype object 'execution1'...>]
    >>> list(act['action1'].stereotypes)[0].profile is list(model.profiles)[0]
    True
    >>> list(act['action1']['execution1'].taggedvalues)
    [<TaggedValue object 'tgv'...>]
    >>> act['action1']['execution1']['tgv'].value
    'dummy value'
    >>> list(act['action1'].preconditions)
    [<PreConstraint object 'lpc1'...>]
    >>> list(act['action1'].postconditions)
    [<PostConstraint object 'lpo1'...>]

    >>> act['8']
    <ActivityEdge object '8'...>
    >>> act['8'].activity
    <Activity object 'main'...>
    >>> act['8'].source
    <DecisionNode object 'decision'...>
    >>> act['8'].target
    <FlowFinalNode object 'flow end'...>
    >>> act['8'].guard
    'else'

Test finding node per xmiid::

    >>> act['8'].xmiid = "abcd"
    >>> from node.ext.uml.activities import get_element_by_xmiid
    >>> act['8'] == get_element_by_xmiid(model, "abcd")
    True

    # >>> interact( locals() )
