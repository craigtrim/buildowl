# buildowl (Build OWL)

## Project Purpose
Contains tools and processes behind an integrated API that can aid in the automated construction of an OWL model.

## Capabilities
1. **AutoTaxo**
    -   Given plain text input, generate either a pandas DataFrame or TTL code.  The output will contain high-precision parent-to-child relationships suitable for generating a taxonomical portion of an Ontology.

2. **AutoRels**
    -   Given a source and one-or-more target elements, generate TTL code.  The output will contain well-formatted entities and relationships that adhere to a common naming standard and can be used to augment an existing OWL file.
    -   Given an existing OWL model, the system can generate new relationships over this model.