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

    def process(self,
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
            d_event (dict): _description_

        Returns:
            dict: _description_
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

        inflections = [x.strip().lower() for x in
                       d_event['choices']['text'].split(',')]

        return inflections
