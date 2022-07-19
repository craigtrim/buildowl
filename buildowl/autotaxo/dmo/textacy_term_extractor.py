#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract Ngrams from Input Text using Textacy """


from functools import partial
from spacy.lang.en import English

from textacy import make_spacy_doc
from textacy.extract import terms
from textacy.extract import entities
from textacy.extract import ngrams

from baseblock import Stopwatch
from baseblock import BaseObject

from buildowl.autotaxo.dmo import StopWordFilter
from buildowl.autotaxo.dto import load_model


class TextacyTermExtractor(BaseObject):
    """ Extract Terms from Input Text using Textacy

    Documentation:
        https://textacy.readthedocs.io/en/latest/api_reference/extract.html#textacy.extract.basics.terms
    """

    def __init__(self,
                 model: English = None):
        """ Change Log

        Created:
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
        self._has_stopword = StopWordFilter().has_stopword

    def _process(self,
                 input_text: str,
                 case_sensitive: bool) -> list:

        if not case_sensitive:
            input_text = input_text.lower()

        doc = make_spacy_doc(input_text, lang=self._model)

        master = []

        for result in terms(doc, ngs=2, ents=True, ncs=True):
            master.append({
                "Term": result.text,
                "Size": len(result.text.split()),
                "Score": None,
                "Source": "terms.1",
            })

        for result in terms(doc, ngs=lambda doc: ngrams(doc, n=2)):
            master.append({
                "Term": result.text,
                "Size": len(result.text.split()),
                "Score": None,
                "Source": "terms.2",
            })

        for result in terms(doc, ents=entities):
            master.append({
                "Term": result.text,
                "Size": len(result.text.split()),
                "Score": None,
                "Source": "terms.3",
            })

        for result in terms(doc, ents=partial(entities, include_types="PERSON")):
            master.append({
                "Term": result.text,
                "Size": len(result.text.split()),
                "Score": None,
                "Source": "terms.4",
            })

        return master

    def process(self,
                input_text: str,
                filter_stops: bool = True,
                case_sensitive: bool = False) -> list:
        """ Extract n-Grams from Input Text

        Args:
            input_text (str): input text of any length
            min_freq (int, optional): Number of times a term must repeat. Defaults to 3.
            filter_stops (bool, optional): Filter Stopwords. Defaults to True.
            drop_determiners (bool, optional): drop determiners from the start of noun chunks. Defaults to True.
            case_sensitive (bool, optional): Determine if input text case should be maintained.  Defaults to False
            as_dataframe (bool, optional): Returns the result set as a pandas Dataframe.  Defaults to False

        Returns:
            list: n-Gram results
        """

        sw = Stopwatch()

        results = self._process(input_text=input_text,
                                case_sensitive=case_sensitive)

        if filter_stops:
            results = [x for x in results if not self._has_stopword(x['Term'])]

        return results
