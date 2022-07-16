#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract Ngrams from Input Text using Textacy """


from socket import NI_DGRAM
import pandas as pd
from pandas import DataFrame

from textacy import load_spacy_lang
from textacy import make_spacy_doc
from textacy.extract import ngrams

from baseblock import Stopwatch
from baseblock import BaseObject

from buildowl.autotaxo.dmo import StopWordFilter


class ExtractTextacyNgrams(BaseObject):
    """ Extract Ngrams from Input Text using Textacy """

    def __init__(self):
        """
        Created:
            20-Apr-2022
            craigtrim@gmail.com
            *   in pursuit of
                https://github.com/grafflr/graffl-core/issues/302
        """
        BaseObject.__init__(self, __name__)
        self._has_stopword = StopWordFilter().has_stopword

    def _process(self,
                 input_text: str,
                 ngram_level: int,
                 filter_stops: bool,
                 filter_punct: bool,
                 filter_nums: bool,
                 case_sensitive: bool,
                 term_frequency: int) -> DataFrame:

        en = load_spacy_lang("en_core_web_sm",
                             disable=("parser",))

        if not case_sensitive:
            input_text = input_text.lower()

        doc = make_spacy_doc(input_text,
                             lang=en)

        results = list(ngrams(doc, ngram_level,
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
                filter_stops: bool = True,
                filter_punct: bool = True,
                filter_nums: bool = True,
                term_frequency: int = 2,
                case_sensitive: bool = False,
                as_dataframe: bool = False) -> list or DataFrame:
        """ Extract n-Grams from Input Text

        Args:
            input_text (str): input text of any length
            ngram_level (int, optional): n-Gram level to extract. Defaults to 3.
            filter_stops (bool, optional): Filter Stopwords. Defaults to True.
            filter_punct (bool, optional): Filter Punctuation. Defaults to True.
            filter_nums (bool, optional): Remove Numbers from results. Defaults to True.
            term_frequency (int, optional): Number of times a term must repeat. Defaults to 2.
            case_sensitive (bool, optional): Determine if input text case should be maintained.  Defaults to False
            as_dataframe (bool, optional): Returns the result set as a pandas Dataframe.  Defaults to False

        Returns:
            list or DataFrame: n-Gram results
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

        if not as_dataframe:
            return results

        master = []

        for result in results:
            master.append({
                "Text": result,
                "Size": ngram_level})

        return pd.DataFrame(master)
