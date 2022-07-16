from tabulate import tabulate

from pandas import DataFrame

from buildowl.autotaxo.svc import GenerateTaxonomyTTL
from buildowl.autotaxo.svc import GenerateTaxonomyDataFrame

# ------------------------------------------------------------------------------
# Please Sync with README.md
# ------------------------------------------------------------------------------


def test_service():

    input_text = """
        A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.
        By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.
        Ethernet and Wi-Fi are the two most common technologies in use for local area networks.
        Historical network technologies include ARCNET, Token Ring, and AppleTalk.
    """

    svc = GenerateTaxonomyDataFrame()
    assert svc

    df = svc.process(
        top_n=10,
        input_text=input_text)

    assert df is not None
    assert type(df) == DataFrame

    print(tabulate(df, headers='keys', tablefmt='psql'))
    """
    The Result looks like
    +----+---------------------+-------------------------------+--------------+
    |    | Parent              | Child                         |   Confidence |
    |----+---------------------+-------------------------------+--------------|
    |  0 | network             | area network                  |    0.0764202 |
    |  1 | area network        | local area network            |    0.0764202 |
    |  2 | network             | area network                  |    0.0710775 |
    |  3 | area network        | wide area network             |    0.0710775 |
    |  4 | technology          | network technology            |    0.0689185 |
    |  5 | network technology  | historical network technology |    0.0689185 |
    |  6 | network             | computer network              |    0.0552382 |
    |  7 | distance            | geographic distance           |    0.0369881 |
    |  8 | geographic distance | large geographic distance     |    0.0369881 |
    |  9 | area                | limited area                  |    0.0361508 |
    | 10 | technology          | common technology             |    0.036106  |
    | 11 | circuit             | telecommunication circuit     |    0.0273769 |
    | 12 | building            | office building               |    0.0269569 |
    | 13 | campus              | university campus             |    0.0267514 |
    +----+---------------------+-------------------------------+--------------+
    """

    # Optionally run This
    ttlgen = GenerateTaxonomyTTL()
    results = ttlgen.process(df)
    [print(x) for x in results]

    """
    The Result looks like this (abbreviated):
    ###  http://graffl.ai/pathology#area_network
                :area_network rdf:type owl:Class ;
                rdfs:label "Area Network" ;
                rdfs:subClassOf :network .
    ###  http://graffl.ai/pathology#network
                :network rdf:type owl:Class ;
                rdfs:label "Network" .
    ###  http://graffl.ai/pathology#local_area_network
                :local_area_network rdf:type owl:Class ;
                rdfs:label "Local Area Network" ;
                rdfs:subClassOf :area_network .
    ###  http://graffl.ai/pathology#area_network
                :area_network rdf:type owl:Class ;
                rdfs:label "Area Network" .    
    """


def main():
    test_service()


if __name__ == "__main__":
    main()
