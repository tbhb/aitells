#!/usr/bin/env python3
# pyright: basic
"""Fetch human writing samples from multiple public domain sources.

Sources:
- Standard Ebooks: beautifully formatted public domain texts
- Government: technical/explanatory writing from US agencies
- Project Gutenberg: plain text downloads of classic literature
- Wikibooks: educational/instructional textbook prose

Usage:
    uv run --group notebooks python scripts/fetch_samples.py
    uv run --group notebooks python scripts/fetch_samples.py --force
    uv run --group notebooks python scripts/fetch_samples.py --source standard-ebooks
    uv run --group notebooks python scripts/fetch_samples.py --source government
    uv run --group notebooks python scripts/fetch_samples.py --source gutenberg
    uv run --group notebooks python scripts/fetch_samples.py --source wikibooks
"""

import argparse
import re
import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

import httpx
from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from bs4.element import Tag


class GovernmentSource(TypedDict):
    """Configuration for a government source."""

    url: str
    selector: str
    output: str
    title: str
    source: str


class GutenbergSource(TypedDict):
    """Configuration for a Gutenberg source."""

    id: int
    title: str
    author: str
    output: str


class WikibooksSource(TypedDict):
    """Configuration for a Wikibooks source."""

    url: str
    output: str
    title: str
    source: str

# Curated list of nonfiction books: (author_slug, title_slug, output_filename)
STANDARD_EBOOKS = [
    # Essays
    ("g-k-chesterton", "heretics", "essay_chesterton.txt"),
    ("henry-david-thoreau", "essays", "essay_thoreau.txt"),
    ("william-hazlitt", "table-talk", "essay_hazlitt.txt"),
    # Nature writing
    ("mary-austin", "the-land-of-little-rain", "nature_austin.txt"),
    ("john-muir", "my-first-summer-in-the-sierra", "nature_muir.txt"),
    # Scientific/analytical prose
    ("charles-darwin", "the-voyage-of-the-beagle", "science_darwin.txt"),
    ("charles-darwin", "the-origin-of-species", "science_darwin_origin.txt"),
]

GOVERNMENT_SOURCES: list[GovernmentSource] = [
    {
        "url": "https://www.nps.gov/subjects/geology/plate-tectonics.htm",
        "selector": ".ArticleTextGroup p",
        "output": "technical_nps_geology.txt",
        "title": "Plate Tectonics",
        "source": "National Park Service",
    },
    {
        "url": "https://www.fs.usda.gov/visit/know-before-you-go/bears",
        "selector": "article p",
        "output": "technical_usfs_bears.txt",
        "title": "Bears",
        "source": "USDA Forest Service",
    },
    {
        "url": "https://www.fs.usda.gov/visit/know-before-you-go/hiking",
        "selector": "article p",
        "output": "technical_usfs_hiking.txt",
        "title": "Hiking Safety",
        "source": "USDA Forest Service",
    },
]

GUTENBERG_SOURCES: list[GutenbergSource] = [
    # Fiction / literary prose
    {
        "id": 211,
        "title": "The Aspern Papers",
        "author": "Henry James",
        "output": "fiction_james.txt",
    },
    # Autobiography / memoir
    {
        "id": 148,
        "title": "The Autobiography of Benjamin Franklin",
        "author": "Benjamin Franklin",
        "output": "memoir_franklin.txt",
    },
    # Philosophy / essays
    {
        "id": 5827,
        "title": "The Problems of Philosophy",
        "author": "Bertrand Russell",
        "output": "philosophy_russell.txt",
    },
    # Travel writing
    {
        "id": 119,
        "title": "A Tramp Abroad",
        "author": "Mark Twain",
        "output": "travel_twain.txt",
    },
    # History / narrative nonfiction
    {
        "id": 2044,
        "title": "The Education of Henry Adams",
        "author": "Henry Adams",
        "output": "memoir_adams.txt",
    },
]

