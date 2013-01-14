UML Convinience Utilities
=========================


Inheritance adapter
-------------------

The Inheritance adapter adapts a UML element and builds a tree of its more
general elements. Our example tree looks like::

                       C1
                       AA  
                      /  \
              C2    C3   C4
               A      A  A
               |       \/ 
               \       C5
                \      A
                 \    /   
                   C6

So, first we build it::        

    >>> from node.ext.uml.core import Model
    >>> from node.ext.uml.classes import Class, Generalization
    >>> m = Model('model')
    >>> for i in range(1,7):
    ...     m['C%s'%i] = Class()   
    >>> m['C6']['g1'] = Generalization()
    >>> m['C6']['g1'].general = m['C2']
    >>> m['C6']['g2'] = Generalization()
    >>> m['C6']['g2'].general = m['C5']
    >>> m['C5']['g1'] = Generalization()
    >>> m['C5']['g1'].general = m['C3']
    >>> m['C5']['g2'] = Generalization()
    >>> m['C5']['g2'].general = m['C4']
    >>> m['C3']['g1'] = Generalization()
    >>> m['C3']['g1'].general = m['C1']
    >>> m['C4']['g1'] = Generalization()
    >>> m['C4']['g1'].general = m['C1']
    >>> m.printtree()
    <class 'node.ext.uml.core.Model'>: model
      <class 'node.ext.uml.classes.Class'>: C1
      <class 'node.ext.uml.classes.Class'>: C2
      <class 'node.ext.uml.classes.Class'>: C3
        <class 'node.ext.uml.classes.Generalization'>: g1
      <class 'node.ext.uml.classes.Class'>: C4
        <class 'node.ext.uml.classes.Generalization'>: g1
      <class 'node.ext.uml.classes.Class'>: C5
        <class 'node.ext.uml.classes.Generalization'>: g1
        <class 'node.ext.uml.classes.Generalization'>: g2
      <class 'node.ext.uml.classes.Class'>: C6
        <class 'node.ext.uml.classes.Generalization'>: g1
        <class 'node.ext.uml.classes.Generalization'>: g2

Lets see how the inheritance tree looks like::

    >>> from node.ext.uml.utils import Inheritance
    >>> inheritance = Inheritance(m['C6'])
    >>> inheritance.printtree()
    <class 'node.ext.uml.utils.Inheritance'>: ... on C6
      <class 'node.ext.uml.utils.Inheritance'>: ... on C2
      <class 'node.ext.uml.utils.Inheritance'>: ... on C5
        <class 'node.ext.uml.utils.Inheritance'>: ... on C3
          <class 'node.ext.uml.utils.Inheritance'>: ... on C1
        <class 'node.ext.uml.utils.Inheritance'>: ... on C4    
          <class 'node.ext.uml.utils.Inheritance'>: ... on C1

We can look at it flattened, we get a Set - but here we order a list::

    >>> all = list(inheritance.all)
    >>> print [n.noderepr for n in sorted(all, 
    ...                                   key=lambda obj: obj.context.__name__)]
    ["<class 'node.ext.uml.utils.Inheritance'>: ... on C1", 
    "<class 'node.ext.uml.utils.Inheritance'>: ... on C2", 
    "<class 'node.ext.uml.utils.Inheritance'>: ... on C3", 
    "<class 'node.ext.uml.utils.Inheritance'>: ... on C4", 
    "<class 'node.ext.uml.utils.Inheritance'>: ... on C5", 
    "<class 'node.ext.uml.utils.Inheritance'>: ... on C6"]        

To be sure we call this on a subpart of the tree::

    >>> sub = Inheritance(m['C5'])  
    >>> all = list(sub.all)
    >>> print [n.noderepr for n in sorted(all, 
    ...                                   key=lambda obj: obj.context.__name__)]    
    ["<class 'node.ext.uml.utils.Inheritance'>: ... on C1", 
    "<class 'node.ext.uml.utils.Inheritance'>: ... on C3", 
    "<class 'node.ext.uml.utils.Inheritance'>: ... on C4", 
    "<class 'node.ext.uml.utils.Inheritance'>: ... on C5"]        


Inheritors adapter
------------------

