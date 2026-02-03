<!-- vale off -->

# Rules

This document catalogs the detection rules for aitells.

The rules listed here are aspirational. They represent the detection capabilities the project is working toward, not what's currently implemented.

## Rule structure

Rules use alphanumeric codes following the Ruff convention:

```text
ST001
││└─┘
││ └── Rule number within category
│└──── Category prefix
└───── Layer indicator
```

Rules also have kebab-case names for readability: `ST001` = `triads`.

## Implementation techniques

| Technique | Description                                      | Requires   |
| --------- | ------------------------------------------------ | ---------- |
| Regex     | Multi-pattern matching on raw text               | Hyperscan  |
| NLP       | Syntax trees, POS tagging, dependency parsing    | spaCy      |
| Stats     | Statistical analysis (variance, distributions)   | NumPy      |
| LLM       | Semantic understanding, context-aware judgment   | Claude API |

### Why Hyperscan for regex

[Hyperscan](https://github.com/intel/hyperscan) compiles all patterns into a single database and matches them simultaneously using SIMD. This matters because VF/RM/FT rules have 100+ patterns to check. Traditional regex engines check patterns sequentially; Hyperscan checks them all in one pass. The database can be serialized and reused across runs.

## Selection

```bash
# Select by prefix (all structural rules)
aitells check --select ST docs/

# Select specific rules
aitells check --select ST001,SE001 docs/

# Ignore specific rules
aitells check --ignore VF003 docs/
```

## Categories

### Vocabulary fingerprints (VF)

Words and phrases with documented overrepresentation in AI-generated text.

| Code  | Name                | Technique | Description                                          |
| ----- | ------------------- | --------- | ---------------------------------------------------- |
| VF001 | overused-vocabulary | Regex     | "delve", "tapestry", "multifaceted", etc.            |
| VF002 | formal-register     | Regex     | "utilize", "facilitate", "commence", etc.            |
| VF003 | formal-transitions  | Regex     | "Moreover", "Furthermore", "Additionally", etc.      |
| VF004 | filler-phrases      | Regex     | "a wide range of", "in order to", etc.               |
| VF005 | compound-cliches    | Regex     | "rich tapestry", "delicate balance", etc.            |
| VF006 | organic-consequence | Regex     | "emerges naturally", "flows naturally", etc.         |
| VF007 | hedged-certainty    | Regex     | "It's generally considered..." for undisputed facts  |

### Rhetorical markers (RM)

Phrase patterns indicating specific rhetorical moves.

| Code  | Name                           | Technique | Description                                     |
| ----- | ------------------------------ | --------- | ----------------------------------------------- |
| RM001 | sycophancy                     | Regex     | "Great question!", "I'd be happy to help", etc. |
| RM002 | hedging-phrases                | Regex     | "It's worth noting", "Generally speaking", etc. |
| RM003 | false-balance                  | Regex     | "both sides have merit", "nuanced approach"     |
| RM004 | conclusion-markers             | Regex     | "In conclusion", "To summarize", etc.           |
| RM005 | opening-cliches                | Regex     | "In today's rapidly evolving", etc.             |
| RM006 | metacommentary                 | Regex     | "Let me explain", "The key here is", etc.       |
| RM007 | affirmative-formulas           | Regex     | "That's the beauty of", "Here's the thing"      |
| RM008 | contrastive-formulas           | Regex     | "It's not X; it's Y" patterns                   |
| RM009 | defensive-hedges               | Regex     | "This may seem X, but..." preemptive defense    |
| RM010 | rhetorical-devices             | Regex     | "Ask yourself:", "The test:" patterns           |
| RM011 | self-answering-questions       | NLP+Regex | "What does this mean? It means..." pattern      |
| RM012 | acknowledgment-before-pushback | Regex     | "You make a great point, and..." ritual         |

### Formatting tells (FT)

Punctuation and markdown patterns.

| Code  | Name            | Technique | Description                               |
| ----- | --------------- | --------- | ----------------------------------------- |
| FT001 | em-dash-overuse | Regex     | Overuse of em-dashes for parentheticals   |
| FT002 | emphatic-copula | Regex     | Italicized "is", "are" for false emphasis |

### Structural tells (ST)

Patterns requiring syntax or statistical analysis. Runs locally, no API calls.

| Code  | Name                    | Technique | Description                                              |
| ----- | ----------------------- | --------- | -------------------------------------------------------- |
| ST001 | triads                  | NLP       | Rule-of-three abuse (three items in sequence)            |
| ST002 | parallel                | NLP       | Parallel structure overuse via dependency parsing        |
| ST003 | hedge-stacking          | NLP+Regex | Multiple hedges in close proximity                       |
| ST004 | transition-cadence      | NLP+Regex | Formal transitions at predictable intervals              |
| ST005 | stacked-anaphora        | NLP       | Repeated sentence starts via POS patterns                |
| ST006 | sentence-uniformity     | Stats     | Low variance in sentence length                          |
| ST007 | paragraph-formula       | NLP+Stats | "Topic, three points, conclusion" structure              |
| ST008 | paragraph-uniformity    | Stats     | Low variance in paragraph length                         |
| ST009 | repeated-openers        | NLP       | Consecutive paragraphs with same opener pattern          |
| ST010 | premature-summarization | NLP       | Restating a point immediately after making it            |
| ST011 | unnecessary-enumeration | NLP       | "First... Second... Third..." when ordering adds nothing |

### Semantic tells (SE)

Patterns requiring meaning comprehension. Runs via Claude API.

| Code  | Name               | Technique | Description                                        |
| ----- | ------------------ | --------- | -------------------------------------------------- |
| SE001 | empty-conclusion   | LLM       | Conclusions that restate without adding insight    |
| SE002 | artificial-balance | LLM       | Forced both-sides framing where inappropriate      |
| SE003 | context-sycophancy | LLM       | Validation that's excessive given the context      |
| SE004 | generic-examples   | LLM       | Examples that are too abstract or hypothetical     |
| SE005 | excessive-hedging  | LLM       | Hedging where directness would be appropriate      |
| SE006 | diplomatic-evasion | LLM       | Balanced framing that avoids taking a clear stance |

## Layered detection

Some patterns span multiple categories with increasing sophistication:

### Presence → Density → Appropriateness

**Hedging:**

| Layer           | Rule  | What it catches                               |
| --------------- | ----- | --------------------------------------------- |
| Presence        | RM002 | Individual hedging phrases                    |
| Presence        | VF007 | Hedged certainty on undisputed facts          |
| Density         | ST003 | Multiple hedges clustered in close proximity  |
| Appropriateness | SE005 | Hedging where directness would be appropriate |

**Sycophancy:**

| Layer           | Rule  | What it catches                                |
| --------------- | ----- | ---------------------------------------------- |
| Presence        | RM001 | Sycophantic vocabulary ("Great question!")     |
| Structure       | RM012 | Acknowledgment-before-pushback ritual          |
| Appropriateness | SE003 | Validation excessive given the context         |

This layering lets users choose their detection depth. Run RM rules for fast pattern matching. Add ST rules to catch density-based tells. Add SE rules when you need judgment about whether patterns are contextually appropriate.

## Open questions

- **Density thresholds**: How many hedges in how many sentences constitutes "stacking"?
- **Triad detection**: Should triads in lists be treated differently than triads in prose?
- **Parallel structure**: When is parallelism a stylistic choice vs. a tell?
- **Severity levels**: Should some rules be warnings vs. errors by default?
- **Rule interactions**: How do findings from different rules combine?
