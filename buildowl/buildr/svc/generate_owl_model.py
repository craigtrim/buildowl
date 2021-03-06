#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Generate an OWL model based on a TTL template """


import os
import pandas as pd
from pandas import DataFrame
from datetime import datetime

from rdflib import Graph
from rdflib import Namespace

from baseblock import EnvIO
from baseblock import FileIO
from baseblock import BaseObject

from buildowl.autorels.svc import FindImpliesRelationships
from buildowl.autorels.svc import FindRequiresRelationships
from buildowl.autorels.svc import GenerateRelationshipsTTL


class GenerateOwlModel(BaseObject):
    """ Generate an OWL model based on a TTL template """

    __authorship = "Generated on TIMESTAMP by AUTHOR"

    def __init__(self):
        """ Change Log:

        Created:
            21-Jul-20922
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/7
        """
        BaseObject.__init__(self, __name__)

    def process(self,
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

        template_path = os.path.normpath(os.path.join(EnvIO.str_or_exception(
            'BUILDOWL_HOME'), 'resources/models/templates/template.owl'))
        FileIO.exists_or_error(template_path)
        lines = FileIO.read_lines(template_path)

        ns_default = "http://graffl.ai/template"
        ns_model_name = f"http://graffl.ai/{model_name}"

        def authorship() -> str:
            dt = str(datetime.now())
            if not model_author:
                return f"Generated on {dt}"
            return f"Generated by {model_author} on {dt}"

        normalized = []
        for line in lines:
            if ns_default in line:
                line = line.replace(ns_default, ns_model_name)
            if self.__authorship in line:
                line = line.replace(self.__authorship, authorship())
            normalized.append(line)

        FileIO.exists_or_error(model_path)
        model_file_name = os.path.normpath(
            os.path.join(model_path, f"{model_name}.owl"))
        FileIO.write_lines(normalized, model_file_name)

        return model_file_name
