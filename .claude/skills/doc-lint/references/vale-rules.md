---
name: vale-rules
title: Vale prose style rules
description: Load when fixing vale errors or understanding prose style requirements
---

## Overview

This project uses vale with four style packages (Google, write-good, Proselint, and ai-tells).

## Running vale

```bash
just lint-prose              # All files
just lint-prose path/to.md   # Specific file
```

<!-- vale off -->
## AI-tells rules (most common)

These rules detect AI-generated writing patterns. The project's AGENTS.md explicitly bans these.

### OverusedVocabulary (warning)

**Message:** "AI vocabulary: '%s'. Replace with a more specific or common word."

**Flagged words:** delve, tapestry, multifaceted, underscores, showcasing, pivotal, intricate, groundbreaking, transformative, seamless, robust, leverage, fostering, harnessing, streamline, elevate, bolster, spearhead, underpins, reimagine, elucidate, synergy, holistic, paradigm, unparalleled, testament, cornerstone, catalyst, meticulous, nuanced, interplay, myriad, plethora, burgeoning, nascent, ubiquitous, encompasses, embark, endeavor

**Fix:** Replace with simpler, more specific words. Examples:

- "leverage" → "use"
- "robust" → "reliable" or "solid"
- "streamline" → "simplify"
- "holistic" → "complete" or "full"
- "endeavor" → "try" or "work"

### SycophancyMarkers (warning)

**Message:** "AI sycophancy: '%s'. Delete this, it sounds robotic and insincere."

**Flagged phrases:** "Great question", "Excellent question", "I'm glad you asked", "I'm happy to help", "Absolutely", "Certainly", "Of course", "You're absolutely right", "That's a wonderful idea"

**Fix:** Delete entirely. Start with the actual content.

### HedgingPhrases (suggestion)

**Message:** "AI hedge: '%s'. Delete this throat-clearing and state your point directly."

**Flagged phrases:** "It's important to note that", "It's worth noting that", "It should be noted that", "Generally speaking", "That being said", "Having said that", "To some extent", "In many ways"

**Fix:** Delete the phrase and start with your point.

### FillerPhrases (suggestion)

**Message:** "AI filler: '%s'. Delete this phrase, it adds no meaning."

**Flagged phrases:** "a wide range of", "a variety of", "in order to", "for the purpose of", "has the potential to", "is capable of", "due to the fact that", "it is clear that"

**Fix:** Simplify:

- "in order to" → "to"
- "a variety of" → delete or use specific count
- "due to the fact that" → "because"
- "is capable of" → "can"

### OpeningCliches (warning)

Flags generic openings like "In today's rapidly evolving…"

**Fix:** Start with your actual point.

### EmDashUsage (suggestion)

Flags em-dashes. AGENTS.md says: "Use commas or periods instead of em-dashes."

**Fix:** Replace em-dash with comma, period, or restructure sentence.

## Google style rules

### Google.Passive (warning)

Flags passive voice constructions.

**Fix:** Rewrite in active voice.

- "The file is read by the loader" → "The loader reads the file"

### Google.FirstPerson (warning)

Flags "I", "we", "our" in technical docs.

**Note:** Disabled for README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md

**Fix:** Rewrite to remove first person or add file to exception list in .vale.ini

### Google.Headings (warning)

Flags title case in headings. AGENTS.md says: "Use sentence case for headlines."

**Fix:** Change to sentence case (only capitalize first word and proper nouns).

- "Getting Started With Configuration" → "Getting started with configuration"

### Google.WordList (warning)

Flags deprecated or incorrect terminology.

**Fix:** Use the suggested replacement.

### Google.Will (warning)

Flags future tense "will".

**Note:** Disabled for community docs.

**Fix:** Use present tense.

- "This will load the config" → "This loads the config"

## Write-good rules

### write-good.Passive (suggestion)

Additional passive voice detection.

### write-good.Weasel (warning)

Flags weasel words: "very", "extremely", "remarkably", etc.

**Fix:** Delete or use specific language.

- "very fast" → "fast" or give actual numbers

### write-good.TooWordy (suggestion)

Flags wordy phrases.

**Fix:** Use simpler alternatives.

### write-good.Cliches (warning)

Flags clichéd phrases.

**Fix:** Rewrite with fresh language.

## Proselint rules

### proselint.Hedging (warning)

Flags hedging language: "I think," "perhaps," "maybe"

**Fix:** State directly or delete.

### proselint.Very (warning)

Flags "very" + adjective combinations.

**Fix:** Use a stronger single word.

- "very good" → "excellent"
- "very bad" → "poor"

### proselint.Cliches (warning)

Additional cliché detection.
<!-- vale on -->

## Handling false positives

If vale flags a legitimate technical term:

1. Check if it's truly necessary (often you can rewrite)
2. If the term is correct, add to vocabulary: `.vale/config/vocabularies/cascade/accept.txt`

See [vocabulary reference](vocabulary.md) for details.

## Project writing style (from AGENTS.md)

Beyond what vale catches, follow these guidelines:

<!-- vale off -->
- Mix sentence lengths: follow long explanations with short punchy statements
- Vary paragraph lengths
- Don't start consecutive paragraphs with the same word
- Skip "In conclusion" wrappers
- Be willing to be direct, even blunt
<!-- vale on -->