The `Inheritors adapter` answers the question "Who inherits from me?". It does
not return a tree, just a list of UMLElements on method call.
We take the same setup  as in the section `Inheritance`. In the simplest case 
we want all inheritors of C2, which will return C6::

    >>> from node.ext.uml.utils import Inheritors
    >>> i = Inheritors(m['C2'])
    >>> i.direct
    [<Class object 'C6' at ...>]

    >>> i.all
    [<Class object 'C6' at ...>]

For C3 we expect C5 and C6::  

    >>> i = Inheritors(m['C3'])
    >>> sorted(i.all, key=lambda obj: obj.__name__)
    [<Class object 'C5' at ...>, <Class object 'C6' at ...>]

But not for direct inheritors, here C5 is the expected result::    

    >>> i.direct
    [<Class object 'C5' at ...>]

Class C1 at the top of the diamond style inheritance must return C3 C4, C5 and 
C6::

    >>> i = Inheritors(m['C1'])
    >>> sorted(i.all, key=lambda obj: obj.__name__)
    [<Class object 'C3' at ...>, <Class object 'C4' at ...>,
    <Class object 'C5' at ...>, <Class object 'C6' at ...>]

As direct inheritors we expect C3 and C4:: 

    >>> sorted(i.all, key=lambda obj: obj.__name__)
    [<Class object 'C3' at ...>, <Class object 'C4' at ...>]


Assosiation adapters
--------------------

Assosiations can stick direct on a class or are inherited, which means class C3
inherits from class C1. Class C3 has an association `b` to class C4. Class C1 
has an association `a` to class C2::

    C1 ---a---> C2 
     A
     |
     |
    C3 ---b---> C4

So we first need to simply find the direct association `b` of class C3. Next 
we're interested in the inherited associations of class C3 which must return 
`a` and `b`.

First set up the scenario::

    >>> m = Model('model')
    >>> for i in range(1,5):
    ...     m['C%s'%i] = Class()
    >>> m['C3']['g1'] = Generalization()
    >>> m['C3']['g1'].general = m['C1']
    >>> from node.ext.uml.classes import Association, AssociationEnd
    >>> m['a'] = Association()
    >>> m['a']['c1'] = AssociationEnd()
    >>> m['a']['c1'].association = m['a']
    >>> m['a']['c1'].type = m['C1']
    >>> m['a']['c2'] = AssociationEnd()
    >>> m['a']['c2'].association = m['a']
    >>> m['a']['c2'].type = m['C2']
    >>> m['b'] = Association()
    >>> m['b']['c3'] = AssociationEnd()
    >>> m['b']['c3'].association = m['b']
    >>> m['b']['c3'].type = m['C3']
    >>> m['b']['c4'] = AssociationEnd()
    >>> m['b']['c4'].association = m['b']
    >>> m['b']['c4'].type = m['C4']

We want to find the association `b` with the direct property::

    >>> from node.ext.uml.utils import Associations
    >>> a = Associations(m['C3'])
    >>> a.direct
    [<AssociationEnd object 'c3' at ...>]

We want to find the inherited association `a` with the inherited property::

    >>> a.inherited
    [<AssociationEnd object 'c1' at ...>]

We want to find the all association `a`, `b` with the all property::

    >>> sorted(a.all, key=lambda obj: obj.__name__) 
    [<AssociationEnd object 'c1' at ...>, <AssociationEnd object 'c3' at ...>]


Aggregations Adapters
---------------------

Aggregations are association which has one end marked with an aggregationkind.
Lets assume a model where we have class C1 composite aggregating class C2.
Class C3 shared aggregates class C4, class C4 composite aggregates class C5.
class C3 inherits from class C1. We have also a normal association from C3 to 
C6::

          C1<.>--a-----C2
          A
          |
          | ------d--->C6         
          |/
          C3< >---b----C4<.>---c---C5

