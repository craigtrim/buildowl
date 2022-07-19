#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract Keyterms from Input Text using Textacy """


from spacy.lang.en import English

from textacy import make_spacy_doc
from textacy.extract import keyterms as kt

from baseblock import Stopwatch
from baseblock import BaseObject

from buildowl.autotaxo.dto import load_model


class TextacyKeytermExtractor(BaseObject):
    """ Extract Keyterms from Input Text using Textacy 

    Documentation:
        https://textacy.readthedocs.io/en/latest/api_reference/extract.html#keyterms
    """

    def __init__(self,
                 model: English = None):
        """ Change Log

        Created:
            20-Apr-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/302
        Updated:
            18-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/3

        Args:
            model (English): spaCy model
        """
        BaseObject.__init__(self, __name__)
        if model is None:
            model = load_model()

        self._model = model

    def _process(self,
                 top_n: int,
                 input_text: str) -> list:

        master = []

        doc = make_spacy_doc(input_text, lang=self._model)

        # TextRank: window_size=2, edge_weighting="binary", position_bias=False
        for result in kt.textrank(doc,
                                  topn=top_n,
                                  window_size=2,
                                  normalize="lemma",
                                  edge_weighting='binary',
                                  position_bias=False):
            master.append({
                "Term": result[0],
                "Size": len(result[0].split()),
                "Score": result[1],
                "Source": "kt.textrank",
            })

        # SingleRank: window_size=10, edge_weighting="count", position_bias=False
        for result in kt.textrank(doc,
                                  topn=top_n,
                                  window_size=10,
                                  normalize="lemma",
                                  edge_weighting='count',
                                  position_bias=False):
            master.append({
                "Term": result[0],
                "Size": len(result[0].split()),
                "Score": result[1],
                "Source": "kt.singlerank",
            })

        # PositionRank: window_size=10, edge_weighting="count", position_bias=True
        for result in kt.textrank(doc,
                                  topn=top_n,
                                  window_size=10,
                                  normalize="lemma",
                                  edge_weighting='count',
                                  position_bias=True):
            master.append({
                "Term": result[0],
                "Size": len(result[0].split()),
                "Score": result[1],
                "Source": "kt.positionrank",
            })

        # yake algorithm
        for result in kt.yake(doc,
                              topn=top_n,
                              window_size=10,
                              normalize="lemma"):
            master.append({
                "Term": result[0],
                "Size": len(result[0].split()),
                "Score": result[1],
                "Source": "yake",
            })

        # scake algorithm
        for result in kt.scake(doc,
                               topn=top_n,
                               normalize="lemma"):
            master.append({
                "Term": result[0],
                "Size": len(result[0].split()),
                "Score": result[1],
                "Source": "scake",
            })

        # sgrank algorithm
        for result in kt.sgrank(doc,
                                topn=top_n,
                                window_size=10,
                                normalize="lemma"):
            master.append({
                "Term": result[0],
                "Size": len(result[0].split()),
                "Score": result[1],
                "Source": "sgrank",
            })

        return master

    def process(self,
                input_text: str,
                top_n: int = 15) -> list:

        sw = Stopwatch()

        results = self._process(
            top_n=top_n,
            input_text=input_text)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Textacy Keyword Extraction Complete",
                f"\tTotal Time: {str(sw)}",
                f"\tTotal Size: {len(results)}"]))

        return results
