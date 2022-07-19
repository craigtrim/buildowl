#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Orchestrate Taxonomy Generation """


from baseblock import BaseObject

from buildowl.autotaxo.svc import ExtractKeyterms
from buildowl.autotaxo.svc import FilterKeyterms
from buildowl.autotaxo.svc import GenerateTaxonomyDataFrame
from buildowl.autotaxo.svc import GenerateTaxonomyTTL
from buildowl.autotaxo.dto import load_model


class AutoTaxoOrchestrator(BaseObject):
    """ Orchestrate Taxonomy Generation """

    def __init__(self):
        """ Change Log:

        Created:
            16-Apr-2022
            craigtrim@gmail.com
            *   in pursuit of "Auto Taxonomy Building with Textacy Library #286"
        Updated:
            2-May-2022
            craigtrim@gmail.com
            *   renamed from 'generate-taxonomy'
        Updated:
            18-Jul-20922
            craigtrim@gmail.com
            *   overhaul end-to-end process
                https://github.com/craigtrim/buildowl/issues/3

        """
        BaseObject.__init__(self, __name__)
        self._model = load_model()

    def process(self,
                input_text: str) -> list or None:

        df_keyterms = ExtractKeyterms(self._model).process(input_text)
        keyterms = FilterKeyterms().process(df_keyterms)
        df_taxo = GenerateTaxonomyDataFrame().process(keyterms)
        ttl_results = GenerateTaxonomyTTL().process(df_taxo)

        return ttl_results
