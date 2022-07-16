from pandas import DataFrame
from tabulate import tabulate


from buildowl.autotaxo.svc import ExtractTextacyNgrams


def test_service():

    input_text = """
        A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.
        By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.
        Ethernet and Wi-Fi are the two most common technologies in use for local area networks.
        Historical network technologies include ARCNET, Token Ring, and AppleTalk.
    """

    svc = ExtractTextacyNgrams()
    assert svc

    df = svc.process(
        input_text,
        filter_stops=True,
        term_frequency=1,
        as_dataframe=True)

    assert df is not None
    assert type(df) == DataFrame

    print(tabulate(df, headers='keys', tablefmt='psql'))

    """
    The Result looks like
    +----+-----------------------------------+--------+
    |    | Text                              |   Size |
    |----+-----------------------------------+--------|
    |  0 | local area network                |      3 |
    |  1 | wide area network                 |      3 |
    |  2 | larger geographic distance        |      3 |
    |  3 | leased telecommunication circuits |      3 |
    |  4 | local area networks               |      3 |
    |  5 | historical network technologies   |      3 |
    |  6 | technologies include arcnet       |      3 |
    +----+-----------------------------------+--------+
    """


def main():
    test_service()


if __name__ == "__main__":
    main()
