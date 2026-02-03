# Edge cases

This directory holds texts that challenge detection. These are useful for testing robustness and identifying false positives/negatives.

## Categories to collect

**False positives**: Human writing that triggers AI detection

- Formal academic prose
- Technical documentation with enumerated lists
- Non-native English speakers
- Highly structured business writing

**False negatives**: AI writing that evades detection

- Prompted for casual/conversational tone
- Deliberately avoiding common patterns
- Creative fiction with voice

**Stylized writing**: Neither typical human nor typical AI

- Poetry and experimental prose
- Historical texts with archaic style
- Translated works
- Genre fiction with distinct conventions

## Adding samples

When adding edge cases, include a note (as a comment at the top of the file or in the filename) indicating:

- Source or generation method
- Why it's an edge case
- What behavior you observed
