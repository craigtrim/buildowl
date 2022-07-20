#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Generate TTL Suitable for use in an OWL file """


from pandas import DataFrame

from baseblock import BaseObject


class GenerateRelationshipsTTL(BaseObject):
    """ Generate TTL Suitable for use in an OWL file """

    def __init__(self):
        """
        Created:
            20-Jul-20922
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/4
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                df: DataFrame) -> list:

        def to_entity(some_value: str) -> str:
            return some_value.replace(' ', '_').lower().strip()

        def to_label(some_value: str) -> str:
            tokens = some_value.replace('_', ' ').split(' ')
            tokens = [f"{x[0].upper()}{x[1:]}" for x in tokens]
            return ' '.join(tokens).strip()

        def ttl_subject() -> str:
            return """
            ###  http://graffl.ai/pathology#EntityName
            :EntityName rdf:type owl:Class ;
            rdfs:label "EntityLabel" ;
            :PredicateName :ObjectName .
            """.strip()

        def ttl_object() -> str:
            return """
            ###  http://graffl.ai/pathology#EntityName
            :EntityName rdf:type owl:Class ;
            rdfs:label "EntityLabel" .
            """.strip()

        snippets = []
        for _, row in df.iterrows():

            subject_entity = to_entity(row['Subject'])
            subject_label = to_label(row['Subject'])

            object_entity = to_entity(row['Object'])
            object_label = to_label(row['Object'])

            predicate = row['Predicate']

            ttl_s = ttl_subject()
            ttl_s = ttl_s.replace('EntityName', subject_entity)
            ttl_s = ttl_s.replace('EntityLabel', subject_label)
            ttl_s = ttl_s.replace('PredicateName', predicate)
            ttl_s = ttl_s.replace('ObjectName', object_entity)
            snippets.append(ttl_s)

            ttl_o = ttl_object()
            ttl_o = ttl_o.replace('EntityName', object_entity)
            ttl_o = ttl_o.replace('EntityLabel', object_label)
            snippets.append(ttl_o)

        return snippets
