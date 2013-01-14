UML Core Elements
=================

Model Root::

    >>> from node.ext.uml.core import Model
    >>> model = Model('testmodel')
    >>> model
    <Model object 'testmodel' at ...>

Package::
 
    >>> from node.ext.uml.core import Package
    >>> model['mypackage'] = Package()
    >>> model['mypackage']
    <Package object 'mypackage' at ...>

    >>> model.printtree()
    <class 'node.ext.uml.core.Model'>: testmodel
      <class 'node.ext.uml.core.Package'>: mypackage

Querying the Package::

    >>> from node.ext.uml.classes import Class
    >>> from node.ext.uml.classes import Interface
    >>> model['package2'] = Package()
    >>> model['package2']['class1'] = Class()
    >>> model['package2']['class2'] = Class()
    >>> model['package2']['iface1'] = Interface()
    >>> model['package2']['iface2'] = Interface()
    >>> model['package2']['package3'] = Package()

    >>> list(model['mypackage'].packages)
    []
    >>> list(model['mypackage'].classes)
    []
    >>> list(model['mypackage'].interfaces)
    []
    >>> list(model['package2'].packages)
    [<Package object 'package3' at ...>]
    >>> list(model['package2'].classes)
    [<Class object 'class1' at ...>, <Class object 'class2' at ...>]
    >>> list(model['package2'].interfaces)
    [<Interface object 'iface1' at ...>, <Interface object 'iface2' at ...>]

Adding Profile to model::

    >>> from node.ext.uml.core import Profile
    >>> model['mypackage']['myprofile'] = Profile()

Adding Stereotype::

    >>> from node.ext.uml.core import Stereotype
    >>> model['mypackage']['mystereotype'] = Stereotype()
    >>> model['mypackage']['mystereotype'].profile = \
    ...                                          model['mypackage']['myprofile']
    >>> model['mypackage']['mystereotype'].profile
    <Profile object 'myprofile' at ...>

Adding TaggedValue to Stereotype::

    >>> from node.ext.uml.core import TaggedValue
    >>> model['mypackage']['mystereotype']['mytgv'] = TaggedValue()
    >>> model['mypackage']['mystereotype']['mytgv'].value = 'hurray'

    >>> model.printtree()
    <class 'node.ext.uml.core.Model'>: testmodel
      <class 'node.ext.uml.core.Package'>: mypackage
        <class 'node.ext.uml.core.Profile'>: myprofile
        <class 'node.ext.uml.core.Stereotype'>: mystereotype
          <class 'node.ext.uml.core.TaggedValue'>: mytgv
      <class 'node.ext.uml.core.Package'>: package2
        <class 'node.ext.uml.classes.Class'>: class1
        <class 'node.ext.uml.classes.Class'>: class2
        <class 'node.ext.uml.classes.Interface'>: iface1
        <class 'node.ext.uml.classes.Interface'>: iface2
        <class 'node.ext.uml.core.Package'>: package3
