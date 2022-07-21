from buildowl.autosyns.svc import GenerateInflectionCall
from baseblock import Enforcer
from tabulate import tabulate
from pandas import DataFrame


import os
os.environ['USE_OPENAI'] = str(False)


def test_service():
    """ not a standard unit test
        I don't want this called during the build phase - because this involves a live OpenAI call
        this test must be invoked manually
    """

    print(">>> os.environ['USE_OPENAI']: ", os.environ['USE_OPENAI'])

    svc = GenerateInflectionCall()
    assert svc

    inflections, _ = svc.process("technology")
    print ("inflections>>> ", inflections)


# def temp(word: str):
#     if word[-1] == 's':
#         return [word]
#     if word[-1] == 'e' and word[-2] not in diphthongs and word[-2] not in triphthongs and word[-3] not in ['i', 'e', 'o', 'u', 'y', 'a']:
#         return [word]
#     if word[-1] == 'y' and word[-2] not in diphthongs and word[-2] not in triphthongs:
#         return [word]
#     if word[-1] == 'd':
#         return [word]
#     if word[-1] == 'l':
#         if word[-2] == 'l':
#             return [word]
#         return [word, word[:-1]+'ing']
#     if word[-1] == 'r':
#         if word[-2] == 'r':
#             return [word]
#         return [word, word[:-1]+'ing']


def main():
    os.environ['USE_OPENAI'] = str(True)
    test_service()


if __name__ == "__main__":
    main()
