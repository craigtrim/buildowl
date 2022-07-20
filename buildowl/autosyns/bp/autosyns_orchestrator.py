#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Orchestrate Synonym Generation for Ontologies """


import pandas as pd
from pandas import DataFrame

from baseblock import BaseObject

from buildowl.autotaxo.bp import AutoTaxoOrchestrator


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

    def process(self,
                input_text: str) -> list:
        svc = AutoTaxoOrchestrator()
        keyterms = svc.keyterms(input_text,
                                use_keyterms=True,
                                use_ngrams=True,
                                use_nounchunks=True,
                                use_terms=True)
        print (keyterms)