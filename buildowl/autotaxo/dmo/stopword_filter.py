#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Simple Stopword Filter """


from baseblock import BaseObject

from buildowl.autotaxo.dto import stopwords


class StopWordFilter(BaseObject):
    """ Simple Stopword Filter """

    __starting_filter = [
        'generally',
        'involves',
    ]

    __ending_filter = [
        'include',
    ]

    def __init__(self):
        """
        Created:
            20-Apr-2022
            craigtrim@gmail.com
            *   in pursuit of
                https://github.com/grafflr/graffl-core/issues/302
        """
        BaseObject.__init__(self, __name__)

    def has_stopword(self,
                     input_text: str) -> bool:
        """ Custom Layer for removing Stopwords beyond OTB capabilities

        Args:
            input_text (str): an incoming string of any length

        Returns:
            bool: True if the input text contains a stop word
        """

        input_text = input_text.lower().strip()
        if input_text in stopwords:
            return True

        tokens = input_text.split()
        if len(tokens) == 1:
            return False

        if tokens[0] in self.__starting_filter:
            return True

        if tokens[-1] in self.__ending_filter:
            return True

        for token in tokens:
            if token in stopwords:
                return True

        return False
