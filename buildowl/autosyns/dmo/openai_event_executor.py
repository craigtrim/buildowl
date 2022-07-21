#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Make an actual OpenAI call """


import openai
from pprint import pformat


from baseblock import EnvIO
from baseblock import Enforcer
from baseblock import BaseObject
from baseblock import CryptoBase


class OpenAIEventExecutor(BaseObject):
    """ Make an actual OpenAI call """

    def __init__(self,
                 timeout: int = 15):
        """ Change Log

        Created:
            20-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/5

        Args:
            timeout (int, optional): the timeout for the API call. Defaults to 15.
        """
        BaseObject.__init__(self, __name__)
        self._openai = self._connect()
        self._timeout = EnvIO.int_or_default(
            'OPENAI_CREATE_TIMEOUT', timeout)  # GRAFFL-380

    def _connect(self):
        key = b'gAAAAABiH-eZKbScaS9reXABcCVeRA-VK7rbh-ZBzH72tfzRjTHIH6y5DmcFPxs1Hbf5suJufyD6Z_WhL4h1N1s_BBGpV5JqGZpVCPoB-dAPIFz6gE3uEgUMv_le5RYej5jnZawccsOSKA1RWWpC-CVTcn80S4LehA=='
        org = b'gAAAAABiH-0FMWAwMybowrACJ6GPkC91E4DgaV2lJoextMR7U4O5DjB_pw9jBUusuCdH9KEUXp-3Iq-Fni1X-eE6ulSg8JEKtZs-bClX_D-2DyvYpv65iPs='

        openai.organization = CryptoBase().decrypt(org)
        openai.api_key = CryptoBase().decrypt(key)

        return openai

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
