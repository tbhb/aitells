# CLI

This document describes the aitells command-line interface.

## Commands

### aitells check

Analyze files for AI writing patterns.

```bash
# Check specific files
aitells check README.md docs/

# Output as JSON
aitells check --format json src/

# Output as markdown
aitells check --format markdown docs/ > report.md

# Run only structural rules (no API calls)
aitells check --select ST docs/

# Run specific rules
aitells check --select ST001,SE001 docs/

# Ignore specific rules
aitells check --ignore ST003 docs/

# Use specific config file
aitells check --config custom.toml docs/
```

Flags:

| Flag       | Description                                                            |
|------------|------------------------------------------------------------------------|
| `--select` | Run only specified rules or prefixes (`ST`, `ST001`)                   |
| `--ignore` | Skip specified rules or prefixes                                       |
| `--format` | Output format: `text` (default), `json`, `sarif`, `markdown`, `github` |
| `--config` | Path to configuration file                                             |
| `--quiet`  | Suppress non-error output                                              |

### aitells hook

Run as a coding assistant hook. Takes the assistant type as a positional argument.
<!-- vale Vale.Spelling = NO -->
Reads context from stdin, checks prose files in the tool output.
<!-- vale Vale.Spelling = YES -->

```bash
# Claude Code hook
echo '{"tool_input": {"file_path": "docs/guide.md"}}' | aitells hook claude

# Codex hook
echo '{"file": "docs/guide.md"}' | aitells hook codex

# Gemini hook
echo '{"path": "docs/guide.md"}' | aitells hook gemini
```

Supported assistants:

| Assistant | Description       |
|-----------|-------------------|
| `claude`  | Claude Code hooks |
| `codex`   | OpenAI Codex CLI  |
| `gemini`  | Google Gemini CLI |

Each assistant has its own input schema and output format tailored to that tool's expectations.

### aitells init

Create a default configuration file.

```bash
# Create aitells.toml in current directory
aitells init

# Create in pyproject.toml format
aitells init --pyproject
```

### aitells rules

List available detection rules.

```bash
# List all rules
aitells rules

# Show details for specific rule
aitells rules triads
```

## Output formats

### Text (default)

Standard linter format for terminal output:

```text
docs/guide.md:42:1: triads - Three triads in 5 paragraphs
docs/guide.md:87:15: hedge-stacking - Four hedges in one sentence
```

### JSON

Machine-readable format for tooling integration:

```json
{
  "findings": [
    {
      "file": "docs/guide.md",
      "line": 42,
      "column": 1,
      "rule": "triads",
      "message": "Three triads in 5 paragraphs"
    }
  ],
  "summary": {
    "files": 1,
    "findings": 1
  }
}
```

### Markdown

Report format for documentation:

```markdown
## AI writing analysis

### docs/guide.md

- **Line 42**: triads - Three triads in 5 paragraphs
- **Line 87**: hedge-stacking - Four hedges in one sentence
```

### SARIF

[Static Analysis Results Interchange Format][sarif-spec] for GitHub Code Scanning and other tools:

```json
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "aitells",
          "rules": [
            {
              "id": "ST001",
              "name": "triads",
              "shortDescription": { "text": "Rule-of-three abuse" }
            }
          ]
        }
      },
      "results": [
        {
          "ruleId": "ST001",
          "message": { "text": "Three triads in 5 paragraphs" },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": { "uri": "docs/guide.md" },
                "region": { "startLine": 42, "startColumn": 1 }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

[sarif-spec]: https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html

### Actions format

[Workflow command format][gh-workflow-commands] for GitHub Actions annotations:

```text
::warning file=docs/guide.md,line=42,col=1,title=triads::Three triads in 5 paragraphs
```

[gh-workflow-commands]: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions

## Hook integration

Claude Code hooks call aitells when files change.

Hook configuration in `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": {
          "tool_name": "Write|Edit",
          "file_paths": ["*.md", "*.txt", "*.rst"]
        },
        "command": "aitells hook claude"
      }
    ]
  }
}
```

<!-- vale Vale.Spelling = NO -->
The hook reads tool context from stdin:
<!-- vale Vale.Spelling = YES -->

```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "docs/guide.md",
    "content": "..."
  }
}
```

It extracts the path, checks if it's a prose file, and runs analysis. Output returns to Claude Code for display.
