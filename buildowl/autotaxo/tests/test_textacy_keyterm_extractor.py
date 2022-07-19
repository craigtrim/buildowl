from baseblock import Enforcer

from buildowl.autotaxo.dmo import TextacyKeytermExtractor


def test_component():

    input_text = """
        A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.
        By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.
        Ethernet and Wi-Fi are the two most common technologies in use for local area networks.
        Historical network technologies include ARCNET, Token Ring, and AppleTalk.
    """.strip()

    dmo = TextacyKeytermExtractor()
    assert dmo

    results = dmo.process(top_n=15,
                          input_text=input_text)

    print(results)


def main():
    test_component()


if __name__ == "__main__":
    main()
