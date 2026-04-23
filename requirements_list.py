with open("requirements_verified.txt") as f:
    packages = []
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Split on common version specifiers
        pkg = line.split("==")[0].split(">=")[0].split("<=")[0].split(">")[0].split("<")[0].strip()
        if pkg:
            packages.append(pkg)
    result = " ".join(packages)
print(result)



# attrs blis catalogue click cymem Cython exceptiongroup iniconfig Jinja2 joblib jsonschema jsonschema-specifications loguru MarkupSafe medspacy medspacy_quickumls medspacy_unqlite murmurhash nltk "numpy<2" packaging pathlib_abc pathy pluggy preshed pydantic PyFastNER Pygments PyRuSH pysbd pysimstring pytest quicksectx referencing regex requests rpds-py six smart-open spacy spacy-legacy srsly thinc tomli tqdm typer typing_extensions Unidecode wasabi