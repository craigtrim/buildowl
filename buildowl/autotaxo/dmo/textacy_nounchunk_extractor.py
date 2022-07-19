#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract Ngrams from Input Text using Textacy """

from collections import Counter
from spacy.lang.en import English

from textacy import make_spacy_doc
from textacy.extract import noun_chunks

from baseblock import Stopwatch
from baseblock import BaseObject

from buildowl.autotaxo.dmo import StopWordFilter
from buildowl.autotaxo.dto import load_model


class TextacyNounChunkExtractor(BaseObject):
    """ Extract Ngrams from Input Text using Textacy

    Documentation:
        https://textacy.readthedocs.io/en/latest/api_reference/extract.html#textacy.extract.basics.noun_chunks
    """

    def __init__(self,
                 model: English = None):
        """ Change Log

        Created:
            15-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/2
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
        self._has_stopword = StopWordFilter().has_stopword

    def _process(self,
                 input_text: str,
                 drop_determiners: bool,
                 case_sensitive: bool,
                 min_freq: int) -> list:

        if not case_sensitive:
            input_text = input_text.lower()

        doc = make_spacy_doc(input_text, lang=self._model)

        results = list(noun_chunks(doc,
                                   min_freq=min_freq,
                                   drop_determiners=drop_determiners))
        print(results)
        c = Counter()
        for result in results:
            c.update({result: 1})

        s = set()
        for term in c:
            frequency = c[term]
            if frequency >= min_freq:
                s.add(term)

        return sorted(s)

    def process(self,
                input_text: str,
                min_freq: int = 1,
                filter_stops: bool = True,
                drop_determiners: bool = True,
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
                                drop_determiners=drop_determiners,
                                case_sensitive=case_sensitive,
                                min_freq=min_freq)

        # the result-set is a list of spacy.tokens.span.Span elements
        results = [x.text.strip() for x in results]

        if filter_stops:
            results = [x for x in results if not self._has_stopword(x)]

        # I consider a 'noun chunk' to be 2..* nouns
        results = [x for x in results if ' ' in x]

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Noun Chunk Extraction Complete",
                f"\tTotal Time: {str(sw)}",
                f"\tTotal Size: {len(results)}"]))

        master = []

        for result in results:
            master.append({
                "Term": result,
                "Size": len(result.split()),
                "Source": "NounChunk",
                "Score": None,
            })

        return master
