from pandas import DataFrame
from tabulate import tabulate
from baseblock import Enforcer

from buildowl.autotaxo.bp import AutoTaxoOrchestrator
from buildowl.autotaxo.svc import ExtractKeyterms
from buildowl.autotaxo.svc import FilterKeyterms
from buildowl.autotaxo.svc import GenerateTaxonomyDataFrame
from buildowl.autotaxo.svc import GenerateTaxonomyTTL
from buildowl.autotaxo.dto import load_model


input_text = """
    A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.
    By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.
    Ethernet and Wi-Fi are the two most common technologies in use for local area networks.
    Historical network technologies include ARCNET, Token Ring, and AppleTalk.
""".strip()


def test_bp():
    bp = AutoTaxoOrchestrator()
    assert bp

    results = bp.ttlresults(input_text)
    Enforcer.is_list_of_str(results)


def test_service():

    model = load_model()

    extract = ExtractKeyterms(model).process
    assert extract

    df = extract(input_text)
    print(tabulate(df, headers='keys', tablefmt='psql'))

    filter = FilterKeyterms().process
    assert filter

    terms = filter(df)
    print (terms)

    gendf = GenerateTaxonomyDataFrame().process
    assert gendf

    df = gendf(terms)
    print(tabulate(df, headers='keys', tablefmt='psql'))

    ttlgen = GenerateTaxonomyTTL().process
    assert ttlgen

    results = ttlgen(df)
    print (">>>> ", results)
    [print(x) for x in results]
    Enforcer.is_list_of_str(results)


def main():
    test_service()


if __name__ == "__main__":
    main()
