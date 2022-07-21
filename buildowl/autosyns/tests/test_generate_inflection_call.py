from baseblock import EnvIO
from baseblock import Enforcer


from buildowl.autosyns.svc import GenerateInflectionCall


import os
os.environ['USE_OPENAI'] = str(False)


def test_service():
    os.environ['AUTOSYN_CACHE_PATH'] = os.path.normpath(
        os.path.join(EnvIO.str_or_exception('BUILDOWL_HOME'),
                     'resources/cache/syns'))

    svc = GenerateInflectionCall()
    assert svc

    d_result = svc.process("hospital")
    if d_result:
        Enforcer.is_dict(d_result)

        print('\n'.join([
            "Retrieved Inflections",
            f"\tInput: technology",
            f"\tResults: {d_result['inflections']}"]))


def main():
    os.environ['USE_OPENAI'] = str(True)
    test_service()


if __name__ == "__main__":
    main()
