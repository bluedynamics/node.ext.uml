from node.base import OrderedNode
from node.ext.uml.interfaces import (
    IGeneralization,
    IAssociationEnd,
    IInterfaceRealization
)
from node.ext.uml.classes import AssociationEnd


class Inheritance(OrderedNode):
    """Tree giving the inheritance tree point of view of arbitary UML-elements.

    By adapting an UML element this tree shows the generelizations of the
    element as a Node tree.

    On __getitem__ it returns the Inheritance adapter of the more general
    element.
    """

    def __init__(self, context):
        """@param context: some UMLElement to get information from."""
        super(Inheritance, self).__init__()
        self.__name__ = context.uuid
        self.context = context

    def _inherited(self):
        for generelization in self.context.filtereditervalues(IGeneralization):
            yield generelization.general

    def __iter__(self):
        """iterates over uuids of more general UML-elements."""
        for element in self._inherited():
            yield element.uuid

    iterkeys = __iter__

    def itervalues(self):
        """iterates over more general UML-elements."""
        for key in self.keys():
            yield self[key]

    def __getitem__(self, uuid):
        """fetches the more general UML-element by key."""
        general = self.context.node(uuid)
        item = Inheritance(general)
        item.__parent__ = self
        return item

    @property
    def noderepr(self):
        return '%s on %s' % (super(Inheritance, self).noderepr,
                             self.context.__name__)

    @property
    def all(self):
        """flattend (list) from the traversed tree of more general
        UML-elements.

        @return: list of UMLElements.
        """
        result = list()
        result.append(self)
        for value in self.values():
            subs = value.all
            for sub in subs:
                if sub.__name__ in [r.__name__ for r in result]:
                    continue
                result.append(sub)
        return result


class Inheritors(object):
    """Adapter giving the inverse inheritance point of view of arbitary
    UML-elements.
    """

    def __init__(self, context):
        """@param context: some UMLElement to get information from."""
        self.context = context

    @property
    def direct(self):
        """UMLElements which are inheriting diretcly (less general) from the
        given UMLElement

        @return: list of UMLElements.
        """
        result = list()
        for node in self.context._index.values():
            if IGeneralization.providedBy(node) \
               and node.general is self.context:
                result.append(node.specific)
        return result

    @property
    def all(self):
        """UMLElements which are inheriting (less general) from the
        given UMLElement, following the tree down: childs of childs are
        included.

        @return: list of UMLElements.
        """
        result = self.direct
        for node in self.direct:
            if node is self.context:
                continue
            result += Inheritors(node).all
        return result


class Associations(object):
    """Adapter to get information about an UMLElements associations.
    """

    def __init__(self, context):
        self.context = context

    def _match_end(self, end):
        return IAssociationEnd.providedBy(end)

    def _find_associations_ends(self, partipants):
        partuuids = [p.uuid for p in partipants]
        result = list()
        for node in self.context._index.values():
            if self._match_end(node) and node.type.uuid in partuuids:
                result.append(node)
        return result

    @property
    def direct(self):
        """All associations which are starting or ending directly at the given
        UML element.

        @return: list of AssociationEnd instances.
        """
        return self._find_associations_ends([self.context])

    @property
    def inherited(self):
        """All associations which are inherited from more general UML-Elements,
        the direct associations are not included.

        @return: list of AssociationEnd instances.
        """
        inheritance = Inheritance(self.context)
        subs = [el.context for el in inheritance.all
                if el.context is not self.context]
        return self._find_associations_ends(subs)

    @property
    def directlyrealized(self):
        """All associations which are on Interfaces with InterfaceRealizations
        directly on this UMLElement. This includes Associations from more
        general Interfaces of the contracted Interface (it takes the Inheritance
        tree of the Relaized interface into account).

        @return: list of AssociationEnd instances.
        """
        participatinginterfaces = list()
        for directrealization in \
            self.context.filtereditervalues(IInterfaceRealization):
            participatinguuids = [i.uuid for i in participatinginterfaces]
            for inheritance in Inheritance(directrealization.contract).all:
                if inheritance.context.uuid not in participatinguuids:
                    participatinginterfaces.append(inheritance.context)
        return self._find_associations_ends(participatinginterfaces)

    @property
    def inheritedrealized(self):
        """All associations which are on Interfaces with InterfaceRealizations
        from more general UMLElements of this element. This includes
        Associations from more general Interfaces of the contracted Interface
        (it takes the Inheritance tree of the Relaized interface into account).
        It does not include directly realized associations.

        @return: list of AssociationEnd instances.
        """
        ends = list()
        inherited = [el.context for el in Inheritance(self.context).all]
        for node in inherited:
            associations = self.__class__(node)
            for end in associations.directlyrealized:
                if end.uuid not in [e.uuid for e in ends]:
                    ends.append(end)
        return ends

    @property
    def all(self):
        """All associations: direct, directlyrealized, inherited and
        inheritedrealized.

        ``return``
          list of AssociationEnd instances.
        """
        result = self.direct
        for end in self.directlyrealized + \
                   self.inherited + \
                   self.inheritedrealized:
            if end.uuid not in [r.uuid for r in result]:
                result.append(end)
        return result


class Aggregations(Associations):
    """Adapter to get information about an UMLElements aggregations.
    """

    def _match_end(self, end):
        return super(Aggregations, self)._match_end(end) \
               and end.aggregationkind in AssociationEnd.AGGREGATIONS


