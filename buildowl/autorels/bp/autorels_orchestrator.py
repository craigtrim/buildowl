#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Orchestrate Taxonomy Generation """


from baseblock import BaseObject


class AutoRelsOrchestrator(BaseObject):
    """ Orchestrate Taxonomy Generation """

    def __init__(self):
        """ Change Log:

        Created:
            18-Jul-20922
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/4

        """
        BaseObject.__init__(self, __name__)

    def process(self,
                terms: list) -> list or None:

        return terms
    