WIKIBOOKS_SOURCES: list[WikibooksSource] = [
    # Cooking / how-to
    {
        "url": "https://en.wikibooks.org/wiki/Cookbook:Bread",
        "output": "howto_wikibooks_bread.txt",
        "title": "Bread",
        "source": "Wikibooks Cookbook",
    },
    # Science education
    {
        "url": "https://en.wikibooks.org/wiki/General_Chemistry/Properties_of_Matter/Basic_Properties_of_Matter",
        "output": "textbook_wikibooks_chemistry.txt",
        "title": "Basic Properties of Matter",
        "source": "Wikibooks General Chemistry",
    },
    # Technical / programming
    {
        "url": "https://en.wikibooks.org/wiki/Python_Programming/Overview",
        "output": "technical_wikibooks_python.txt",
        "title": "Python Overview",
        "source": "Wikibooks Python Programming",
    },
    # Biology / life sciences
    {
        "url": "https://en.wikibooks.org/wiki/Human_Physiology/The_Nervous_System",
        "output": "textbook_wikibooks_nervous.txt",
        "title": "The Nervous System",
        "source": "Wikibooks Human Physiology",
    },
    # Practical skills
    {
        "url": "https://en.wikibooks.org/wiki/First_Aid/Introduction",
        "output": "howto_wikibooks_firstaid.txt",
        "title": "First Aid Introduction",
        "source": "Wikibooks First Aid",
    },
]

OUTPUT_DIR = Path(__file__).parent.parent / "notebooks" / "samples" / "human_written"
STANDARD_EBOOKS_URL = "https://standardebooks.org/ebooks/{author}/{title}/text/single-page"
GUTENBERG_URL = "https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
GUTENBERG_EBOOK_URL = "https://www.gutenberg.org/ebooks/{book_id}"

# Target word count range for excerpts
MIN_WORDS = 150
MAX_WORDS = 400
MIN_PARAGRAPHS = 2
MAX_PARAGRAPHS = 5

# Minimum words for a paragraph to be considered content (not navigation/headers)
MIN_PARAGRAPH_WORDS = 20


# User-Agent for requests (some sites block requests without one)
USER_AGENT = "aitells-sample-fetcher/1.0 (https://github.com/tbhb/aitells; educational use)"


def fetch_page(url: str, *, timeout: float = 30.0) -> str | None:
    """Fetch a page and return its HTML content."""
    try:
        headers = {"User-Agent": USER_AGENT}
        response = httpx.get(url, headers=headers, follow_redirects=True, timeout=timeout)
        response.raise_for_status()
        return response.text
    except httpx.HTTPError as e:
        print(f"  Warning: Failed to fetch {url}: {e}", file=sys.stderr)
        return None


# IDs to skip when looking for content sections
SKIP_IDS = {
    "titlepage",
    "toc",
    "imprint",
    "preface",
    "halftitlepage",
    "endnotes",
    "colophon",
    "uncopyright",
}


def extract_sections(soup: BeautifulSoup) -> list[tuple[str, list[str]]]:
    """Extract content sections with their paragraph texts.

    Handles both chapter-based books and essay collections.
    Returns list of (section_id, [paragraph_texts]).
    """
    sections: list[tuple[str, list[str]]] = []

    # First try chapter-* elements (for novels)
    chapter_elements = soup.find_all(id=re.compile(r"^chapter-"))

    if chapter_elements:
        for chapter_el in chapter_elements:
            chapter_id = str(chapter_el.get("id", "unknown"))
            paragraphs = _extract_paragraphs(chapter_el)
            if paragraphs:
                sections.append((chapter_id, paragraphs))
        return sections

    # For essay collections, find article/section elements with prose content
    # Look for sections that have an id and contain multiple <p> tags
    for el in soup.find_all(["article", "section"]):
        section_id_attr = el.get("id")
        if not section_id_attr:
            continue
        section_id = str(section_id_attr)
        if section_id in SKIP_IDS:
            continue
        # Skip subsections (e.g., "essay-name-1", "essay-name-2")
        if re.match(r".*-\d+$", section_id):
            continue
        # Skip volume markers
        if section_id.startswith("volume-"):
            continue

        paragraphs = _extract_paragraphs(el)
        if len(paragraphs) >= 3:  # Only include sections with enough prose
            sections.append((section_id, paragraphs))

    return sections


