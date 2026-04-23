import platform
from pathlib import Path
from invoke import task  # type: ignore


@task
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


def get_current_folder_temp_venv_path() -> Path:
    current_folder: Path = Path.cwd()
    temp_venv_path: Path = current_folder / ".temp_venv"
    return temp_venv_path


@task
def remove_install_venv(c):
    """
    Remove the temporary virtual environment
    """
    import shutil
    from pathlib import Path

    temp_venv_path: Path = get_current_folder_temp_venv_path()
    if temp_venv_path.exists():
        shutil.rmtree(temp_venv_path)


@task
def create_install_venv(c):
    """
    Create a virtual environment, install the required packages, and patch the medspacy sentence splitting code
    """

    import sys
    from pathlib import Path

    remove_install_venv(c)

    temp_venv_path: Path = get_current_folder_temp_venv_path()

    # create a temporary virtual environment named .temp_venv
    c.run(f"{sys.executable} -m venv {temp_venv_path}")
    c.run(
        f"{temp_venv_path}\\Scripts\\python -m pip install toml_sort taplo uv && {temp_venv_path}\\Scripts\\python -m pip install --upgrade pip"
    )


@task(pre=[create_install_venv], post=[remove_install_venv])
def build_pyproject(c):
    """
    Build the pyproject.toml file using poetry
    """
    import subprocess
    from pathlib import Path

    # No need to activate the venv; use the venv python directly for subprocesses

    # Paths
    requirements_path = Path("windows.requirements.txt")
    pyproject_path = Path("pyproject.toml")
    pyproject_path.unlink(
        missing_ok=True
    )  # Remove existing pyproject.toml to avoid conflicts

    # 1. Run uv init to create pyproject.toml if it doesn't exist
    if not pyproject_path.exists():
        subprocess.run(["uv", "init"], check=True)

    # 2. Parse requirements.txt
    deps = []
    with open(requirements_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Only keep lines with package[==version] or similar
            if (
                "==" in line
                or ">=" in line
                or "<=" in line
                or "~=" in line
                or ">" in line
                or "<" in line
            ):
                deps.append(line)
            else:
                deps.append(line)

    # 3. Insert dependencies into pyproject.toml using tomlkit only
    from tomlkit import parse, dumps, table, inline_table

    if pyproject_path.exists():
        with open(pyproject_path, "r") as f:
            pyproject = parse(f.read())
    else:
        pyproject = table()

    if "project" not in pyproject:
        pyproject["project"] = table()
    pyproject["project"]["name"] = "medspacy-pneumonia"
    pyproject["project"]["version"] = "0.1.0"
    pyproject["project"][
        "description"
    ] = "A medspacy pipeline for pneumonia detection in clinical text. (Windows Environment Definition)"
    pyproject["project"]["readme"] = "README.md"
    pyproject["project"]["requires-python"] = ">=3.9,<3.12"
    if "en_core_web_sm" not in deps:
        deps.append("en_core_web_sm")
    pyproject["project"]["dependencies"] = deps  # deps should be a list of strings

    # Ensure nested structure for [tool.uv.sources]
    if "tool" not in pyproject:
        pyproject["tool"] = table()
    if "uv" not in pyproject["tool"]:
        pyproject["tool"]["uv"] = table()
    pyproject["tool"]["uv"]["override-dependencies"] = ["pydantic==1.10.21"]
    if "sources" not in pyproject["tool"]["uv"]:
        pyproject["tool"]["uv"]["sources"] = table()

    en_core_web_sm = inline_table()
    en_core_web_sm["url"] = (
        "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.1.0/en_core_web_sm-3.1.0-py3-none-any.whl"
    )
    pyproject["tool"]["uv"]["sources"]["en-core-web-sm"] = en_core_web_sm

    # Add [project.optional-dependencies] section
    from tomlkit import aot, array, table

    if "optional-dependencies" not in pyproject["project"]:
        pyproject["project"]["optional-dependencies"] = table()

    pyproject["project"]["optional-dependencies"]["adjudication"] = array()
    pyproject["project"]["optional-dependencies"]["adjudication"].extend(
        [
            "ipython>=8.18.1",
            "ipywidgets>=8.1.8",
            "matplotlib>=3.9.4",
            "scikit-learn>=1.6.1",
            "seaborn>=0.13.2",
        ]
    )

    pyproject["project"]["optional-dependencies"]["dev"] = array()
    pyproject["project"]["optional-dependencies"]["dev"].append("pytest>=8.4.2")

    pyproject["project"]["optional-dependencies"]["tasks"] = array()
    pyproject["project"]["optional-dependencies"]["tasks"].append("invoke>=2.2.1")

    with open(pyproject_path, "w") as f:
        f.write(dumps(pyproject))

    temp_venv_path: Path = get_current_folder_temp_venv_path()

    initial_sort_cmd = f"uv run toml-sort --in-place --all --spaces-indent-inline-array 4 --trailing-comma-inline-array --sort-first name,version,description pyproject.toml"
    subprocess.run(initial_sort_cmd, shell=True, check=True)
    second_sort_cmd = f"uv run taplo format --option reorder_keys=false --option column_width=80 pyproject.toml"
    subprocess.run(second_sort_cmd, shell=True, check=True)

    print("pyproject.toml created and dependencies added.")
