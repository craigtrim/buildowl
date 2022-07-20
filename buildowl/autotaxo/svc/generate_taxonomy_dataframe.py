#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Generate Taxonomy Suitable for use in an OWL file """


import pandas as pd
from pandas import DataFrame
from spacy.tokens.doc import Doc

from textacy import extract
from textacy import make_spacy_doc

from baseblock import Stopwatch
from baseblock import BaseObject


class GenerateTaxonomyDataFrame(BaseObject):
    """ Generate Taxonomy Suitable for use in an OWL file """

    def __init__(self):
        """
        Created:
            16-Apr-2022
            craigtrim@gmail.com
            *   refactored out of jupyter notebook:
                    GRAFFL-286 Textacy Textrank
                    http://localhost:8888/notebooks/grafflbox/GRAFFL-286%20Textacy%20Textrank.ipynb
                https://github.com/grafflr/graffl-core/issues/286
        """
        BaseObject.__init__(self, __name__)

    def _decompose_term(self,
                        term: str) -> list:
        taxonomy = []

        tokens = term.split()
        if len(tokens) == 1:
            return [term]

        for i in range(len(tokens)):
            current = tokens[:i]
            if len(current):
                current.reverse()
                taxonomy.append(' '.join(current))

        return taxonomy

    def _process(self,
                 results: list) -> list:
        master = []

        for result in results:

            tokens = result.split()
            tokens.reverse()

            taxonomy = []
            for i in range(len(tokens)):
                current = tokens[:i]
                if len(current):
                    current.reverse()
                    taxonomy.append(' '.join(current))

            if result not in taxonomy:
                taxonomy.append(result)

            if not len(taxonomy):
                continue

            for i in range(len(taxonomy)):
                if i + 1 < len(taxonomy):
                    master.append({
                        "Parent": taxonomy[i],
                        "Child": taxonomy[i+1],
                        "Confidence": result[1],
                    })

        return master

    def process(self,
                results: list) -> DataFrame:

        sw = Stopwatch()

        master = self._process(results)

        df = pd.DataFrame(master)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Taxonomy Generation Complete",
                f"\tTotal Time: {str(sw)}",
                f"\tTotal Size: {len(df)}"]))

        return df
