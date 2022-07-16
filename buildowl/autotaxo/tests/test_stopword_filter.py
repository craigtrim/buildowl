from buildowl.autotaxo.dmo import StopWordFilter


def test_component():

    dmo = StopWordFilter()
    assert dmo

    assert dmo.has_stopword('network that interconnects')
    assert not dmo.has_stopword('leased telecommunication circuits')
