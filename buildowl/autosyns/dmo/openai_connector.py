#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Connect to OpenAI """


import openai

from baseblock import BaseObject
from baseblock import CryptoBase


class OpenAIConnector(BaseObject):
    """ Connect to OpenAI """

    def __init__(self):
        """
        Created:
            20-Jul-2022
            craig@graffl.ai
            *   https://github.com/craigtrim/buildowl/issues/5
        """
        BaseObject.__init__(self, __name__)

    def process(self) -> object:
        key = b'gAAAAABiH-eZKbScaS9reXABcCVeRA-VK7rbh-ZBzH72tfzRjTHIH6y5DmcFPxs1Hbf5suJufyD6Z_WhL4h1N1s_BBGpV5JqGZpVCPoB-dAPIFz6gE3uEgUMv_le5RYej5jnZawccsOSKA1RWWpC-CVTcn80S4LehA=='
        org = b'gAAAAABiH-0FMWAwMybowrACJ6GPkC91E4DgaV2lJoextMR7U4O5DjB_pw9jBUusuCdH9KEUXp-3Iq-Fni1X-eE6ulSg8JEKtZs-bClX_D-2DyvYpv65iPs='

        openai.organization = CryptoBase().decrypt(org)
        openai.api_key = CryptoBase().decrypt(key)

        return openai
