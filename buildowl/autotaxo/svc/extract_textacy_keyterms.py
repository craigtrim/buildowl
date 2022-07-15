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


class ExtractTextacyKeyterms(BaseObject):
    """ Extract Keyterms from Input Text using Textacy """

    def __init__(self):
        """
        Created:
            20-Apr-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/302
        """
        BaseObject.__init__(self, __name__)

    def _process(self,
                 top_n: int,
                 input_text: str) -> DataFrame:

        en = load_spacy_lang("en_core_web_sm",
                             disable=("parser",))

        doc = make_spacy_doc(input_text,
                             lang=en)

        return kt.textrank(doc,
                           normalize="lemma",
                           topn=top_n)

    def process(self,
                top_n: int,
                input_text: str) -> DataFrame:

        sw = Stopwatch()

        df = self._process(
            top_n=top_n,
            input_text=input_text)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Textacy Keyword Extraction Complete",
                f"\tTotal Time: {str(sw)}",
                f"\tTotal Size: {len(df)}"]))

        return df
