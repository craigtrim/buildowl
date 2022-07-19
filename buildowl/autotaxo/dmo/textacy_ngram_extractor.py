#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract Ngrams from Input Text using Textacy """


from spacy.lang.en import English

from textacy import make_spacy_doc
from textacy.extract import ngrams

from baseblock import Stopwatch
from baseblock import BaseObject

from buildowl.autotaxo.dmo import StopWordFilter
from buildowl.autotaxo.dto import load_model


class TextacyNgramExtractor(BaseObject):
    """ Extract Ngrams from Input Text using Textacy 

    Documentation:
        https://textacy.readthedocs.io/en/latest/api_reference/extract.html#textacy.extract.basics.ngrams
    """

    def __init__(self,
                 model: English = None):
        """ Change Log

        Created:
            20-Apr-2022
            craigtrim@gmail.com
            *   in pursuit of
                https://github.com/grafflr/graffl-core/issues/302
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
                 ngram_level: int,
                 filter_stops: bool,
                 filter_punct: bool,
                 filter_nums: bool,
                 case_sensitive: bool,
                 term_frequency: int) -> list:

        if not case_sensitive:
            input_text = input_text.lower()

        doc = make_spacy_doc(input_text, lang=self._model)

        results = list(ngrams(doc, ngram_level,
                              include_pos=('NOUN', 'PROPN', 'ADJ'),
                              exclude_pos=('ADV'),
                              filter_stops=filter_stops,
                              filter_punct=filter_punct,
                              filter_nums=filter_nums))

        from collections import Counter
        c = Counter()
        for result in results:
            c.update({result: 1})

        s = set()
        for term in c:
            frequency = c[term]
            if frequency >= term_frequency:
                s.add(term)

        return sorted(s)

    def process(self,
                input_text: str,
                ngram_level: int = 3,
                term_frequency: int = 1,
                filter_stops: bool = True,
                filter_punct: bool = True,
                filter_nums: bool = True,
                case_sensitive: bool = False) -> list:
        """ Extract n-Grams from Input Text

        Args:
            input_text (str): input text of any length
            ngram_level (int, optional): n-Gram level to extract. Defaults to 3.
            filter_stops (bool, optional): Filter Stopwords. Defaults to True.
            filter_punct (bool, optional): Filter Punctuation. Defaults to True.
            filter_nums (bool, optional): Remove Numbers from results. Defaults to True.
            term_frequency (int, optional): Number of times a term must repeat. Defaults to 2.
            case_sensitive (bool, optional): Determine if input text case should be maintained.  Defaults to False

        Returns:
            list: n-Gram results
        """

        sw = Stopwatch()

        results = self._process(input_text=input_text,
                                ngram_level=ngram_level,
                                filter_stops=filter_stops,
                                filter_punct=filter_punct,
                                filter_nums=filter_nums,
                                term_frequency=term_frequency,
                                case_sensitive=case_sensitive)

        # the result-set is a list of spacy.tokens.span.Span elements
        results = [x.text for x in results]

        if filter_stops:
            results = [x for x in results if not self._has_stopword(x)]

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "N-Gram Extraction Complete",
                f"\tTotal Time: {str(sw)}",
                f"\tTotal Size: {len(results)}"]))

        master = []

        for result in results:
            master.append({
                "Term": result,
                "Size": ngram_level,
                "Score": None,
                "Source": "Ngram"
            })

        return master
