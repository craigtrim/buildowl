#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" OpenAI: Generate Inflection Prompts """


from pprint import pprint
from typing import Callable

from baseblock import EnvIO
from baseblock import Stopwatch
from baseblock import BaseObject
from baseblock import Enforcer

from baseblock import ServiceEventGenerator

from buildowl.autosyns.dmo import OpenAIEventExecutor
from buildowl.autosyns.dmo import OpenAIOutputExtractor
from buildowl.autosyns.dto import OpenAICache


class GenerateInflectionCall(BaseObject):
    """ OpenAI: Generate Inflection Prompts """

    __generate_event = None
    __execute_event = None
    __extract_output = None

    def __init__(self):
        """
        Created:
            20-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/5
        """
        BaseObject.__init__(self, __name__)
        cache = OpenAICache()
        self._exists_in_cache = cache.exists
        self._write_to_cache = cache.write
        self._read_from_cache = cache.read

    def _generate_event(self) -> Callable:
        if not self.__generate_event:
            self.__generate_event = ServiceEventGenerator().process
        return self.__generate_event

    def _execute_event(self) -> Callable:
        if not self.__execute_event:
            self.__execute_event = OpenAIEventExecutor().process
        return self.__execute_event

    def _extract_output(self) -> Callable:
        if not self.__extract_output:
            self.__extract_output = OpenAIOutputExtractor().process
        return self.__extract_output

    def process(self,
                input_text: str,
                temperature: float = 0.7,
                max_tokens: int = 512,
                top_p: float = 1.0,
                best_of: int = 1,
                frequency_penalty: float = 0.0,
                presence_penalty: float = 0.0) -> dict or None:
        """ Call the OpenAI Text Summarizer

        Args:
            input_text (str): the input text to send to OpenAI
            temperature (float, optional): Controls Randomness. Defaults to 0.7.
                as the value approaches 0.0 the model becomes deterministic and repetitive
            max_tokens (int, optional): the maximum number of tokens to generate. Defaults to 64.
                the max is 2048 and the tokens are shared between input and output
            top_p (float, optional): controls diversity via nucleus sampling. Defaults to 1.0.
            frequency_penalty (float, optional): how much to penalize new tokens based on their existing frequency. Defaults to 0.0.
                decreases the model's likelihood to repeat the same line verbatim
            presence_penalty (float, optional): how much to penalize new tokens based in the text. Defaults to 0.0.
                increases the model's likelihood to talk about new topics

        Returns:
            dict: the complete openAI event
        """

        if self._exists_in_cache(input_text):
            return self._read_from_cache(input_text)

        if not EnvIO.is_true("USE_OPENAI"):
            return None

        sw = Stopwatch()
        if self.isEnabledForDebug:
            Enforcer.is_str(input_text)

        prompt_input = f"""
Generate all the English inflections for a word

Word: troubleshoot
Inflections: troubleshoots,troubleshooting,troubleshooted,troubleshooter,troubleshooters
Word: computer
Inflections: computers, computerized, computerizing, computerize, computerizes, computerizing, computerization, computerizations

Word: {input_text}
Inflections:  

        """

        d_openai_input = {
            'input_text': input_text,
            'prompt_input': prompt_input,
            'engine': 'text-davinci-002',
            'temperature': temperature,
            'max_tokens': max_tokens,
            'top_p': top_p,
            'best_of': best_of,
            'frequency_penalty': frequency_penalty,
            'presence_penalty': presence_penalty,
        }

        d_openai_output = self._execute_event()(d_openai_input)
        inflections = self._extract_output()(search_term=input_text,
                                             d_event=d_openai_output)

        # GRAFFL-278; Generate an Event Record
        d_event = self._generate_event()(
            service_name=self.component_name(),
            event_name='generate-inflection-call',
            stopwatch=sw,
            data={
                'input_text': input_text,
                'output_text': inflections,
                'openai_input': d_openai_input,
                'openai_output': d_openai_output,
            })

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                f"OpenAI Service Completed ({d_event['service']})",
                f"\tTotal Time: {str(sw)}",
                f"\tInput Text: {input_text.strip()}",
                f"\tOutput Text: {inflections}"]))

        result = {
            'inflections': inflections,
            'events': [d_event]
        }

        self._write_to_cache(data=result,
                             file_name=input_text)
        return result
