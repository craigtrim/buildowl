from pandas import DataFrame
from tabulate import tabulate

from buildowl.autotaxo.svc import ExtractKeyterms


def test_service():

    input_text = """
        A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.
        By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.
        Ethernet and Wi-Fi are the two most common technologies in use for local area networks.
        Historical network technologies include ARCNET, Token Ring, and AppleTalk.
    """.strip()

    svc = ExtractKeyterms()
    assert svc

    df = svc.process(input_text)
    print(tabulate(df, headers='keys', tablefmt='psql'))

    terms = [x.lower()
             for x in list(df['Term'].unique()) if len(x.split()) > 1]
    terms = sorted(set(terms), key=len, reverse=True)
    [print(x) for x in terms]


def main():
    test_service()


if __name__ == "__main__":
    main()
