from pandas import DataFrame
from tabulate import tabulate


from buildowl.autotaxo.svc import ExtractTextacyNounChunks


def test_service():

    input_text = """
        A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.
        By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.
        Ethernet and Wi-Fi are the two most common technologies in use for local area networks.
        Historical network technologies include ARCNET, Token Ring, and AppleTalk.
    """

    svc = ExtractTextacyNounChunks()
    assert svc

    df = svc.process(
        input_text,
        min_freq=True,
        drop_determiners=True,
        case_sensitive=False,
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
    |  1 | computer network                  |      2 |
    |  2 | limited area                      |      2 |
    |  3 | university campus                 |      2 |
    |  4 | office building                   |      2 |
    |  5 | wide area network                 |      3 |
    |  6 | larger geographic distance        |      3 |
    |  7 | leased telecommunication circuits |      3 |
    |  8 | local area networks               |      3 |
    |  9 | historical network technologies   |      3 |
    | 10 | token ring                        |      2 |
    +----+-----------------------------------+--------+
    """


def main():
    test_service()


if __name__ == "__main__":
    main()
