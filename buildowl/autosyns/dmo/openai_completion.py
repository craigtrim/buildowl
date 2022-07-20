#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Make an actual OpenAI call """


from pprint import pformat


from baseblock import EnvIO
from baseblock import Enforcer
from baseblock import BaseObject


class OpenAICompletion(BaseObject):
    """ Make an actual OpenAI call """

    def __init__(self,
                 openai: object,
                 timeout: int = 15):
        """ Change Log

        Created:
            20-Jul-2022
            craig@graffl.ai
            *   https://github.com/craigtrim/buildowl/issues/5

        Args:
            openai (object): an openAI connection
            timeout (int, optional): the timeout for the API call. Defaults to 15.
        """
        BaseObject.__init__(self, __name__)
        self._openai = openai
        self._timeout = EnvIO.int_or_default(
            'OPENAI_CREATE_TIMEOUT', timeout)  # GRAFFL-380

    def process(self,
                d_event: dict) -> dict:

        if self.isEnabledForDebug:
            Enforcer.is_dict(d_event)

        if 'best_of' not in d_event:
            d_event['best_of'] = 1

        response = self._openai.Completion.create(
            engine=d_event['engine'],
            prompt=d_event['prompt_input'],
        temperature=d_event['temperature'],
            max_tokens=d_event['max_tokens'],
            top_p=d_event['top_p'],
            best_of=d_event['best_of'],
            frequency_penalty=d_event['frequency_penalty'],
            presence_penalty=d_event['presence_penalty'],
            timeout=self._timeout  # GRAFFL-380
        )

        d_result = dict(response)
        if self.isEnabledForDebug:

            Enforcer.is_dict(d_event)
            self.logger.debug('\n'.join([
                "OpenAI Call Completed",
                pformat(d_result)]))

        return d_result
