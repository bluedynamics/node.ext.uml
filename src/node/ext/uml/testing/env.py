import node.ext.uml.core as core
import node.ext.uml.activities as activities


profile = core.Profile('pr')
#profile['execution1'] = core.Stereotype()
#profile['execution1']['tgv'] = core.TaggedValue()


model = core.Package('testmodel')
model[profile.__name__] = profile
model['main'] = activities.Activity()
act = model['main']


act['pc1'] = activities.PreConstraint(specification='True is True')
act['po1'] = activities.PostConstraint(specification='False is False')


act['start'] = activities.InitialNode()
act['fork'] = activities.ForkNode()


act['action1'] = activities.OpaqueAction()
act['action1']['execution1'] = core.Stereotype()
act['action1']['execution1'].profile = profile
act['action1']['execution1']['tgv'] = core.TaggedValue()
act['action1']['execution1']['tgv'].value = "dummy value"
act['action1']['lpc1'] = activities.PreConstraint(
    specification='True is True')
act['action1']['lpo1'] = activities.PostConstraint(
    specification='False is False')


act['action2'] = activities.OpaqueAction()
act['action3'] = activities.OpaqueAction()


act['join'] = activities.JoinNode()
act['decision'] = activities.DecisionNode()
act['merge'] = activities.MergeNode()


act['flow end'] = activities.FlowFinalNode()
act['end'] = activities.ActivityFinalNode()


act['1'] = activities.ActivityEdge(source=act['start'],
                                   target=act['fork'])
act['2'] = activities.ActivityEdge(source=act['fork'],
                                   target=act['action1'])
act['3'] = activities.ActivityEdge(source=act['fork'],
                                   target=act['action2'])
act['4'] = activities.ActivityEdge(source=act['action1'],
                                   target=act['action3'])
act['5'] = activities.ActivityEdge(source=act['action2'],
                                   target=act['join'])
act['6'] = activities.ActivityEdge(source=act['action3'],
                                   target=act['decision'])
act['7'] = activities.ActivityEdge(source=act['action3'],
                                   target=act['join'])
act['8'] = activities.ActivityEdge(source=act['decision'],
                                   target=act['flow end'],
                                   guard="else")
act['9'] = activities.ActivityEdge(source=act['decision'],
                                   target=act['merge'],
                                   guard="True")
act['10'] = activities.ActivityEdge(source=act['join'],
                                    target=act['merge'])
act['11'] = activities.ActivityEdge(source=act['merge'],
                                    target=act['end'])


activities.validate(model)
