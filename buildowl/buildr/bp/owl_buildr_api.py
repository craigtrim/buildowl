#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Orchestrate Taxonomy Generation """


from baseblock import BaseObject

from buildowl.buildr.svc import AddGraphNodes
from buildowl.buildr.svc import GenerateOwlModel


class OwlBuilderAPI(BaseObject):
    """ Orchestrate Taxonomy Generation """

    def __init__(self):
        """ Change Log:

        Created:
            21-Jul-20922
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/7
        """
        BaseObject.__init__(self, __name__)

    def generate(self,
                 model_name: str,
                 model_path: str,
                 model_author: str = None) -> str:
        """ Generate an OWL model

        Args:
            model_name (str): the name of the model
                this will form part of the namespace URI
            model_path (str): the directory the model will be persisted to
            model_author (str, optional): the model author. Defaults to None.

        Returns:
            str: the absolute path to the OWL model
        """
        return GenerateOwlModel().process(
            model_name=model_name,
            model_path=model_path,
            model_author=model_author)

    def add_entities(self,
                     model_file_name: str,
                     ttl_entities: list) -> str:
        """ Add new Entities in TTL (Turtle) format to the Model

        Args:
            model_file_name (str): the path to the existing model
            ttl_entities (list): the list of entities

        Returns:
            str: the new version
        """
        return AddGraphNodes().process(
            ttl_entities=ttl_entities,
            model_file_name=model_file_name)


def main():

    api = OwlBuilderAPI()

    model_file_name = api.generate(
        model_name="mytest001",
        model_path="c:/Users/Craig/Desktop",
        model_author="ctrim")

    version = api.add_entities(
        ttl_entities=[],
        model_file_name=model_file_name)

    version = api.add_entities(
        ttl_entities=[],
        model_file_name=model_file_name)

    version = api.add_entities(
        ttl_entities=[],
        model_file_name=model_file_name)

    version = api.add_entities(
        ttl_entities=[],
        model_file_name=model_file_name)

    print(version)


if __name__ == "__main__":
    main()