def _extract_paragraphs(element: "Tag") -> list[str]:
    """Extract paragraph text from an element."""
    paragraphs: list[str] = []
    for p in element.find_all("p"):
        text = p.get_text(strip=True)
        if text:
            paragraphs.append(text)
    return paragraphs


def normalize_text(text: str) -> str:
    """Normalize whitespace in text."""
    # Collapse multiple spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)
    # Normalize line breaks
    text = re.sub(r"\n\s*\n", "\n\n", text)
    return text.strip()


def find_suitable_excerpt(
    sections: list[tuple[str, list[str]]]
) -> tuple[str, list[str]] | None:
    """Find a suitable excerpt from middle sections.

    Returns (section_id, [selected_paragraphs]) or None.
    """
    if len(sections) < 3:
        # Not enough sections to skip first and last
        return None

    # Skip first and last sections
    middle_sections = sections[1:-1]

    for section_id, paragraphs in middle_sections:
        # Try to find a suitable consecutive sequence
        for start_idx in range(len(paragraphs)):
            for num_paras in range(MAX_PARAGRAPHS, MIN_PARAGRAPHS - 1, -1):
                end_idx = start_idx + num_paras
                if end_idx > len(paragraphs):
                    continue

                selected = paragraphs[start_idx:end_idx]
                word_count = sum(len(p.split()) for p in selected)

                if MIN_WORDS <= word_count <= MAX_WORDS:
                    return (section_id, selected)

    return None


def find_suitable_excerpt_from_paragraphs(
    paragraphs: list[str],
) -> list[str] | None:
    """Find a suitable excerpt from a flat list of paragraphs.

    Returns [selected_paragraphs] or None.
    """
    for start_idx in range(len(paragraphs)):
        for num_paras in range(MAX_PARAGRAPHS, MIN_PARAGRAPHS - 1, -1):
            end_idx = start_idx + num_paras
            if end_idx > len(paragraphs):
                continue

            selected = paragraphs[start_idx:end_idx]
            word_count = sum(len(p.split()) for p in selected)

            if MIN_WORDS <= word_count <= MAX_WORDS:
                return selected

    return None


def format_title(slug: str) -> str:
    """Convert a URL slug to a readable title."""
    return slug.replace("-", " ").title()


def create_standard_ebooks_output(
    author_slug: str,
    title_slug: str,
    section_id: str,
    paragraphs: list[str],
) -> str:
    """Create the formatted output text with header for Standard Ebooks."""
    url = STANDARD_EBOOKS_URL.format(author=author_slug, title=title_slug)
    author = format_title(author_slug)
    title = format_title(title_slug)
    section_name = format_title(section_id)

    header = f"""# Source: Standard Ebooks - {title} by {author}
# Section: {section_name}
# URL: {url}
# License: Public Domain (CC0)

"""
    body = "\n\n".join(paragraphs)
    return header + body + "\n"


def create_government_output(
    source: str,
    title: str,
    url: str,
    paragraphs: list[str],
) -> str:
    """Create the formatted output text with header for government sources."""
    header = f"""# Source: {source} - {title}
# URL: {url}
# License: Public Domain (US Government Work)

"""
    body = "\n\n".join(paragraphs)
    return header + body + "\n"


