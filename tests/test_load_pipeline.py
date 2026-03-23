import pytest

from medspacy_pna.util import build_nlp, load_cfg_file, load_rules_from_cfg, RESOURCES_FOLDER

import os

class TestLoadPipeline:
    def test_load_pipeline(self):
        domain = "emergency"
        nlp = build_nlp(domain)

    def test_load_all_domains(self):
        for domain in ["emergency", "radiology", "discharge"]:
            nlp = build_nlp(domain)
            assert nlp is not None

    def test_load_config_file(self):
        filepath = os.path.join(RESOURCES_FOLDER, "configs", "discharge.json")
        cfg = load_cfg_file(filepath)
        assert cfg

    def test_load_rules_from_config(self):
        filepath = os.path.join(RESOURCES_FOLDER, "configs", "discharge.json")
        cfg = load_cfg_file(filepath)
        rules = load_rules_from_cfg(cfg)
        assert set(rules.keys()) == {"context", "sectionizer", "target_matcher", "concept_tagger"}
