"""Conversion logic for generating Cinematic Markup from parsed content."""

from __future__ import annotations

from typing import Dict, List


def generate_cinematic_markup(parsed_book: Dict[str, object]) -> Dict[str, object]:
    """Convert parsed book data into Cinematic Markup JSON structure.

    The transformation implemented here is intentionally simple: each content
    item from the parsed book becomes an entry in the ``content`` list with the
    ``paragraph`` type and an empty ``effects`` list. This provides a predictable
    structure for clients while leaving room for future enhancement logic.

    Args:
        parsed_book: Output from the parser containing structured book data.

    Returns:
        A dictionary following the Cinematic Markup schema as outlined in the
        project ``README``.
    """

    chapters_markup: List[Dict[str, object]] = []

    for chapter in parsed_book.get("chapters", []):
        content: List[Dict[str, object]] = []
        for item in chapter.get("content", []):
            text = item.get("text", "")
            content.append({"type": "paragraph", "text": text, "effects": []})

        chapters_markup.append(
            {
                "chapterTitle": chapter.get("title"),
                "content": content,
            }
        )

    return {
        "bookTitle": parsed_book.get("title"),
        "theme": parsed_book.get("theme", "default"),
        "chapters": chapters_markup,
    }
