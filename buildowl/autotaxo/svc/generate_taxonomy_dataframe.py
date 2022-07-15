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

    def _extract_keyterms(self,
                          doc: Doc,
                          top_n: int) -> list:
        results = extract.keyterms.textrank(
            doc,
            normalize="lemma",
            topn=top_n)

        master = []

        for result in results:
            tokens = result[0].split()
            tokens.reverse()

            taxonomy = []
            for i in range(len(tokens)):
                current = tokens[:i]
                if len(current):
                    current.reverse()
                    taxonomy.append(' '.join(current))

            if result[0] not in taxonomy:
                taxonomy.append(result[0])

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

    def _extract_noun_phrases(self,
                              doc: Doc) -> list:
        observed = [nc.text for nc in extract.noun_chunks(
            doc, drop_determiners=True)]

        for item in observed:
            print (item, " ---> ", self._decompose_term(item))

        # print(observed)

    def _process(self,
                 input_text: str,
                 top_n) -> DataFrame:

        doc = make_spacy_doc(
            input_text,
            lang="en_core_web_sm")

        print(type(doc))

        master = self._extract_keyterms(doc, top_n)

        # self._extract_noun_phrases(doc)
        # raise ValueError('stop here')

        df = pd.DataFrame(master)
        return df

    def process(self,
                input_text: str,
                top_n: int) -> DataFrame:

        sw = Stopwatch()

        df = self._process(
            input_text=input_text,
            top_n=top_n)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Taxonomy Generation Complete",
                f"\tTotal Time: {str(sw)}",
                f"\tTotal Size: {len(df)}"]))

        return df