def process_standard_ebook(
    author_slug: str,
    title_slug: str,
    output_filename: str,
    *,
    force: bool = False,
) -> bool:
    """Fetch and extract a sample from a single Standard Ebook.

    Returns True if successful.
    """
    output_path = OUTPUT_DIR / output_filename

    if output_path.exists() and not force:
        print(f"  Skipping {output_filename} (already exists, use --force to overwrite)")
        return True

    url = STANDARD_EBOOKS_URL.format(author=author_slug, title=title_slug)
    print(f"  Fetching {format_title(title_slug)}...")

    html = fetch_page(url)
    if html is None:
        return False

    soup = BeautifulSoup(html, "html.parser")
    sections = extract_sections(soup)

    if not sections:
        print(f"  Warning: No sections found in {title_slug}", file=sys.stderr)
        return False

    result = find_suitable_excerpt(sections)
    if result is None:
        print(
            f"  Warning: Could not find suitable excerpt in {title_slug}",
            file=sys.stderr,
        )
        return False

    section_id, paragraphs = result
    output_text = create_standard_ebooks_output(
        author_slug, title_slug, section_id, paragraphs
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output_text, encoding="utf-8")
    word_count = sum(len(p.split()) for p in paragraphs)
    print(f"  Saved {output_filename} ({len(paragraphs)} paragraphs, {word_count} words)")

    return True


def process_government_source(
    source_config: GovernmentSource,
    *,
    force: bool = False,
) -> bool:
    """Fetch and extract a sample from a government source.

    Returns True if successful.
    """
    output_filename = source_config["output"]
    output_path = OUTPUT_DIR / output_filename

    if output_path.exists() and not force:
        print(f"  Skipping {output_filename} (already exists, use --force to overwrite)")
        return True

    url = source_config["url"]
    title = source_config["title"]
    source = source_config["source"]
    selector = source_config["selector"]

    print(f"  Fetching {title} from {source}...")

    # Government sites can be slow
    html = fetch_page(url, timeout=10.0)
    if html is None:
        return False

    soup = BeautifulSoup(html, "html.parser")

    # Use CSS selector to find content paragraphs
    elements = soup.select(selector)

    if not elements:
        print(
            f"  Warning: No paragraphs found with selector '{selector}' at {url}",
            file=sys.stderr,
        )
        return False

    # Extract and filter paragraphs
    paragraphs = []
    for el in elements:
        text = normalize_text(el.get_text())
        word_count = len(text.split())
        # Filter out short paragraphs (navigation, headers, etc.)
        if word_count >= MIN_PARAGRAPH_WORDS:
            paragraphs.append(text)

    if len(paragraphs) < MIN_PARAGRAPHS:
        print(
            f"  Warning: Not enough content paragraphs found at {url} (found {len(paragraphs)}, need {MIN_PARAGRAPHS})",
            file=sys.stderr,
        )
        return False

    # Find suitable excerpt
    selected = find_suitable_excerpt_from_paragraphs(paragraphs)
    if selected is None:
        print(
            f"  Warning: Could not find suitable excerpt from {url}",
            file=sys.stderr,
        )
        return False

    output_text = create_government_output(source, title, url, selected)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output_text, encoding="utf-8")
    word_count = sum(len(p.split()) for p in selected)
    print(f"  Saved {output_filename} ({len(selected)} paragraphs, {word_count} words)")

    return True


def fetch_standard_ebooks(*, force: bool = False) -> tuple[int, int]:
    """Fetch all Standard Ebooks sources.

    Returns (success_count, total_count).
    """
    print("Fetching from Standard Ebooks...")
    print()

    success_count = 0
    for i, (author, title, filename) in enumerate(STANDARD_EBOOKS):
        if i > 0:
            time.sleep(1)

        if process_standard_ebook(author, title, filename, force=force):
            success_count += 1

    return success_count, len(STANDARD_EBOOKS)


def fetch_government_sources(*, force: bool = False) -> tuple[int, int]:
    """Fetch all government sources.

    Returns (success_count, total_count).
    """
    print("Fetching from government sources...")
    print()

    success_count = 0
    for i, source_config in enumerate(GOVERNMENT_SOURCES):
        if i > 0:
            time.sleep(1)

        if process_government_source(source_config, force=force):
            success_count += 1

    return success_count, len(GOVERNMENT_SOURCES)


