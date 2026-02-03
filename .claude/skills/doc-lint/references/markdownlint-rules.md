---
name: markdownlint-rules
title: markdownlint formatting rules
description: Load when fixing markdownlint errors or understanding markdown structure requirements
---

## Overview

This project uses markdownlint-cli2 for markdown formatting validation.

## Running markdownlint

```bash
just lint-markdown             # All .md files
just lint-markdown path/to.md  # Specific file
```

## Rules turned off

The project turns off these rules in `.markdownlint-cli2.jsonc`:

| Rule  | Name                 | Why off                                     |
|-------|----------------------|---------------------------------------------|
| MD013 | line-length          | Long lines often needed for tables, links   |
| MD041 | first-line-h1        | Not all files need H1 first                 |
| MD024 | no-duplicate-heading | Same headings allowed in different sections |
| MD033 | no-inline-html       | HTML sometimes needed                       |
| MD051 | link-fragments       | Fragment validation not always accurate     |
| MD004 | list-marker-space    | Flexible list formatting                    |
| MD046 | code-block-style     | Mixed styles allowed                        |

<!-- vale off -->
## Active rules (common issues)

### MD001: Heading increment

Headings must increment by one level at a time.

**Bad:**

```markdown
# Heading 1
### Heading 3
```

**Fix:**

```markdown
# Heading 1
## Heading 2
### Heading 3
```

### MD003: Heading style

Use consistent heading style (ATX style with `#`).

**Bad:**

```markdown
Heading
=======
```

**Fix:**

```markdown
# Heading
```

### MD005: Inconsistent list indentation

List items at same level must have same indentation.

**Bad:**

```markdown
- Item 1
  - Nested
 - Item 2 (wrong indent)
```

**Fix:**

```markdown
- Item 1
  - Nested
- Item 2
```

### MD007: Unordered list indentation

Nested lists should use 2 spaces (project default).

**Bad:**

```markdown
- Item
    - Nested (4 spaces)
```

**Fix:**

```markdown
- Item
  - Nested (2 spaces)
```

### MD009: Trailing spaces

No trailing whitespace on lines.

**Fix:** Remove trailing spaces. Most editors can do this automatically.

### MD010: Hard tabs

Use spaces, not tabs.

**Fix:** Convert tabs to spaces.

### MD011: Reversed link syntax

Links use `[text](url)` not `(text)[url]`.

**Bad:**

```markdown
(Click here)[https://example.com]
```

**Fix:**

```markdown
[Click here](https://example.com)
```

### MD012: Multiple blank lines

No more than one consecutive blank line.

**Fix:** Remove extra blank lines.

### MD018/MD019: Space after hash

Headings need exactly one space after `#`.

**Bad:**

```markdown
#Heading
#  Heading
```

**Fix:**

```markdown
# Heading
```

### MD022: Blank lines around headings

Headings need blank lines before and after.

**Bad:**

```markdown
Some text.
## Heading
More text.
```

**Fix:**

```markdown
Some text.

## Heading

More text.
```

### MD023: Headings must start at line beginning

No indentation before headings.

**Bad:**

```markdown
  ## Heading
```

**Fix:**

```markdown
## Heading
```

### MD025: Single top-level heading

Only one H1 (`#`) per document.

**Fix:** Use H2 or lower for additional sections.

### MD026: No trailing punctuation in headings

Headings should not end with punctuation (except `?`).

**Bad:**

```markdown
## What is this?:
```

**Fix:**

```markdown
## What is this?
```

### MD027: Multiple spaces after blockquote

Blockquotes need exactly one space after `>`.

**Fix:**

```markdown
> Quote text
```

### MD028: Blank line inside blockquote

No blank lines between blockquote lines unless intentional.

### MD030: Spaces after list markers

List markers need exactly one space after.

**Bad:**

```markdown
-Item
-  Item
```

**Fix:**

```markdown
- Item
```

### MD031: Fenced code blocks surrounded by blank lines

Code blocks need blank lines before and after.

### MD032: Lists surrounded by blank lines

Lists need blank lines before and after.

### MD034: Bare URLs

URLs should be in angle brackets or proper links.

**Bad:**

```markdown
See https://example.com for details.
```

**Fix:**

```markdown
See <https://example.com> for details.
See [example](https://example.com) for details.
```

### MD035: Horizontal rule style

Use consistent horizontal rule style (usually `---`).

### MD037: Spaces inside emphasis markers

No spaces inside `*` or `_`.

**Bad:**

```markdown
** bold **
```

**Fix:**

```markdown
**bold**
```

### MD038: Spaces inside code span

No spaces inside backticks.

**Bad:**

```markdown
` code `
```

**Fix:**

```markdown
`code`
```

### MD039: Spaces inside link text

No spaces inside link brackets.

**Bad:**

```markdown
[ link ](url)
```

**Fix:**

```markdown
[link](url)
```

### MD040: Fenced code block language

Specify language for fenced code blocks.

**Bad:**

````markdown
```
code here
```
````

**Fix:**

````markdown
```go
code here
```
````

### MD047: File should end with newline

Files must end with a single newline.

**Fix:** Add newline at end of file.
<!-- vale on -->

## Quick fixes

Most markdownlint issues are mechanical. Common patterns:

1. **Spacing issues** (MD009, MD010, MD012, MD018, MD019, MD027, MD030, MD037, MD038, MD039): adjust whitespace
2. **Blank line issues** (MD022, MD031, MD032): add or remove blank lines around elements
3. **Structure issues** (MD001, MD025): fix heading hierarchy
4. **Syntax issues** (MD003, MD011, MD034, MD040): use correct markdown syntax
