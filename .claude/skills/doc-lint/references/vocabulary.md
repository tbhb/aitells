---
name: vocabulary
title: Managing project vocabulary
description: Load when adding terms to accept.txt or deciding whether to add vs rewrite
---

## Overview

Vale uses a vocabulary file to recognize project-specific terms that would otherwise trigger spelling errors or unknown word warnings.

## Vocabulary file location

```text
.vale/config/vocabularies/aitells/accept.txt
```

## When to add vs when to wrap in backticks vs when to rewrite

Before adding a term to the vocabulary, check if it's a code identifier that needs backticks instead.

**Wrap in backticks (inline code) when:**

<!-- vale off -->
- The term is a function name, method name, or type name (`NewConfig()`, `LoadFromFile`, `ConfigStore`)
- The term is a variable or constant name (`configPath`, `DEFAULT_TIMEOUT`)
- The term is a CLI flag or command (`--verbose`, `kubectl apply`)
- The term is a code symbol referenced in prose (`nil`, `error`, `struct`)
<!-- vale on -->

**Add to vocabulary when:**

<!-- vale off -->
- The term is a project or library name used as prose (koanf, pflag, TOML)
- The term is project-specific jargon that readers encounter (provenance, unmarshal)
- The term is an acronym or abbreviation in common use (CLI, SDK, API)
<!-- vale on -->
- The term is a proper noun (tool name, library name, company)

**Rewrite instead when:**

<!-- vale off -->
- The term is AI vocabulary that you should replace (see ai-tells rules)
<!-- vale on -->
- The term is unnecessarily technical and a simpler word exists
- The term is jargon that readers won't understand
- You're using the term to sound sophisticated rather than communicate

## Adding terms

Add one term per line to `accept.txt`:

```text
myterm
AnotherTerm
```

### Case sensitivity

By default, terms are case-sensitive. For case-insensitive matching, use a regular expression:

```text
(?i)terraform
```

This matches: terraform, Terraform, TERRAFORM, TerraForm

### Common patterns

**Exact match (case-sensitive):**

```text
YAML
JSON
CLI
```

**Case-insensitive:**

```text
(?i)config
(?i)enum
(?i)middleware
```

**Variant forms:**

```text
unmarshal
unmarshaling
unmarshalling
unmarshaler
```

## Current vocabulary categories

The aitells project vocabulary includes:

**Data formats:**
YAML, JSON

**Python ecosystem:**
spaCy, tricolon, hendiatris

**NLP and linguistics:**
rhetorical, anaphora, epistrophe, parallelism

**Project concepts:**
aitells, AI-generated, prose

## Checking your addition

After adding a term, verify it works:

```bash
just lint-prose path/to/file.md
```

Vale should no longer flag the term.

## Reject list

There's also a reject list at:

```text
.vale/config/vocabularies/aitells/reject.txt
```

Vale always flags terms here, even if they'd normally pass. Use this for:

- Common misspellings you want to catch
- Terms that should never appear in docs
- Deprecated terminology

## Best practices

<!-- vale off -->
1. **Be specific:** Add `kubectl` not just `kube`
2. **Include variants:** If adding `unmarshal`, also add `unmarshaling`, `unmarshaller`, etc.
3. **Use case-insensitive for flexible terms:** `(?i)config` catches all case variants
4. **Don't add AI vocabulary:** If vale flags "leverage" or "robust", rewrite instead of adding
5. **Document unusual additions:** Add a comment in a PR if the term isn't obvious
<!-- vale on -->

## Example workflow

1. Run `just lint-prose` and see: `'koanf' does not exist in the dictionary`
2. Check if it's a code identifier:
   - Is it a function/method name? → Wrap in backticks: `` `koanf.New()` ``
   - Is it a variable? → Wrap in backticks
   - Is it a CLI flag? → Wrap in backticks
3. If it's a prose term (library name, concept), confirm it's legitimate
4. Add to `.vale/config/vocabularies/aitells/accept.txt`
5. Re-run `just lint-prose` to verify vale no longer flags the term

### Common mistakes

<!-- vale off -->
**Wrong:** Adding `LoadConfig` to vocabulary
**Right:** Writing `` `LoadConfig` `` in the markdown

**Wrong:** Adding `--config` to vocabulary
**Right:** Writing `` `--config` `` in the markdown
<!-- vale on -->

<!-- vale Google.Colons = NO -->
**Correct vocabulary addition:** Adding `spaCy` because it's a library name used in prose like "aitells uses spaCy for dependency parsing"
<!-- vale Google.Colons = YES -->