# Regex patterns for Gutenberg start/end markers
GUTENBERG_START_PATTERN = re.compile(
    r"\*\*\* ?START OF (?:THE |THIS )?PROJECT GUTENBERG", re.IGNORECASE
)
GUTENBERG_END_PATTERN = re.compile(
    r"\*\*\* ?END OF (?:THE |THIS )?PROJECT GUTENBERG", re.IGNORECASE
)

def fetch_gutenberg_text(url: str) -> str | None:
    """Fetch a Gutenberg text file, handling encoding issues."""
    try:
        headers = {"User-Agent": USER_AGENT}
        response = httpx.get(url, headers=headers, follow_redirects=True, timeout=30.0)
        response.raise_for_status()

        # Try UTF-8 first, fall back to Latin-1
        try:
            return response.content.decode("utf-8")
        except UnicodeDecodeError:
            return response.content.decode("latin-1")
    except httpx.HTTPError as e:
        print(f"  Warning: Failed to fetch {url}: {e}", file=sys.stderr)
        return None


def extract_gutenberg_content(text: str) -> str | None:
    """Extract the main content from a Gutenberg text, stripping header/footer."""
    # Normalize line endings (Gutenberg uses CRLF)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Find start marker
    start_match = GUTENBERG_START_PATTERN.search(text)
    if not start_match:
        return None

    # Find end marker
    end_match = GUTENBERG_END_PATTERN.search(text)
    if not end_match:
        return None

    # Extract content between markers
    # Skip to end of the start marker line
    start_pos = text.find("\n", start_match.end())
    if start_pos == -1:
        start_pos = start_match.end()

    content = text[start_pos : end_match.start()]

    # Normalize paragraph breaks (collapse 3+ newlines to 2)
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content.strip()


def extract_gutenberg_paragraphs(content: str) -> list[str]:
    """Split Gutenberg content into paragraphs and filter by word count."""
    # Split on double newlines
    raw_paragraphs = content.split("\n\n")

    paragraphs = []
    for para in raw_paragraphs:
        # Normalize whitespace within paragraph
        text = " ".join(para.split())
        if not text:
            continue

        word_count = len(text.split())
        # Filter out very short paragraphs (headers, page numbers, etc.)
        # but keep longer ones for excerpt selection
        if word_count >= MIN_PARAGRAPH_WORDS:
            paragraphs.append(text)

    return paragraphs


