<!-- vale off -->

# Settings

This document describes the configuration options for aitells.

Configuration can live in `aitells.toml` at the project root, or in `pyproject.toml` under the `[tool.aitells]` table.

## Top-level

### `select`

A list of rule codes or prefixes to enable.

**Type**: `list[str]`

**Default**: `["VF", "RM", "FT", "ST"]` (all rules except semantic)

**Example**:

=== "aitells.toml"

    ```toml
    select = ["VF", "ST001", "ST002"]
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells]
    select = ["VF", "ST001", "ST002"]
    ```

---

### `ignore`

A list of rule codes or prefixes to disable.

**Type**: `list[str]`

**Default**: `[]`

**Example**:

=== "aitells.toml"

    ```toml
    ignore = ["VF003", "FT001"]
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells]
    ignore = ["VF003", "FT001"]
    ```

---

### `extend-select`

A list of rule codes or prefixes to enable, in addition to those specified by `select`.

**Type**: `list[str]`

**Default**: `[]`

**Example**:

=== "aitells.toml"

    ```toml
    extend-select = ["SE001", "SE002"]
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells]
    extend-select = ["SE001", "SE002"]
    ```

---

### `extend-ignore`

A list of rule codes or prefixes to disable, in addition to those specified by `ignore`.

**Type**: `list[str]`

**Default**: `[]`

**Example**:

=== "aitells.toml"

    ```toml
    extend-ignore = ["RM002"]
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells]
    extend-ignore = ["RM002"]
    ```

---

## Paths

### `include`

A list of file patterns to include.

**Type**: `list[str]`

**Default**: `["*.md", "*.txt", "*.rst"]`

**Example**:

=== "aitells.toml"

    ```toml
    [paths]
    include = ["*.md", "docs/**/*.rst"]
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells.paths]
    include = ["*.md", "docs/**/*.rst"]
    ```

---

### `exclude`

A list of file patterns to exclude.

**Type**: `list[str]`

**Default**: `[]`

**Example**:

=== "aitells.toml"

    ```toml
    [paths]
    exclude = ["vendor/", "node_modules/", "*.min.md"]
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells.paths]
    exclude = ["vendor/", "node_modules/"]
    ```

---

### `extend-exclude`

A list of file patterns to exclude, in addition to those specified by `exclude`.

**Type**: `list[str]`

**Default**: `[]`

**Example**:

=== "aitells.toml"

    ```toml
    [paths]
    extend-exclude = ["CHANGELOG.md"]
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells.paths]
    extend-exclude = ["CHANGELOG.md"]
    ```

---

## Output

### `format`

Output format for findings.

**Type**: `"text" | "json" | "sarif" | "markdown" | "github"`

**Default**: `"text"`

**Example**:

=== "aitells.toml"

    ```toml
    [output]
    format = "json"
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells.output]
    format = "json"
    ```

---

### `quiet`

Suppress non-error output.

**Type**: `bool`

**Default**: `false`

**Example**:

=== "aitells.toml"

    ```toml
    [output]
    quiet = true
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells.output]
    quiet = true
    ```

---

## Rules

Rule-specific configuration. Each rule can be configured under its kebab-case name.

### `rules.<rule>.enabled`

Enable or disable a specific rule.

**Type**: `bool`

**Default**: Depends on rule category (see `select` default)

**Example**:

=== "aitells.toml"

    ```toml
    [rules.triads]
    enabled = false
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells.rules.triads]
    enabled = false
    ```

---

### `rules.<rule>.threshold`

For density-based rules, the threshold at which to trigger.

**Type**: `int`

**Default**: Rule-dependent

**Example**:

=== "aitells.toml"

    ```toml
    [rules.hedge-stacking]
    threshold = 3  # Flag when 3+ hedges in proximity
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells.rules.hedge-stacking]
    threshold = 3
    ```

---

### `rules.<rule>.ignore-patterns`

Patterns to ignore for a specific rule.

**Type**: `list[str]`

**Default**: `[]`

**Example**:

=== "aitells.toml"

    ```toml
    [rules.triads]
    ignore-patterns = ["^## ", "^- "]  # Ignore in headings and lists
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells.rules.triads]
    ignore-patterns = ["^## ", "^- "]
    ```

---

## LLM

Configuration for semantic analysis rules (SE*).

### `llm.enabled`

Enable LLM-based semantic analysis.

**Type**: `bool`

**Default**: `false`

**Example**:

=== "aitells.toml"

    ```toml
    [llm]
    enabled = true
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells.llm]
    enabled = true
    ```

---

### `llm.model`

Model to use for semantic analysis.

**Type**: `str`

**Default**: `"claude-3-haiku-20240307"`

**Example**:

=== "aitells.toml"

    ```toml
    [llm]
    model = "claude-sonnet-4-20250514"
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells.llm]
    model = "claude-sonnet-4-20250514"
    ```

---

### `llm.api-key-env`

Environment variable containing the API key. When running inside Claude Code, authentication is automatic.

**Type**: `str`

**Default**: `"ANTHROPIC_API_KEY"`

**Example**:

=== "aitells.toml"

    ```toml
    [llm]
    api-key-env = "AITELLS_API_KEY"
    ```

=== "pyproject.toml"

    ```toml
    [tool.aitells.llm]
    api-key-env = "AITELLS_API_KEY"
    ```
