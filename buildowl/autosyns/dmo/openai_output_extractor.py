#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract Output from OpenAI Response """


from pprint import pformat
from baseblock import BaseObject


class OpenAIOutputExtractor(BaseObject):
    """ Extract Output from OpenAI Response """

    def __init__(self):
        """
        Created:
            20-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/5
        """
        BaseObject.__init__(self, __name__)

    def _remove_conflicts(self,
                          search_term: list,
                          inflections: set) -> list:
        """ The openAI output will occasionally return the examples used in the prompt
            as part of the answer

        Args:
            search_term (str): the term that was searched on
            inflections (set): the inflections extracted from the search result

        Returns:
            set: the potentially modified set of inflections
        """
        if not search_term.lower().startswith('troubleshoot'):
            prompt_terms = [
                'troubleshoots',
                'troubleshooting',
                'troubleshooted',
                'troubleshooter',
                'troubleshooters'
            ]

            inflections = [x for x in inflections if x not in prompt_terms]

        return inflections

    def _handle_inner_line_breaks(self,
                                  inflections: list) -> list:
        """ Handle Line Breaks embedded within the output list

        Args:
            inflections (list): the incoming inflections
            the incoming list can sometimes look like this:
                "text": " wider, widest\n         widens, widened, widening\n         widely",

        Returns:
            list: the corrected list
        """
        normalized = []
        for inflection in inflections:
            [normalized.append(x.strip()) for x in inflection.split('\n')]

        return normalized

    def process(self,
                search_term: str,
                d_event: dict) -> dict:
        """ Like all OpenAI events there are multiple possible format outcomes

        The optimal outcome is
            {
                'choices': [
                    {
                        'finish_reason': 'stop',
                        'index': 0,
                        'logprobs': None,
                        'text': ' Technologies, technologized, technologizing, technologize, technologizes, technologizing, technologization, technologizations'
                    }
                ]
            }

        Args:
            search_term (str): the term that was searched on
            d_event (dict): the raw result from openAI

        Returns:
            dict: a normalized result
        """

        def has_expected_format() -> bool:
            if 'choices' not in d_event:
                return False
            if not len(d_event['choices']):
                return False
            if 'text' not in d_event['choices'][0]:
                return False
            return True

        if not has_expected_format():
            self.logger.warning('\n'.join([
                "Unexpected OpenAI Outcome",
                pformat(d_event)]))
            return None

        output_text = d_event['choices'][0]['text']

        inflections = [x.strip().lower()
                       for x in output_text.split(',')]

        inflections = self._handle_inner_line_breaks(inflections)

        inflections = self._remove_conflicts(search_term=search_term,
                                             inflections=inflections)

        inflections = [x.strip() for x in inflections]
        inflections = sorted(set(inflections), key=len, reverse=True)

        return inflections
