# Goals

This document defines the principles and goals guiding aitells development. It captures what the tool does and why.

## Principles

### Findings, not severity levels

Report what the tool detects without moralizing. A triad isn't wrong. Parallel structure isn't bad. These patterns become tells when they cluster unnaturally. The tool surfaces findings; writers decide what matters.

### Fast feedback loops

Analysis runs in seconds, not minutes. Writers check their prose mid-draft. The NLP layer handles most patterns locally. LLM analysis runs only when needed.

### Graceful degradation

No API key? Run NLP-only mode. Slow network? Cache aggressively. Missing configuration? Use sensible defaults. The tool stays useful across environments.

### Complement, don't replace

Vale catches vocabulary fingerprints and pattern-matchable text. aitells catches what Vale can't: structural tells that need parse trees, semantic tells that need language models. The tools work together.

### Machine-readable output

Every output format serves a consumer. Humans read the default format. CI parses exit codes. Editors parse file:line:col. Hooks consume JSON. No format serves many masters poorly.

## Goals

<!-- vale off -->

### Detection categories

aitells targets five categories of AI writing patterns:

1. **Vocabulary fingerprints (VF)** - Words and phrases with documented overrepresentation in AI-generated text. "Delve," "tapestry," "multifaceted," formal transitions like "Moreover" and "Furthermore."

2. **Rhetorical markers (RM)** - Phrase patterns indicating specific rhetorical moves. Sycophantic openers, hedging phrases, false balance, conclusion markers, metacommentary.

3. **Formatting tells (FT)** - Punctuation and markdown patterns. Em-dash overuse, emphatic italics on copulas.

4. **Structural tells (ST)** - Patterns visible in syntax trees. Triads, parallel structure overuse, hedge stacking, transition cadence, sentence and paragraph uniformity.

5. **Semantic tells (SE)** - Patterns requiring meaning comprehension. Empty conclusions, artificial balance, context-inappropriate sycophancy, generic examples, diplomatic evasion.

<!-- vale on -->

See [Rules](rules.md) for the full catalog.

### Integration

- **Claude Code hooks** - Check prose as it's written. Give feedback before commit.
- **CI pipelines** - Run in GitHub Actions. Fail builds on detection. Generate SARIF reports for code scanning.
