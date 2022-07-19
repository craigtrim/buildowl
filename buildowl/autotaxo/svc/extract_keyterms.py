#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract Keyterms from Input Text using Textacy """


import pandas as pd
from pandas import DataFrame

from textacy import load_spacy_lang
from textacy import make_spacy_doc
from textacy.extract import keyterms as kt

from baseblock import Stopwatch
from baseblock import BaseObject


from buildowl.autotaxo.dto import load_model
from buildowl.autotaxo.dmo import TextacyKeytermExtractor
from buildowl.autotaxo.dmo import TextacyNgramExtractor
from buildowl.autotaxo.dmo import TextacyNounChunkExtractor
from buildowl.autotaxo.dmo import TextacyTermExtractor


class ExtractKeyterms(BaseObject):
    """ Aggregation Service for Extracting Keyterms """

    def __init__(self):
        """
        Created:
            18-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/3
        """
        BaseObject.__init__(self, __name__)
        model = load_model()

        self._extract_terms = TextacyTermExtractor(model).process
        self._extract_ngrams = TextacyNgramExtractor(model).process
        self._extract_keyterms = TextacyKeytermExtractor(model).process
        self._extract_nounchunks = TextacyNounChunkExtractor(model).process

    def _process(self,
                 input_text: str,
                 use_keyterms: bool,
                 use_ngrams: bool,
                 use_terms: bool,
                 use_nounchunks: bool) -> DataFrame:

        master = []

        if use_keyterms:
            [master.append(x) for x in self._extract_keyterms(input_text)]

        if use_ngrams:
            [master.append(x) for x in self._extract_ngrams(input_text)]

        if use_terms:
            [master.append(x) for x in self._extract_terms(input_text)]

        if use_nounchunks:
            [master.append(x) for x in self._extract_nounchunks(input_text)]

        return pd.DataFrame(master)

    def process(self,
                input_text: str,
                use_terms: bool = True,
                use_keyterms: bool = True,
                use_ngrams: bool = False,
                use_nounchunks: bool = False) -> DataFrame:

        sw = Stopwatch()

        df = self._process(input_text,
                           use_terms=use_terms,
                           use_keyterms=use_keyterms,
                           use_ngrams=use_ngrams,
                           use_nounchunks=use_nounchunks)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Keyword Extraction Complete",
                f"\tTotal Time: {str(sw)}",
                f"\tTotal Size: {len(df)}"]))

        return df
