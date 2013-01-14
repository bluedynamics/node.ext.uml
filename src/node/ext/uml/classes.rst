UML CLasses
===========

Create a model to work at::

    >>> from node.ext.uml.core import Model
    >>> m = Model()

Add a Class::

    >>> from node.ext.uml.classes import Class
    >>> from node.ext.uml.classes import Parameter
    >>> m['myclass'] = Class()

Add a Property for a primitive Datatype. Primitive Datatypes are always bound
to the Model element (root) and prefixed by ``uml:``. Datatypes have to exist
before they is assigned to the property::

    >>> from node.ext.uml.core import Datatype
    >>> m['uml:String'] = Datatype()
    >>> from node.ext.uml.classes import Property
    >>> m['myclass']['prop1'] = Property()
    >>> m['myclass']['prop1'].type = m['uml:String']

Add a property with a custom datatype::

    >>> from node.ext.uml.core import Datatype
    >>> m['mytype'] = Datatype()
    >>> m['myclass']['prop1'] = Property()
    >>> m['myclass']['prop1'].type = m['mytype']

Add a Operation without anything::

    >>> from node.ext.uml.classes import Operation 
    >>> m['myclass']['op1'] = Operation()

An Operation with a return value::

    >>> from node.ext.uml.classes import Parameter 
    >>> m['myclass']['op2'] = Operation()
    >>> m['myclass']['op2']['param'] = Parameter()
    >>> m['myclass']['op2']['param'].direction = 'return'
    >>> m['myclass']['op2']['param'].type = m['mytype']

Query the operations from the class::

    >>> list(m['myclass'].operations)
    [<Operation object 'op1' at ...>, <Operation object 'op2' at ...>]

We also have interfaces::

    >>> from node.ext.uml.classes import Interface
    >>> m['myiface'] =  Interface()
    >>> m['myiface']['opdef'] = Operation()    

Query the operations from the interface::

    >>> list(m['myiface'].operations)
    [<Operation object 'opdef' at ...>]

Inherit a class from another by generalization::

    >>> from node.ext.uml.classes import Generalization
    >>> m['myotherclass'] = Class()
    >>> m['myotherclass']['name_or_xmiid'] = Generalization()
    >>> m['myotherclass']['name_or_xmiid'].general = m['myclass']

Its possible to realize an interface::

    >>> from node.ext.uml.classes import InterfaceRealization
    >>> m['myotherclass']['name_or_xmiid'] = InterfaceRealization()
    >>> m['myotherclass']['name_or_xmiid'].contract = m['myiface']

We can have an simple association between two classes::

    >>> from node.ext.uml.classes import Association, AssociationEnd
    >>> m['assoc1'] = Association()
    >>> m['assoc1']['src'] = AssociationEnd()
    >>> m['assoc1']['src'].association = m['assoc1']
    >>> m['assoc1']['src'].type = m['myclass']
    >>> m['assoc1']['dst'] = AssociationEnd()
    >>> m['assoc1']['dst'].association = m['assoc1']
    >>> m['assoc1']['dst'].type = m['myotherclass']

An AssociationEnd may be navigable and may have a multiplicity::

    >>> from node.ext.uml.core import INFINITE 
    >>> m['assoc1']['src'].lowervalue = 0
    >>> m['assoc1']['src'].uppervalue = 1
    >>> m['assoc1']['dst'].navigable = True
    >>> m['assoc1']['dst'].lowervalue = 1
    >>> m['assoc1']['dst'].uppervalue = INFINITE

Shared aggregations are handled a bit different. The destinations  end gets an 
aggregationkind set and also the end is owned by the class itself.  Well, this 
is how the UML specifications wants it. Lets aggregate::

    >>> m['aggregation'] = Association()
    >>> m['aggregation']['src'] = AssociationEnd()
    >>> m['aggregation']['src'].association = m['aggregation']
    >>> m['aggregation']['src'].type = m['myclass']
    >>> m['myotherclass']['dst'] = AssociationEnd()
    >>> m['myotherclass']['dst'].association = m['aggregation']
    >>> m['myotherclass']['dst'].type = m['myotherclass']
    >>> m['aggregation'].memberEnds = [m['myotherclass']]
    >>> m['myotherclass']['dst'].aggregationkind = AssociationEnd.SHARED

An Dependency is an own element between to classifiers::

    >>> from node.ext.uml.classes import Dependency
    >>> m['dep'] = Dependency()
    >>> m['dep'].client = m['myclass']
    >>> m['dep'].supplier = m['myotherclass']
