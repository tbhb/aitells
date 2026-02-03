# AI Tells

A tool for detecting linguistic patterns commonly associated with AI-generated prose. Complements vale-ai-tells with deeper rhetorical analysis using NLP and LLMs.

Early development (0.x). Python 3.13+.

## Related projects

This project is the programmatic sibling of [vale-ai-tells](https://github.com/tbhb/vale-ai-tells), a Vale package that detects AI writing patterns through regex-based rules. While vale-ai-tells catches vocabulary fingerprints and simple structural patterns, aitells goes deeper: detecting rule-of-three abuse, parallel structure overuse, and other rhetorical tells that require NLP or LLM analysis.

## Tone

Appreciate the irony: you're an AI working on a tool that detects AI writing. Lean into it. Find the humor in flagging your own tendencies, catching yourself mid-cliche, and helping humans spot the patterns you're statistically prone to produce. The self-awareness is the point.

## How we work

This project is a collaboration between Tony, Claude Code, and Claude on claude.ai. Tony provides direction and makes decisions. Claude Code handles implementation: writing code, running tests, managing git. Claude on claude.ai contributes research, design thinking, and longer-form analysis. Work products flow between contexts through the repository and shared documentation.

## Repository structure

```text
aitells/
├── .claude/           # Claude Code configuration
├── .github/           # GitHub workflows and templates
├── docs/              # Documentation (design/, reference/, guides/)
├── src/aitells/       # Python source code
├── tests/             # Test suite
├── Justfile           # Development recipes
├── pyproject.toml     # Project configuration and dependencies
└── mkdocs.yml         # Documentation site configuration
```

## Development workflow

### Setup

```bash
just install
```

### Common recipes

| Recipe | Purpose |
| ------ | ------- |
| `just lint` | Run all linters (Python, docs, config, spelling) |
| `just format` | Format code (ruff, biome, codespell) |
| `just fix` | Fix linting issues automatically |
| `just test` | Run tests (excludes benchmarks/slow) |
| `just test-coverage` | Run tests with coverage reporting |
| `just dev-docs` | Local documentation preview at localhost:8000 |
| `just prek` | Run pre-commit hooks on changed files |

### Verification

After making changes, run `just lint` and `just test` to verify.

## Writing style

All prose must pass `just lint-prose` (vale) with no errors and no warnings.

When writing or editing prose:

- Use sentence case for headlines
- Prefer simple words: "use" not "utilize", "help" not "facilitate"
- Be direct. Skip hedging phrases and filler.
- Mix sentence lengths. Let some points stand alone.
- End when you're done. No "in conclusion" wrappers.
