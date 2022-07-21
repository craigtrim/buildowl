#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Orchestrate Taxonomy Generation """


import os

from buildowl.buildr.bp import OwlBuilderAPI


def test_owl_buildr_api():
    api = OwlBuilderAPI()

    model_file_name = api.generate(
        model_name="mytest001",
        model_path=os.getcwd(),
        model_author="ctrim")
    
    print (f"Generated Test Model: {model_file_name}")
    assert os.path.exists(model_file_name)

    version = api.add_entities(
        ttl_entities=[],
        model_file_name=model_file_name)

    assert version == "0.1.1"
    assert os.path.exists(model_file_name)

    version = api.add_entities(
        ttl_entities=[],
        model_file_name=model_file_name)

    assert version == "0.1.2"
    assert os.path.exists(model_file_name)

    version = api.add_entities(
        ttl_entities=[],
        model_file_name=model_file_name)

    assert version == "0.1.3"
    assert os.path.exists(model_file_name)

    version = api.add_entities(
        ttl_entities=[],
        model_file_name=model_file_name)

    assert version == "0.1.4"
    assert os.path.exists(model_file_name)

    os.remove(model_file_name)
    assert not os.path.exists(model_file_name)


def main():
    test_owl_buildr_api()


if __name__ == "__main__":
    main()
