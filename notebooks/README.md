# Notebooks

Experimental notebooks for developing detection techniques before extracting to `src/aitells`.

## Setup

```bash
uv sync --group notebooks
just spacy-models
```

Open notebooks in VS Code or your preferred Jupyter environment.

## Naming conventions

**Rule-specific notebooks** use rule codes as prefixes to match `docs/design/rules.md`:

- `ST001_triads.ipynb` - triad detection experiments
- `ST002_parallel_structures.ipynb` - parallel structure analysis

**General exploration notebooks** use numeric prefixes:

- `00_spacy_basics.ipynb` - learning spaCy fundamentals
- `01_dependency_parsing.ipynb` - exploring parse trees

## Samples directory

Text samples for testing detection techniques:

| Directory | Contents |
| --------- | -------- |
| `samples/ai_generated/` | Known AI-generated text for positive cases |
| `samples/human_written/` | Human-written text for negative cases |
| `samples/edge_cases/` | Ambiguous or boundary cases |

## Workflow

1. Experiment in notebook until technique works
2. Extract working code to `src/aitells`
3. Keep notebook as testbed for edge cases and iteration
