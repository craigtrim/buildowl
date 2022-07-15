from buildowl.autotaxo.svc import ExtractTextacyNgrams


def test_service():

    input_text = """
Babies typically demonstrate limitation of the speech sounds they hear between the ages of 7 months and 1 year. 
Between birth and 3 months, they typically coo, goo, differentiate their crying according to different needs, and smile at parents. 
From around 4 to 6 months, they normally babble including speech sounds like /m/,/p/, and /b/; laugh and chuckle; gurgle; and vocally express unhappiness and excitement. 
From 1 year to 18 months, children normally begin uttering words, use one-and/or two-word questions and phrases, and acquire many different word-initial consonants. 
Pragmatics is the domain of language focused on language use in social contexts, including how it affects others. Semantics  is the domain of language focused on the meanings of words. 
Phonology  is the domain of language focused on speech sounds and their relationships and systems. Syntax  is the domain of language focused on word order and sentence structure. 
Typical motor skills development of a 1-year-old includes using the forefinger to point at and/or poke things and people. 
Cognitive skills  of a typically developing 1-year-old include searching for objects he or she has seen that have moved out of his or her sight. 
Sensory skills  of a typical 1-year-old include moving his or her body to music and limitating adult sounds.
    """.strip()

    svc = ExtractTextacyNgrams()
    assert svc

    results = svc.process(
        input_text,
        term_frequency=1)
    assert results
