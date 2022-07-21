#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Orchestrate Synonym Generation for Ontologies """


import pandas as pd
from pandas import DataFrame

from baseblock import BaseObject

from buildowl.autotaxo.bp import AutoTaxoOrchestrator
from buildowl.autosyns.svc import GenerateInflectionCall


class AutoSynsOrchestrator(BaseObject):
    """ Orchestrate Synonym Generation for Ontologies """

    def __init__(self):
        """ Change Log:

        Created:
            20-Jul-20922
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/5

        """
        BaseObject.__init__(self, __name__)
        self._find_inflections = GenerateInflectionCall().process

    def _keyterms(self,
                  input_text: str) -> list:
        if ' ' not in input_text:
            return [input_text]

        svc = AutoTaxoOrchestrator()
        keyterms = svc.keyterms(input_text,
                                use_keyterms=True,
                                use_ngrams=True,
                                use_nounchunks=True,
                                use_terms=True)

        unigrams = set()
        for keyterm in keyterms:
            [unigrams.add(x) for x in keyterm.split()]

        return sorted(unigrams)

    def process(self,
                input_text: str) -> list:
        master = []

        for keyterm in self._keyterms(input_text):
            d_result = self._find_inflections(keyterm)
            if d_result:
                csv = ','.join(d_result['inflections'])
                master.append(f"{keyterm}~{csv}")

        return master
