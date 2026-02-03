---
description: Lint and fix documentation issues (prose style with vale, markdown formatting with markdownlint)
argument-hint: Optional file paths to lint (defaults to all markdown files)
disable-model-invocation: true
references:
  - prose-quality
---

# Documentation linting

Lint and fix documentation issues in markdown files. This skill runs vale (prose style) and markdownlint (markdown formatting), interprets the output, and fixes issues.

## Quick reference

| Tool         | Recipe               | What it checks                               |
| ------------ | -------------------- | -------------------------------------------- |
| Both         | `just lint-docs`     | Run prose and markdown linting together      |
| vale         | `just lint-prose`    | Prose style, AI vocabulary, hedging, clarity |
| markdownlint | `just lint-markdown` | Markdown formatting, structure               |

## Core workflow

### Step 1: Run linters

Run both linters on the target files.

**For specific files:**

```bash
just lint-docs path/to/file.md
```

**For all files:**

```bash
just lint-docs
```

You can also run linters individually with `just lint-prose` or `just lint-markdown`.

### Step 2: Interpret output

Categorize issues by type:

1. **Auto-fixable markdown issues** - Fix directly (heading levels, list formatting, spacing)
2. **Prose style issues** - Require judgment (rewrite sentences, simplify language)
3. **Vocabulary issues** - Decide: add to accept.txt or rewrite
4. **False positives** - Technical terms that need vocabulary entries

### Step 3: Fix issues

<!-- vale Google.Colons = NO -->
**Markdown issues:** Edit files to fix formatting problems. Most are straightforward structural fixes.

**Prose issues:** Rewrite following AGENTS.md writing style:
<!-- vale Google.Colons = YES -->

<!-- vale off -->
- Use sentence case for headlines
- Avoid AI vocabulary (`delve`, `tapestry`, `robust`, `leverage`, `foster`)
- Cut hedging ("It's important to note…") and filler ("in order to")
- Prefer simple words: "use" not "utilize"
- Be direct, even blunt
<!-- vale on -->

<!-- vale Google.Colons = NO -->
**Vocabulary:** Before adding a term to the vocabulary, check if it's a code identifier that should use backticks instead.
<!-- vale Google.Colons = YES --> Identifiers like function names, variable names, type names, and CLI flags belong in inline code formatting, not the vocabulary. Add to `.vale/config/vocabularies/aitells/accept.txt` only for legitimate prose terms (project names, technical concepts, acronyms). One term per line. Supports regular expression patterns like `(?i)term` for case-insensitive matching.

### Step 4: Verify fixes

Re-run linters to confirm all issues resolved:

```bash
just lint-docs path/to/file.md
```

**The target is zero errors AND zero warnings.** Both linters must pass clean.

## Handling difficult warnings

Never declare a warning "acceptable" or dismiss it as a false positive without discussing with the user first. If you believe you cannot resolve a warning:

1. Explain the specific warning and why you think you cannot fix it
2. Propose options (rewrite differently, add vale directive, add to vocabulary, ask user to adjust config)
3. Let the user decide how to proceed

Most warnings have solutions:

- **Prose showing bad examples:** Wrap in `<!-- vale off -->` / `<!-- vale on -->`
- **Rule names with dots:** Use `<!-- vale Google.Spacing = NO -->` for specific rules
- **Technical terms:** Add to vocabulary or wrap in backticks
- **Style conflicts:** Rewrite the sentence differently

Do not assume warnings are inevitable. The linting configuration exists for a reason, and clean output is always the goal.

## References

The prose-quality reference loads automatically with this skill. It covers what Vale cannot detect: sentence rhythm, paragraph shape, register consistency, over-resolution, and connective tissue patterns.

Load these for detailed rule information when needed:

- [vale-rules](references/vale-rules.md) - Prose style rules and fixes
- [markdownlint-rules](references/markdownlint-rules.md) - Markdown formatting rules
- [vocabulary](references/vocabulary.md) - Managing the project vocabulary

## Restrictions

**You cannot edit `.vale.ini`.** The system blocks attempts to change the vale configuration file. If you need changes to vale configuration (adding paths to exclusions, changing alert levels, enabling/disabling styles), ask the user to make those changes.

You can freely edit the vocabulary file at `.vale/config/vocabularies/aitells/accept.txt`.

## Excluded paths

Vale skips these paths (configured in `.vale.ini`):

- `.claude/**/*.md`
- `.oaps/**/*.md`
- `.vale/**/*.md`
- `tmp/**/*.md`
- `PLAN.md`
