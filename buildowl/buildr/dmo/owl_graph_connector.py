#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Connect to an RDF Graph (Ontology) """


from rdflib import Graph
from rdflib import Namespace

from baseblock import BaseObject


class OwlGraphConnector(BaseObject):
    """ Connect to an RDF Graph (Ontology) """

    def __init__(self,
                 prefix: str,
                 namespace: str,
                 model_file_name: str):
        """ Change Log

        Created:
            21-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/7

        Args:
            prefix (str): the query prefix
            namespace (str): the ontology namespace
            model_file_name (str): the absolute path to the model
        """
        BaseObject.__init__(self, __name__)

        self._format = "ttl"
        self._prefix = prefix
        self._namespace = namespace
        self._model_file_name = model_file_name

        self._graph = self._process()

        self.logger.debug('\n'.join([
            f"Loading Ontology",
            f"\tPath: {self._model_file_name}",
            f"\tNamespace: {self._namespace}",
            f"\tPrefix: {self._prefix}",
            f"\tFormat: {self._format}"]))

    def _process(self) -> Graph:
        """load the ontology from disk as an RDF Graph

        Returns:
            Graph: an instantiated and in-memory RDF Graph
        """
        g = Graph()

        g.parse(self._model_file_name,
                format=self._format)

        g.bind(self._prefix,
               Namespace(self._namespace))

        return g

    def graph(self) -> Graph:
        return self._graph
