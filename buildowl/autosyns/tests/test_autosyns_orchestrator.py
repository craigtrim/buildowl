from baseblock import Enforcer

from buildowl.autosyns.bp import AutoSynsOrchestrator


import os
os.environ['USE_OPENAI'] = str(False)


input_text = """
    A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.
    By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.
    Ethernet and Wi-Fi are the two most common technologies in use for local area networks.
    Historical network technologies include ARCNET, Token Ring, and AppleTalk.
""".strip()


def test_orchestrator():
    bp = AutoSynsOrchestrator()
    assert bp

    result = bp.process(input_text)

    if result:
        [print(x) for x in result]
        Enforcer.is_list_of_str(result)


def main():
    os.environ['USE_OPENAI'] = str(True)
    test_orchestrator()


if __name__ == "__main__":
    main()
