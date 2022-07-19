from pprint import pprint

from baseblock import Enforcer

from buildowl.autotaxo.dto import FuzzyWuzzyWrapper


def test_service():

    wrapper = FuzzyWuzzyWrapper()
    d_results = wrapper.process(s1='computer techonology',
                                s2='computer technologies',
                                basic=True,
                                q_ratio=True,
                                w_ratio=True,
                                uq_ratio=True,
                                uw_ratio=True,
                                partial_ratio=True,
                                token_sort_ratio=True)

    Enforcer.is_dict(d_results)
    pprint(d_results)

    assert d_results == {
        "ratios": {
            "basic": 88,
            "partial": 90,
            "q": 88,
            "token_sort": 88,
            "uq": 88,
            "uw": 88,
            "w": 88
        },
        "score": 88.3,
        "text": {
            "s1": "computer techonology",
            "s2": "computer technologies"
        }
    }


def main():
    test_service()


if __name__ == "__main__":
    main()
