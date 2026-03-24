from invoke.tasks import task


@task()
def patch_medpsacy_sentence_splitting(c):
    """
    Find the path to the medspacy package in the .venv, then patch the sentence splitting component
    to patch the code


    @Language.factory("medspacy_pyrush")
    def create_pyrush(nlp, name, pyrush_path=None):
        if pyrush_path is None:
            pyrush_path = path.join(Path(__file__).resolve().parents[1], "resources", "rush_rules.tsv")
        return PyRuSHSentencizer(pyrush_path)

    to

    if "medspacy_pyrush" not in spacy.registry.factories:
        @Language.factory("medspacy_pyrush")
        def create_pyrush(nlp, name, pyrush_path=None):
            if pyrush_path is None:
                pyrush_path = path.join(Path(__file__).resolve().parents[1], "resources", "rush_rules.tsv")
            return PyRuSHSentencizer(pyrush_path)
    """

    import spacy
    from os import path
    from pathlib import Path

    # Get the path to "site-packages" in the .venv
    import sys

    venv_path = Path(sys.prefix)
    site_packages_path = venv_path / "Lib" / "site-packages"
    sentence_splitting_path = site_packages_path / "medspacy" / "sentence_splitting.py"
    with open(sentence_splitting_path, "r") as f:
        code = f.read()

    if 'if "medspacy_pyrush" not in spacy.registry.factories:' in code:
        print("Code already patched")
        return

    replacement_code = """import spacy
if "medspacy_pyrush" not in spacy.registry.factories:
    @Language.factory("medspacy_pyrush")
    def create_pyrush(nlp, name, pyrush_path=None):
        if pyrush_path is None:
            pyrush_path = path.join(Path(__file__).resolve().parents[1], "resources", "rush_rules.tsv")
        return PyRuSHSentencizer(pyrush_path)
"""

    original_code = """@Language.factory("medspacy_pyrush")
def create_pyrush(nlp, name, pyrush_path=None):
    if pyrush_path is None:
        pyrush_path = path.join(Path(__file__).resolve().parents[1], "resources", "rush_rules.tsv")
    return PyRuSHSentencizer(pyrush_path)
"""

    new_code = code.replace(
        original_code,
        replacement_code,
    )

    assert replacement_code in new_code

    # backup the original file
    with open(sentence_splitting_path.with_suffix(".py.bak"), "w") as f:
        f.write(code)

    with open(sentence_splitting_path, "w") as f:
        f.write(new_code)

    print("Code patched successfully")


if __name__ == "__main__":
    from invoke.context import Context

    context = Context()
    patch_medpsacy_sentence_splitting(context)
