from baseblock import Enforcer

from buildowl.autorels.svc import FindImpliesRelationships


def test_service():
    svc = FindImpliesRelationships()
    assert svc

    input_terms = [
        'network hardware',
        'network protocol',
        'network',
        'protocol'
    ]

    actual_results = svc.process(input_terms)
    Enforcer.is_list_of_dicts(actual_results)


def main():
    test_service()


if __name__ == "__main__":
    main()