First set up the scenario::

    >>> m = Model('model')
    >>> for i in range(1,7):
    ...     m['C%s'%i] = Class()
    >>> m['C3']['g1'] = Generalization()
    >>> m['C3']['g1'].general = m['C1']    
    >>> m['a'] = Association()
    >>> m['a']['c1'] = AssociationEnd()
    >>> m['a']['c1'].association = m['a']
    >>> m['a']['c1'].type = m['C1']
    >>> m['a']['c1'].aggregationkind = AssociationEnd.COMPOSITE
    >>> m['a']['c2'] = AssociationEnd()
    >>> m['a']['c2'].association = m['a']
    >>> m['a']['c2'].type = m['C2']
    >>> m['b'] = Association()
    >>> m['C3']['c3'] = AssociationEnd()
    >>> m['C3']['c3'].association = m['b']
    >>> m['C3']['c3'].type = m['C3']
    >>> m['C3']['c3'].aggregationkind = AssociationEnd.SHARED
    >>> m['b'].memberEnds = [m['C3']['c3']]
    >>> m['b']['c4b'] = AssociationEnd()
    >>> m['b']['c4b'].association = m['b']
    >>> m['b']['c4b'].type = m['C4']          
    >>> m['c'] = Association()
    >>> m['c']['c4c'] = AssociationEnd()
    >>> m['c']['c4c'].association = m['c']
    >>> m['c']['c4c'].type = m['C4']
    >>> m['c']['c4c'].aggregationkind = AssociationEnd.COMPOSITE
    >>> m['c']['c5'] = AssociationEnd()
    >>> m['c']['c5'].association = m['c']
    >>> m['c']['c5'].type = m['C5']
    >>> m['d'] = Association()
    >>> m['d']['c3d'] = AssociationEnd()
    >>> m['d']['c3d'].association = m['d']
    >>> m['d']['c3d'].type = m['C3']
    >>> m['d']['c6'] = AssociationEnd()
    >>> m['d']['c6'].association = m['d']
    >>> m['d']['c6'].type = m['C6']

We use the basic association adapter to see if we get all associations from 
this scenario:: 

    >>> a = Associations(m['C3'])
    >>> sorted(a.all, key=lambda obj: obj.__name__) 
    [<AssociationEnd object 'c1' at ...>, <AssociationEnd object 'c3' at ...>, 
    <AssociationEnd object 'c3d' at ...>]

With the aggregation-adapter we get only aggregations::

    >>> from node.ext.uml.utils import Aggregations
    >>> a = Aggregations(m['C3'])
    >>> sorted(a.all, key=lambda obj: obj.__name__) 
    [<AssociationEnd object 'c1' at ...>, <AssociationEnd object 'c3' at ...>]

    >>> a = Aggregations(m['C4'])
    >>> sorted(a.all, key=lambda obj: obj.__name__) 
    [<AssociationEnd object 'c4c' at ...>]


Associations over InterfaceRealizations
---------------------------------------

We may have Associations defined via interfaces the class realizes. We assume
an interface I2 which inherits from interface I1. Class C3 realizes the 
interface I2. class C1 has a shared aggregation to I1. I1 has an composite 
aggregation to C5. Class C2 has a composite aggregation to interface I2. Also 
C4 has an composite aggregation to C4. Class C6 inherits from C3::
 
        C1 < >--a-- I1 <.>--d-- C5
                     A
                     |
        C2 <.>--b-- I2      
                     A
                     :
                    C3 <.>--c-- C4
                     A
                     |
                    C6                     

Set up the scenario::

    >>> from node.ext.uml.classes import Interface
    >>> from node.ext.uml.classes import InterfaceRealization
    >>> m = Model('model')
    >>> for i in range(1,7):
    ...     m['C%s'%i] = Class()
    >>> m['I1'] = Interface()
    >>> m['I2'] = Interface()
    >>> m['I2']['g1'] = Generalization()
    >>> m['I2']['g1'].general = m['I1']
    >>> m['C6']['g2'] = Generalization()
    >>> m['C6']['g2'].general = m['C3']
    >>> m['C3']['r'] = InterfaceRealization()
    >>> m['C3']['r'].contract = m['I2']    
    >>> m['a'] = Association()
    >>> m['C1']['c1'] = AssociationEnd()
    >>> m['C1']['c1'].association = m['a']
    >>> m['C1']['c1'].type = m['C1']
    >>> m['C1']['c1'].aggregationkind = AssociationEnd.SHARED
    >>> m['a']['i1a'] = AssociationEnd()
    >>> m['a']['i1a'].association = m['a']
    >>> m['a']['i1a'].type = m['I1']    
    >>> m['b'] = Association()
    >>> m['b']['c2'] = AssociationEnd()
    >>> m['b']['c2'].association = m['b']
    >>> m['b']['c2'].type = m['C2']
    >>> m['b']['c2'].aggregationkind = AssociationEnd.COMPOSITE
    >>> m['b']['i2'] = AssociationEnd()
    >>> m['b']['i2'].association = m['b']
    >>> m['b']['i2'].type = m['I2']
    >>> m['c'] = Association()
    >>> m['c']['c3'] = AssociationEnd()
    >>> m['c']['c3'].association = m['c']
    >>> m['c']['c3'].type = m['C3']
    >>> m['c']['c3'].aggregationkind = AssociationEnd.COMPOSITE
    >>> m['c']['c4'] = AssociationEnd()
    >>> m['c']['c4'].association = m['c']
    >>> m['c']['c4'].type = m['C4']
    >>> m['d'] = Association()
    >>> m['d']['i1d'] = AssociationEnd()
    >>> m['d']['i1d'].association = m['d']
    >>> m['d']['i1d'].type = m['I1']
    >>> m['d']['i1d'].aggregationkind = AssociationEnd.COMPOSITE
    >>> m['d']['c5'] = AssociationEnd()
    >>> m['d']['c5'].association = m['d']
    >>> m['d']['c5'].type = m['C5']

