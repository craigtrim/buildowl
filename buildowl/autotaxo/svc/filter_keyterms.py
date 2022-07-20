#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract Keyterms from Input Text using Textacy """


from pandas import DataFrame
from textblob import Word

from baseblock import Stopwatch
from baseblock import BaseObject

from buildowl.autotaxo.dto import FuzzyWuzzyWrapper


class FilterKeyterms(BaseObject):
    """ Filter a DataFrame of KeyTerms """

    def __init__(self):
        """
        Created:
            18-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/3
        """
        BaseObject.__init__(self, __name__)
        self._fuzzscore = FuzzyWuzzyWrapper().process

    def _process(self,
                 df: DataFrame) -> list:

        terms = [x.lower() for x in list(df['Term'].unique())]
        print(terms)

        # sort by length
        terms = sorted(set(terms), key=len, reverse=True)

        discards = set()

        # discard plurals
        for t1 in terms:
            for t2 in [x for x in terms if x != t1]:
                if f"{t1}s" == t2:
                    discards.add(t2)
                elif f"{t2}s" == t1:
                    discards.add(t1)

        # discard bigrams found in trigrams
        for t1 in [x for x in terms if len(x.split()) == 2]:
            for t2 in [x for x in terms if len(x.split()) == 3]:
                if f"{t1} " in t2 or f" {t1}" in t2:
                    discards.add(t1)

        terms = [x.strip() for x in terms if x not in discards]

        # discard larger length if word similarity value is close
        for t1 in terms:
            for t2 in [x for x in terms if x != t1]:
                if self._fuzzscore(t1, t2)['score'] >= 85:
                    if len(t1) > len(t2):
                        discards.add(t1)
                    else:
                        discards.add(t2)

        # given a term like 'wi-fi' discard any 'wi' and 'fi' terms
        for tokens in [x.split('-') for x in terms if '-' in x]:
            print("CHECK TOKENS: ", tokens)
            [discards.add(x) for x in tokens if x in terms]

        self.logger.debug('\n'.join([
            "Tokens Filtering Completed",
            f"\tTotal Discards: {len(discards)}",
            f"\t\t{list(discards)}"]))

        terms = [x.strip() for x in terms if x not in discards]

        # lemmatize individual tokens in each term
        lemmatized_terms = set()
        for term in terms:
            tokens = term.split()
            term = ' '.join([Word(x).lemmatize() for x in tokens]).strip()
            lemmatized_terms.add(term)

        return sorted(lemmatized_terms, key=len, reverse=True)

    def process(self,
                df: DataFrame) -> list:

        sw = Stopwatch()

        results = self._process(df)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Keyword Filtering Complete",
                f"\tTotal Time: {str(sw)}",
                f"\tTotal Size: {len(df)}"]))

        return results
