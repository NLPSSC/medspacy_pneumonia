# Understanding The Pipeline

## MedspaCy Concepts

This code base has config file that define the way in which pneumonia is defined for different clinical note types (`domain`).  These inform four parts of the MedspaCy pipeline:

    - **Concept Tagger**: Identifies and labels clinical concepts (e.g., diseases, symptoms, anatomy) in the text using rule-based patterns. It assigns entity labels to spans of text that match predefined rules.
    - **Target Matcher**: Finds specific clinical targets or phrases of interest (e.g., mentions of pneumonia, findings, or procedures) using pattern rules. It’s often used to flag key terms for further analysis.
    - **Context**: Determines the context of identified concepts, such as negation (e.g., “no pneumonia”), uncertainty, temporality, or experiencer (e.g., “family history of pneumonia”). This is crucial for accurate clinical interpretation.
    - **Sectionizer**: Segments the document into logical sections (e.g., “History of Present Illness”, “Impression”, “Findings”) based on section headers or patterns. This helps in associating findings with the correct part of the document.

**Example**

Within the `domain` of radiology notes, the configuration for these parts of the pipeline are found in [medspacy_pna\resources\configs\radiology.json](medspacy_pna\resources\configs\radiology.json).

```json
{
  "domain": "radiology",
  "resources": [
    {
      "concept_tagger": [
        "common/anatomy_concept_tag_rules.json",
        "common/concept_tag_rules.json"
      ],
      "target_matcher": [
        "common/target_rules.json",
        "radiology/radiology_target_rules.json"
      ],
      "context": [
        "common/context_rules.json",
        "radiology/radiology_context_rules.json",
        "common/anatomy_descriptor_modifier_rules.json"
      ],
      "sectionizer": [
        "radiology/radiology_section_rules.json"
      ]
    }
  ]
}
```

literal: For documentation and reference.
category: To assign a semantic label to matched text.
pattern: To specify how to find the relevant text spans in the document.