class Aggregators(Associations):
    """Adapter to get information about an UMLElements aggregators.

    This is done by adding a filter so the inherited methods of this class instances
    are taking onyl aggregations into account.
    """

    def _oppositeend(self, end):
        oppositeends = [e for e in end.association.memberEnds if e is not end]
        oppositeends += [e for e in end.association.ownedEnds if e is not end]
        assert(len(oppositeends)==1)
        return oppositeends[0]

    def _match_end(self, end):
        if not super(Aggregators, self)._match_end(end):
            return False
        return self._oppositeend(end).aggregationkind in \
               AssociationEnd.AGGREGATIONS

    def _find_associations_ends(self, partipants):
        ends = super(Aggregators, self)._find_associations_ends(partipants)
        return [self._oppositeend(e) for e in ends]

    @property
    def allparticipants(self):
        """All UMLElements the AssociationEnds of `all` are pointing to.

        ``return``
           list of UMLElements
        """
        results = list()
        for end in self.all:
            results.append(end.type)
            for inheritor in Inheritors(end.type).all:
                if inheritor.uuid not in [r.uuid for r in results]:
                    results.append(inheritor)
        return results


UNSET = object()


class TaggedValues(object):
    """Adapter to get information about an UMLElements TaggedValues.
    """

    def __init__(self, context):
        self.context = context

    def direct(self, tag, stereotype=None, default=UNSET):
        """Access only tgvs directly applied through stereotypes on element.

        ``tag``
          The name of the tag to fetch the value from. If no ``stereotype``
          argument is given it is expected here in the form: ``STEREOTYPE:TAG``.

        ``stereotype``
          Name of the stereotype. Can be omitted if it is part of ``tag``
          argument.

        ``return``
          some value
        """
        if stereotype is None:
            stereotype, tag = tag.split(':')
        stereotypeob = self.context.stereotype(stereotype)
        if stereotypeob is None:
            return default
        taggedvalue =  stereotypeob.taggedvalue(tag)
        if taggedvalue is None:
            return default
        return taggedvalue.value

    def _normalized_tgv_pairs(self, tag, stereotype, alternatives):
        normalized = list()
        if stereotype is None:
            normalized.append(list(reversed(tag.split(':'))))
        else:
            normalized.append((tag, stereotype))
        for alternative in alternatives:
            if isinstance(alternative, tuple) or isinstance(alternative, list):
               normalized.append(alternative)
            else:
               normalized.append(list(reversed(alternative.split(':'))))
        return normalized

    def _direct_with_alternatives(self, tag, stereotype, alternatives):
        result = list()
        for ltag, lstereotype in self._normalized_tgv_pairs(tag, stereotype,
                                                  alternatives):
            value = self.direct(ltag, lstereotype)
            if value is not UNSET:
                result.append(self.direct(ltag, lstereotype))
        return result

    def inherited(self, tag, stereotype=None, alternatives=[], aggregate=True):
        """Access tgvs on this element and more general elements of element.

        ``tag``
          The name of the tag to fetch the value from. If no ``stereotype``
          argument is given it is expected here in the form: ``STEREOTYPE:TAG``.

        ``stereotype``
          Name of the stereotype. Can be omitted if it is part of ``tag``
          argument.

        ``alternatives``
          Look in more general elements also for stereotypes/tags in this list.
          Expects either a tuple ``tag, stereotype`` or a tag prefixed with
          stereotype as described above. Lookup order: arguments, order of list,
          first one hit wins.

        ``aggregate``
          When ``True`` a list of all found values is returned. Otherwise it
          stops on the first matching tag and returns its value.

        ``return``
          A value, or in case of ``aggregate`` a list of values.
        """
        result = self._direct_with_alternatives(tag, stereotype, alternatives)
        if not aggregate and result:
            return result[0]
        for generalization in self.context.filtereditervalues(IGeneralization):
            tgv = TaggedValues(generalization.general)
            subres = tgv.inherited(tag, stereotype, alternatives, aggregate)
            if aggregate:
                result += subres
            elif subres is not UNSET:
                return subres
        if not aggregate:
            return UNSET
        return result

    def namespaced(self, tag, stereotype=None, alternatives=[], aggregate=True):
        """Access tgvs on this element and elements down in namespace.

        ``tag``
          The name of the tag to fetch the value from. If no ``stereotype``
          argument is given it is expected here in the form: ``STEREOTYPE:TAG``.

        ``stereotype``
          Name of the stereotype. Can be omitted if it is part of ``tag``
          argument.

        ``alternatives``
          Look in more general elements also for stereotypes/tags in this list.
          Expects either a tuple ``tag, stereotype`` or a tag prefixed with
          stereotyoe as described above.

        ``aggregate``
          When ``True`` a list of all found values is returned. Otherwise it
          stops on the first matching tag and returns its value.

        ``return``
          A value, or in case of ``aggregate`` a list of values.
        """
        result = self._direct_with_alternatives(tag, stereotype, alternatives)
        if not aggregate and result:
            return result[0]
        if self.context.__parent__ is None:
            if not aggregate:
               return UNSET
            return result
        tgv = TaggedValues(self.context.__parent__)
        if not aggregate:
            return tgv.namespaced(tag, stereotype, alternatives, aggregate)
        return result + tgv.namespaced(tag, stereotype, alternatives, aggregate)