def find_gutenberg_excerpt(paragraphs: list[str]) -> list[str] | None:
    """Find a suitable excerpt from the middle of a Gutenberg text.

    Skips the first and last 10% of paragraphs to avoid front/back matter.
    """
    if len(paragraphs) < 5:
        return None

    # Skip first and last 10%
    skip_count = max(1, len(paragraphs) // 10)
    middle_paragraphs = paragraphs[skip_count:-skip_count]

    if len(middle_paragraphs) < MIN_PARAGRAPHS:
        return None

    # Find suitable excerpt from middle paragraphs
    return find_suitable_excerpt_from_paragraphs(middle_paragraphs)


def create_gutenberg_output(
    title: str,
    author: str,
    book_id: int,
    paragraphs: list[str],
) -> str:
    """Create the formatted output text with header for Gutenberg sources."""
    url = GUTENBERG_EBOOK_URL.format(book_id=book_id)

    header = f"""# Source: Project Gutenberg - {title} by {author}
# URL: {url}
# License: Public Domain

"""
    body = "\n\n".join(paragraphs)
    return header + body + "\n"


def process_gutenberg_source(
    source_config: GutenbergSource,
    *,
    force: bool = False,
) -> bool:
    """Fetch and extract a sample from a Gutenberg source.

    Returns True if successful.
    """
    output_filename = source_config["output"]
    output_path = OUTPUT_DIR / output_filename

    if output_path.exists() and not force:
        print(f"  Skipping {output_filename} (already exists, use --force to overwrite)")
        return True

    book_id = source_config["id"]
    title = source_config["title"]
    author = source_config["author"]

    print(f"  Fetching {title} by {author}...")

    url = GUTENBERG_URL.format(book_id=book_id)
    text = fetch_gutenberg_text(url)
    if text is None:
        return False

    # Extract content between start/end markers
    content = extract_gutenberg_content(text)
    if content is None:
        print(
            f"  Warning: Could not find Gutenberg markers in {title}",
            file=sys.stderr,
        )
        return False

    # Extract and filter paragraphs
    paragraphs = extract_gutenberg_paragraphs(content)
    if len(paragraphs) < MIN_PARAGRAPHS:
        print(
            f"  Warning: Not enough suitable paragraphs in {title} (found {len(paragraphs)}, need {MIN_PARAGRAPHS})",
            file=sys.stderr,
        )
        return False

    # Find suitable excerpt from middle of text
    selected = find_gutenberg_excerpt(paragraphs)
    if selected is None:
        print(
            f"  Warning: Could not find suitable excerpt in {title}",
            file=sys.stderr,
        )
        return False

    output_text = create_gutenberg_output(title, author, book_id, selected)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output_text, encoding="utf-8")
    word_count = sum(len(p.split()) for p in selected)
    print(f"  Saved {output_filename} ({len(selected)} paragraphs, {word_count} words)")

    return True


def fetch_gutenberg_sources(*, force: bool = False) -> tuple[int, int]:
    """Fetch all Gutenberg sources.

    Returns (success_count, total_count).
    """
    print("Fetching from Project Gutenberg...")
    print()

    success_count = 0
    for i, source_config in enumerate(GUTENBERG_SOURCES):
        if i > 0:
            time.sleep(1)

        if process_gutenberg_source(source_config, force=force):
            success_count += 1

    return success_count, len(GUTENBERG_SOURCES)


# Classes to skip when extracting Wikibooks content
WIKIBOOKS_SKIP_CLASSES = {
    "toc",
    "navbox",
    "mw-editsection",
    "hatnote",
    "thumb",
    "mw-empty-elt",
    "noprint",
    "sistersitebox",
    "metadata",
    "ambox",
    "mbox-small",
}

# Pattern to match wiki artifacts like [edit], [1], etc.
WIKI_ARTIFACT_PATTERN = re.compile(r"\[\s*(?:edit|citation needed|\d+)\s*\]", re.IGNORECASE)


def clean_wikibooks_text(text: str) -> str:
    """Clean wiki markup artifacts from text."""
    # Remove [edit], [1], [citation needed], etc.
    text = WIKI_ARTIFACT_PATTERN.sub("", text)
    # Normalize whitespace
    text = " ".join(text.split())
    return text.strip()


def extract_wikibooks_paragraphs(soup: BeautifulSoup) -> list[str]:
    """Extract prose paragraphs from Wikibooks content."""
    # Find the main content area
    content = soup.select_one("#mw-content-text .mw-parser-output")
    if not content:
        return []

    paragraphs = []

    # Get all <p> tags within content area
    for p in content.find_all("p"):
        # Skip if inside a class we want to exclude
        skip = False
        for parent in p.parents:
            parent_classes = parent.get("class") or []
            if parent_classes:
                if set(parent_classes) & WIKIBOOKS_SKIP_CLASSES:
                    skip = True
                    break
        if skip:
            continue

        # Get text and clean it
        text = clean_wikibooks_text(p.get_text())
        if not text:
            continue

        word_count = len(text.split())
        # Filter out short paragraphs (navigation, captions, etc.)
        if word_count >= MIN_PARAGRAPH_WORDS:
            paragraphs.append(text)

    return paragraphs


