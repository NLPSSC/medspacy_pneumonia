# Examples Matches

This document gives an overview of the MedspaCy pneumonia relative to what it will capture.  The pipeline itself
is a rules-based model, using key words, regular expressions, and patterns to capture phrases.  The purpose of
this document is to give an overview to help inform what this pipeline will produce.

## Overview

The following describes how to read examples in this document.

### Tags versus Token

For purposes of this document, a token can just be considered a word, and it will be represented in lower case
(e.g., "acute").  A token is a place holder, and will be represented in upper case (e.g., PNEUMONIA).  

### Shorthand Notation Used

This is a rule-based system that allows for cases like "zero or more" or "one or more" instances of a set of words
(a.k.a tokens).  Within this document if you see 

[...]* 

this means zero or more of the token or tag in the brackets, and

[...]+

means one or more of the token or tag.

### Tags

Here is a list of tokens (words) pulled from the configuration files within the pipeline for different tags.  Information
about tag use will follow this section.  This is not a comprehensive list, as it excludes potential partial matches.  The
intent is to provide an initial review for later discussion.

#### PNEUMONIA
- pneumonia
- pneumonias
- pneumoniae
- pna
- bronchopneumonia
- pleuropneumonia
- pneumonitis
- legionellosis
- legionnaire
- HCAP

#### ATELECTASIS
- atelectasis

#### INFILTRATE
- infiltrate
- infiltrates
- infiltration
- infiltrative

#### CONSOLIDATION
- consolidation
- consolidations
- consolidate
- consolidative

#### PATCHY
- patchy

#### FOCAL
- focal

#### DENSITY
- density
- densities

#### COVID
- covid
- covid-19
- sars-cov-2
- coronavirus

#### LINEAR
- linear
- some linear features
- strandy linear
- linear features
- streaky
- strandy-linear

#### STREAKY
- streaky
- streaking

#### STRANDING
- stranding

#### OPACITY
- opacity
- opacities
- opacification
- opacified

#### TREATMENT
- treatment
- antibiotics
- therapy
- treated
- management
- managed


### Tags and Tokens as Phrase Matches

The following is a short of list of *possible* matches (since producing all possible combinations would rapidly get out of hand with term expansion).  

#### Possible Matches

1. "acute chest disease" (and variants)
    - acute chest disease
    - acute lung disease
    - acute cardiopulmonary process
    - acute findings
    - acute disease
2. "infectious/inflammatory process"
infectious process
inflammatory process
3. "pneumonia and/or atelectasis"
    - [PNEUMONIA]+ and [ATELECTASIS]+
    - [PNEUMONIA]+ or [ATELECTASIS]+
    - [PNEUMONIA]+ and/or [ATELECTASIS]+
    - [ATELECTASIS]+ and [PNEUMONIA]+
    - [ATELECTASIS]+ or [PNEUMONIA]+
    - [ATELECTASIS]+ and/or [PNEUMONIA]+
4. "pneumonia and/or infiltrate"
    - [ATELECTASIS]+ and [INFILTRATE]+
    - [ATELECTASIS]+ or [INFILTRATE]+
    - [ATELECTASIS]+ and/or [INFILTRATE]+
    - [ATELECTASIS]+ / [INFILTRATE]+
    - [INFILTRATE]+ and [ATELECTASIS]+
    - [INFILTRATE]+ or [ATELECTASIS]+
    - [INFILTRATE]+ and/or [ATELECTASIS]+
    - [INFILTRATE]+ / [ATELECTASIS]+
5. "pneumon*/atelectasis"
    - pneumonitis and atelectasis
    - pneumonia or atelectasis
    - pneumonic and/or atelectasis
    - pneumon/atelectasis
6. "airspace disease"
    - airspace disease
    - air space disease
7. "consolidation" (from common/target_rules.json)
    - [PATCHY|FOCAL]* [CONSOLIDATION]+ (e.g., patchy consolidation, focal consolidation, consolidation)
8. "infiltrate"
    - [INFILTRATE]+ [DENSITY]* (e.g., infiltrate, infiltrates, infiltrate patchy)
9. "density"
    - [FOCAL|PATCHY]* [DENSITY]+ (e.g., patchy density, focal density, density)
10. "pneumonia"
    - [FOCAL|INFILTRATE|COVID]* [PNEUMONIA]+ (e.g., focal pneumonia, infiltrate pneumonia, pneumonia)
11. "opacity"
    - [LINEAR|STREAKY|STRANDING]* [OPACITY]+ (e.g., streaky opacity, opacity)
12. "treatment for pneumonia"
    - [TREATMENT]+ for [PNEUMONIA]+ (e.g., antibiotics for pneumonia)
13. "Klebsiella/other pneumonia"
    - klebsiella pneumonia
    - chlamydophila pneumonia
    - mycoplasma pneumonia
14. "interstitial pneumonia"
    - interstitial pneumonia
15. "pneumonia vaccination"
    - pneumonia vaccination
    - pneumonia vaccine
16. "atelectasis"
    - [ATELECTASIS]+
17. "fibrotic"
    - fibrotic tissue
    - fibrotic
18. "Pneumonia"
19. "Pneumonia No"
20. "pneumonitis"
pneumonitis