We can fetch from C3 only the ones coming over realization::

    >>> a = Associations(m['C3'])
    >>> sorted(a.directlyrealized, key=lambda obj: obj.__name__)
    [<AssociationEnd object 'i1a' at ...>, <AssociationEnd object 'i1d' at ...>, 
    <AssociationEnd object 'i2' at ...>]

Now check if `direct` is returning what we expect::

    >>> sorted(a.direct, key=lambda obj: obj.__name__)
    [<AssociationEnd object 'c3' at ...>]

If we ask C3 for all associations we have to see a whole bunch::

    >>> sorted(a.all, key=lambda obj: obj.__name__) 
    [<AssociationEnd object 'c3' at ...>, <AssociationEnd object 'i1a' at ...>, 
    <AssociationEnd object 'i1d' at ...>, <AssociationEnd object 'i2' at ...>]

We expect C6 to return on all the same as C3, because it inherits all from C3.
For direct its empty::

    >>> a = Associations(m['C6'])

    >>> sorted(a.direct, key=lambda obj: obj.__name__)
    []

    >>> sorted(a.directlyrealized, key=lambda obj: obj.__name__)
    []

    >>> sorted(a.inheritedrealized, key=lambda obj: obj.__name__)
    [<AssociationEnd object 'i1a' at ...>, <AssociationEnd object 'i1d' at ...>, 
    <AssociationEnd object 'i2' at ...>]

    >>> sorted(a.all, key=lambda obj: obj.__name__) 
    [<AssociationEnd object 'c3' at ...>, <AssociationEnd object 'i1a' at ...>, 
    <AssociationEnd object 'i1d' at ...>, <AssociationEnd object 'i2' at ...>]


Aggregators
-----------

Suppose class C2 has some aggregation to C1, class C4 has some aggregations to 
class C3, class C7 has some aggregation to class C6 and class C7 has some 
self-aggregation. Class C3 inherits from class C1 and class C3 inherits from C2.
Class C6 inherits from class C3 and class C5 inherits from class C4::

    C1 ---a---<> C2
     A           A        
     |         /
     |       /
     |     /
     |   /
     | / 
    C3 ---b---<> C4
     A            A
     |            |
     |           C5 
     |
    C6 ---c---<> C7<>-.
                  |_d_|