def create_wikibooks_output(
    source: str,
    title: str,
    url: str,
    paragraphs: list[str],
) -> str:
    """Create the formatted output text with header for Wikibooks sources."""
    header = f"""# Source: {source} - {title}
# URL: {url}
# License: CC BY-SA 3.0

"""
    body = "\n\n".join(paragraphs)
    return header + body + "\n"


def process_wikibooks_source(
    source_config: WikibooksSource,
    *,
    force: bool = False,
) -> bool:
    """Fetch and extract a sample from a Wikibooks source.

    Returns True if successful.
    """
    output_filename = source_config["output"]
    output_path = OUTPUT_DIR / output_filename

    if output_path.exists() and not force:
        print(f"  Skipping {output_filename} (already exists, use --force to overwrite)")
        return True

    url = source_config["url"]
    title = source_config["title"]
    source = source_config["source"]

    print(f"  Fetching {title} from {source}...")

    html = fetch_page(url)
    if html is None:
        return False

    soup = BeautifulSoup(html, "html.parser")

    # Extract paragraphs
    paragraphs = extract_wikibooks_paragraphs(soup)

    # Check if page is a stub (< 100 words total)
    total_words = sum(len(p.split()) for p in paragraphs)
    if total_words < 100:
        print(
            f"  Warning: Page appears to be a stub ({total_words} words) at {url}",
            file=sys.stderr,
        )
        return False

    if len(paragraphs) < MIN_PARAGRAPHS:
        print(
            f"  Warning: Not enough prose paragraphs found at {url} (found {len(paragraphs)}, need {MIN_PARAGRAPHS})",
            file=sys.stderr,
        )
        return False

    # Find suitable excerpt
    selected = find_suitable_excerpt_from_paragraphs(paragraphs)
    if selected is None:
        print(
            f"  Warning: Could not find suitable excerpt from {url}",
            file=sys.stderr,
        )
        return False

    output_text = create_wikibooks_output(source, title, url, selected)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output_text, encoding="utf-8")
    word_count = sum(len(p.split()) for p in selected)
    print(f"  Saved {output_filename} ({len(selected)} paragraphs, {word_count} words)")

    return True


def fetch_wikibooks_sources(*, force: bool = False) -> tuple[int, int]:
    """Fetch all Wikibooks sources.

    Returns (success_count, total_count).
    """
    print("Fetching from Wikibooks...")
    print()

    success_count = 0
    for i, source_config in enumerate(WIKIBOOKS_SOURCES):
        if i > 0:
            time.sleep(1)

        if process_wikibooks_source(source_config, force=force):
            success_count += 1

    return success_count, len(WIKIBOOKS_SOURCES)


def main() -> int:
    """Run the sample fetcher."""
    parser = argparse.ArgumentParser(
        description="Fetch human writing samples from multiple public domain sources"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )
    parser.add_argument(
        "--source",
        choices=["standard-ebooks", "government", "gutenberg", "wikibooks", "all"],
        default="all",
        help="Which sources to fetch (default: all)",
    )
    args = parser.parse_args()

    total_success = 0
    total_count = 0

    if args.source in ("standard-ebooks", "all"):
        success, count = fetch_standard_ebooks(force=args.force)
        total_success += success
        total_count += count
        print()

    if args.source in ("government", "all"):
        success, count = fetch_government_sources(force=args.force)
        total_success += success
        total_count += count
        print()

    if args.source in ("gutenberg", "all"):
        success, count = fetch_gutenberg_sources(force=args.force)
        total_success += success
        total_count += count
        print()

    if args.source in ("wikibooks", "all"):
        success, count = fetch_wikibooks_sources(force=args.force)
        total_success += success
        total_count += count
        print()

    print(f"Completed: {total_success}/{total_count} sources processed successfully")

    return 0 if total_success == total_count else 1


if __name__ == "__main__":
    sys.exit(main())
