from pandas import DataFrame
from tabulate import tabulate

from baseblock import Enforcer

from buildowl.autorels.bp import AutoRelsOrchestrator


def test_orchestrator():
    bp = AutoRelsOrchestrator()
    assert bp

    input_terms = [
        'network hardware',
        'network protocol',
        'network',
        'protocol'
    ]

    df_results = bp.dataframe(input_terms)
    assert df_results is not None
    assert type(df_results) == DataFrame

    print(tabulate(df_results, headers='keys', tablefmt='psql'))


def main():
    test_orchestrator()


if __name__ == "__main__":
    main()
