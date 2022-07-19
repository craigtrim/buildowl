
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from spacy.lang.en import English
from textacy import load_spacy_lang


def load_model() -> English:
    """ Load spaCy model consistently

    Returns:
        English: an activated spaCy model
    """
    return load_spacy_lang("en_core_web_sm")
