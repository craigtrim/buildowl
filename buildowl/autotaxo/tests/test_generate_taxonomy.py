from buildowl.autotaxo.svc import GenerateTaxonomyTTL
from buildowl.autotaxo.svc import GenerateTaxonomyDataFrame


def test_service():
    assert GenerateTaxonomyTTL()
    assert GenerateTaxonomyDataFrame()