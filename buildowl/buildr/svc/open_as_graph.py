#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Open a file-based model as an rdflib Graph """


from rdflib import Graph

from baseblock import BaseObject
from baseblock import FileIO

from buildowl.buildr.dmo import OwlGraphConnector


class OpenAsGraph(BaseObject):
    """ Open a file-based model as an rdflib Graph """

    def __init__(self):
        """ Change Log:

        Created:
            21-Jul-20922
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/7
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                model_file_name: str) -> Graph:
        """ Open a file-based model as an rdflib Graph

        Args:
            model_file_name (str): the path to the existing model

        Returns:
            Graph: an instantiation of an rdflib Graph object
        """

        lines = FileIO.read_lines(model_file_name)

        def get_namespace() -> str:
            for line in lines:
                if line.startswith('@prefix'):
                    line = line.split(': <')[-1].split('#')[0]
                    return line

        namespace = get_namespace()
        prefix = namespace.split('/')[-1].strip()

        graph = OwlGraphConnector(
            prefix=prefix,
            namespace=namespace,
            model_file_name=model_file_name).graph()

        return graph
