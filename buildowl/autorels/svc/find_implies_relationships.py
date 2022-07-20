#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Create "Implies" Relationships between entities """


from baseblock import BaseObject


class FindImpliesRelationships(BaseObject):
    """ Create "Implies" Relationships between entities """

    def __init__(self):
        """ Change Log:

        Created:
            20-Jul-20922
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/4

        """
        BaseObject.__init__(self, __name__)

    def process(self,
                terms: list) -> list or None:
        """ Find 'Implies' Relationships between terms

        Sample Input:
            ['network hardware', 'network protocol', 'network', 'protocol']

        Sample Output (pseudo):
            [   "network hardware" implies "network",
                "network protocol" implies "protocol"
            ]

        Args:
            terms (list): a list of plain text terms

        Returns:
            list or None: a list of S/P/O triple results
        """

        # normalize incoming terms
        # the function expects 'alpha_beta_gamma' formatted terms
        terms = [x.replace(' ', '_') for x in terms]

        unigrams = [x for x in terms if '_' not in x]
        ngrams = [x for x in terms if '_' in x]

        def match(input_text: str) -> str or None:
            l_text = f"_{input_text}"
            r_text = f"{input_text}_"
            for ngram in ngrams:
                if l_text in ngram:
                    return ngram, ngram.replace(l_text, '')
                if r_text in ngram:
                    return ngram, ngram.replace(r_text, '')
            return None, None

        results = []
        for unigram in unigrams:
            x, y = match(unigram)
            if x and y:
                results.append({
                    "Subject": x,
                    "Predicate": "implies",
                    "Object": y
                })

        return results
