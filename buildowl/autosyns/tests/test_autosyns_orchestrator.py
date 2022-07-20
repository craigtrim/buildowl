from pandas import DataFrame
from tabulate import tabulate

from baseblock import Enforcer

from buildowl.autosyns.bp import AutoSynsOrchestrator

input_text = """
    A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.
    By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.
    Ethernet and Wi-Fi are the two most common technologies in use for local area networks.
    Historical network technologies include ARCNET, Token Ring, and AppleTalk.
""".strip()


def test_orchestrator():
    bp = AutoSynsOrchestrator()
    assert bp

    bp.process(input_text)


def main():
    test_orchestrator()


if __name__ == "__main__":
    main()