Setup the scenario::

    >>> m = Model('model')
    >>> for i in range(1,8):
    ...     m['C%s'%i] = Class()
    >>> m['C3']['g1'] = Generalization()
    >>> m['C3']['g1'].general = m['C1']    
    >>> m['C3']['g2'] = Generalization()
    >>> m['C3']['g2'].general = m['C2']    
    >>> m['C5']['g3'] = Generalization()
    >>> m['C5']['g3'].general = m['C4']    
    >>> m['C6']['g4'] = Generalization()
    >>> m['C6']['g4'].general = m['C3']    
    >>> m['a'] = Association()
    >>> m['a']['c1'] = AssociationEnd()
    >>> m['a']['c1'].association = m['a']
    >>> m['a']['c1'].type = m['C1']
    >>> m['a']['c2'] = AssociationEnd()
    >>> m['a']['c2'].association = m['a']
    >>> m['a']['c2'].type = m['C2']
    >>> m['a']['c2'].aggregationkind = AssociationEnd.COMPOSITE                  
    >>> m['b'] = Association()
    >>> m['b']['c3'] = AssociationEnd()
    >>> m['b']['c3'].association = m['b']
    >>> m['b']['c3'].type = m['C3']
    >>> m['b']['c4'] = AssociationEnd()
    >>> m['b']['c4'].association = m['b']
    >>> m['b']['c4'].type = m['C4']
    >>> m['b']['c4'].aggregationkind = AssociationEnd.COMPOSITE
    >>> m['c'] = Association()
    >>> m['c']['c6'] = AssociationEnd()
    >>> m['c']['c6'].association = m['c']
    >>> m['c']['c6'].type = m['C6']
    >>> m['c']['c7c'] = AssociationEnd()
    >>> m['c']['c7c'].association = m['c']
    >>> m['c']['c7c'].type = m['C7']
    >>> m['c']['c7c'].aggregationkind = AssociationEnd.COMPOSITE
    >>> m['d'] = Association()
    >>> m['d']['c7d1'] = AssociationEnd()
    >>> m['d']['c7d1'].association = m['d']
    >>> m['d']['c7d1'].type = m['C7']
    >>> m['d']['c7d2'] = AssociationEnd()
    >>> m['d']['c7d2'].association = m['d']
    >>> m['d']['c7d2'].type = m['C7']
    >>> m['d']['c7d2'].aggregationkind = AssociationEnd.COMPOSITE

Now we want to know the aggregators of some classes.

First the simplest for C1::

    >>> from node.ext.uml.utils import Aggregators
    >>> a = Aggregators(m['C1'])
    >>> a.direct
    [<AssociationEnd object 'c2' at ...>]

    >>> a.inherited
    []

    >>> a.all
    [<AssociationEnd object 'c2' at ...>]

Now we look at the self-aggregation on C7::    

    >>> a = Aggregators(m['C7'])
    >>> a.direct
    [<AssociationEnd object 'c7d2' at ...>]

    >>> a.inherited
    []

    >>> a.all
    [<AssociationEnd object 'c7d2' at ...>]

Next it gets more complicated. C3 can be contained in C4 and in C5, because C5
inherits from C4. Furthermore it can be contained in C2, because C2 is an 
aggregator of C1 and C3 inherits from C1. Then C3 can contain itself, since it 
inherits from C2 which can contain C1 and as said C3 inherits from C1. Last C3
can contain C6, because C6 inherits from C3. In other words we expect as the 
result: C1, C2, C3, C4, C5, C6::

    >>> a = Aggregators(m['C3'])
    >>> sorted(a.allparticipants, key=lambda obj: obj.__name__)
    [<Class object 'C2' at ...>, <Class object 'C3' at ...>, 
    <Class object 'C4' at ...>, <Class object 'C5' at ...>, 
    <Class object 'C6' at ...>]

Now lets take InterfaceRealizations into account. Assume a model, where class
C1 aggregates an Interface I1. Class C2 realizes the interface I1. Class C3
inherits from class C2::

       C1<>------I1
                  A
                  :
                 C2
                  A
                  |
                 C3

Setup our scenario::

    >>> m = Model('model')
    >>> for i in range(1,4):
    ...     m['C%s'%i] = Class()
    >>> m['I1'] = Interface()
    >>> m['C2']['r'] = InterfaceRealization()
    >>> m['C2']['r'].contract = m['I1']
    >>> m['C3']['g1'] = Generalization()
    >>> m['C3']['g1'].general = m['C2']        
    >>> m['a'] = Association()
    >>> m['a']['c1'] = AssociationEnd()
    >>> m['a']['c1'].association = m['a']
    >>> m['a']['c1'].type = m['C1']
    >>> m['a']['c1'].aggregationkind = AssociationEnd.COMPOSITE                  
    >>> m['a']['i1'] = AssociationEnd()
    >>> m['a']['i1'].association = m['a']
    >>> m['a']['i1'].type = m['I1']                                   

If we now ask C2 for its aggregators we expect C1 to appear::

    >>> a = Aggregators(m['C2'])
    >>> a.all
    [<AssociationEnd object 'c1' at ...>]

    >>> a.allparticipants    
    [<Class object 'C1' at ...>]

We expect for class C3 the same::

    >>> a = Aggregators(m['C3'])
    >>> a.allparticipants    
    [<Class object 'C1' at ...>]
 

Tagged Value Convinience
------------------------

