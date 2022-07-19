#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from statistics import mean
from fuzzywuzzy import fuzz

from nltk import stem

from baseblock import BaseObject


class FuzzyWuzzyWrapper(BaseObject):
    """ Wrap the Fuzzy Wuzzy API """

    __stemmer = stem.PorterStemmer()

    def __init__(self):
        """
        Created:
            18-Jul-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    @staticmethod
    def process(s1: str,
                s2: str,
                basic: bool = True,
                q_ratio: bool = False,
                w_ratio: bool = False,
                uq_ratio: bool = False,
                uw_ratio: bool = False,
                partial_ratio: bool = False,
                token_sort_ratio: bool = False) -> dict:

        s1 = s1.lower().strip()
        s2 = s2.lower().strip()

        d_result = {"text": {
            "s1": s1,
            "s2": s2},
            "ratios": {}}

        def _basic() -> float:
            return fuzz.ratio(s1, s2)

        def _q_ratio() -> float:
            return fuzz.QRatio(s1, s2,
                               force_ascii=True,
                               full_process=True)

        def _w_ratio() -> float:
            return fuzz.WRatio(s1, s2,
                               force_ascii=True,
                               full_process=True)

        def _uq_ratio() -> float:
            return fuzz.UQRatio(s1, s2,
                                full_process=True)

        def _uw_ratio() -> float:
            return fuzz.UWRatio(s1, s2,
                                full_process=True)

        def _partial_ratio() -> float:
            return fuzz.partial_ratio(s1, s2)

        def _token_sort_ratio() -> float:
            return fuzz.token_sort_ratio(s1, s2,
                                         force_ascii=True,
                                         full_process=True)

        ratios = []

        def _add_ratio(ratio_type: str,
                       ratio_value: float):
            ratios.append(ratio_value)
            d_result["ratios"][ratio_type] = ratio_value

        if basic:
            _add_ratio("basic", _basic())
        if partial_ratio:
            _add_ratio("partial", _partial_ratio())
        if token_sort_ratio:
            _add_ratio("token_sort", _token_sort_ratio())
        if q_ratio:
            _add_ratio("q", _q_ratio())
        if w_ratio:
            _add_ratio("w", _w_ratio())
        if uq_ratio:
            _add_ratio("uq", _uq_ratio())
        if uw_ratio:
            _add_ratio("uw", _uw_ratio())

        def mean_score() -> int:
            if not len(ratios):
                return 0
            if len(ratios) == 1:
                return ratios[0]
            return round(mean(ratios), 1)

        d_result['score'] = mean_score()

        return d_result
