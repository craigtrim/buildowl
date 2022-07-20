#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Create "Requires" Relationships between entities """


from baseblock import BaseObject


class FindRequiresRelationships(BaseObject):
    """ Create "Requires" Relationships between entities """

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
        """ Find 'Requires' Relationships between terms

        Sample Input:
            ['network hardware', 'network protocol', 'network', 'protocol']

        Sample Output (pseudo):
            [   "network hardware" requires "hardware",
                "network protocol" requires "network"
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
                    return ngram, l_text.replace('_', '')
                if r_text in ngram:
                    return ngram, r_text.replace('_', '')
            return None, None

        print(unigrams)
        print(ngrams)

        results = []
        for unigram in unigrams:
            x, y = match(unigram)
            if x and y:
                results.append({
                    "Subject": x,
                    "Predicate": "requires",
                    "Object": y
                })

        return results


if __name__ == "__main__":
    input = ['network hardware', 'network protocol', 'network', 'protocol']
    results = FindRequiresRelationships().process(input)
    [print(x) for x in results]
    print('done')