Take a simple model first. We have a stereotype ``sA`` which can have a tagged 
value (abbrev. tgv) `tgv1` and a stereotype ``sB`` with tgv ``tgv2``. The model 
has <<sA>> applied and ``tgv1`` et. Model contains a package `p` with 
``<<sA>>/tgv1`` and ``<<sBA>>/tgv2`` set. Inside the package we have two 
classes ``C1`` and ``C2``. ``C2`` inherits from ``C1``. On ````C1``  both, 
``<<sA>>/tgv1`` and ``<<sBA>>/tgv2`, are set. On ``C2`` ``<<sA>>/tgv1`` is set.
All values are different::

    model <<sA>>: tgv1='value one on model'      

    | p <<sA>>: tgv1='value one on package'  |
    |   <<sB>>: tgv2='value two on package'  |
    |---------------------------------------------
    |                                             |
    |    C1 <<sA>>: tgv1='value one on class C1'  |
    |     A <<sB>>: tgv2='value two on class C2'  |
    |     |                                       |
    |    C2 <<sA>>: tgv1='value one on class C2'  |
    |_____________________________________________| 

    >>> from node.ext.uml.core import Package
    >>> from node.ext.uml.core import Stereotype
    >>> from node.ext.uml.core import TaggedValue
    >>> m = Model('model')
    >>> m['sA'] = Stereotype()
    >>> m['sA']['tgv1'] = TaggedValue()
    >>> m['sA']['tgv1'].value = 'value one on model'
    >>> m['p'] = Package()
    >>> m['p']['sA'] = Stereotype()
    >>> m['p']['sA']['tgv1'] = TaggedValue()
    >>> m['p']['sA']['tgv1'].value = 'value one on package'
    >>> m['p']['sB'] = Stereotype()
    >>> m['p']['sB']['tgv2'] = TaggedValue()
    >>> m['p']['sB']['tgv2'].value = 'value two on package'
    >>> m['p']['C1'] = Class()
    >>> m['p']['C1']['sA'] = Stereotype()
    >>> m['p']['C1']['sA']['tgv1'] = TaggedValue()
    >>> m['p']['C1']['sA']['tgv1'].value = 'value one on class C1'
    >>> m['p']['C1']['sB'] = Stereotype()
    >>> m['p']['C1']['sB']['tgv2'] = TaggedValue()
    >>> m['p']['C1']['sB']['tgv2'].value = 'value two on class C1'
    >>> m['p']['C2'] = Class()
    >>> m['p']['C2']['g'] = Generalization()
    >>> m['p']['C2']['g'].general = m['p']['C1']
    >>> m['p']['C2']['sA'] = Stereotype()
    >>> m['p']['C2']['sA']['tgv1'] = TaggedValue()
    >>> m['p']['C2']['sA']['tgv1'].value = 'value one on class C2'

Direct access simply returns values on the class::  

    >>> from node.ext.uml.utils import TaggedValues
    >>> tgv = TaggedValues(m['p']['C2'])
    >>> tgv.direct('tgv1', 'sA')
    'value one on class C2'

    >>> tgv.direct('sA:tgv1')
    'value one on class C2'

    >>> from node.ext.uml.utils import UNSET
    >>> tgv.direct('sB:tgv2') is UNSET
    True

    >>> tgv.direct('NotExistent:tgv999') is UNSET
    True

Inherited access works as well::    

    >>> tgv.inherited('tgv1', 'sA')
    ['value one on class C2', 'value one on class C1']

    >>> tgv.inherited('tgv1', 'sA', aggregate=False)
    'value one on class C2'

    >>> tgv.inherited('tgv2', 'sB')
    ['value two on class C1']

    >>> tgv.inherited('tgv2', 'sB', aggregate=False)
    'value two on class C1'

    >>> tgv.inherited('tgv2', 'sB', alternatives=[('tgv1', 'sA')])
    ['value one on class C2', 'value two on class C1', 'value one on class C1']

    >>> tgv.inherited('tgv1', 'sA', alternatives=['sB:tgv2',])
    ['value one on class C2', 'value one on class C1', 'value two on class C1']

Namespaced access walks up the UML namespace hierarchy::

    >>> tgv.namespaced('tgv1', 'sA')
    ['value one on class C2', 'value one on package', 'value one on model']


Dependencies
------------

TODO/ Nice to have

>> deputil = Dependencies(someumlelement)
>> dep.incoming
[Dep1, Dep3]

>> dep.outgoing
[Dep2, Dep4]
