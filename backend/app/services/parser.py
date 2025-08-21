"""Utilities for parsing EPUB files into structured content."""

from __future__ import annotations

import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Dict, List


def _get_rootfile_path(zf: zipfile.ZipFile) -> str:
    container = ET.fromstring(zf.read("META-INF/container.xml"))
    ns = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
    rootfile = container.find("c:rootfiles/c:rootfile", ns)
    return rootfile.attrib["full-path"]


def _parse_content_opf(content: bytes) -> Dict[str, object]:
    ns = {
        "opf": "http://www.idpf.org/2007/opf",
        "dc": "http://purl.org/dc/elements/1.1/",
    }
    root = ET.fromstring(content)
    title_elem = root.find("opf:metadata/dc:title", ns)
    title = title_elem.text if title_elem is not None else ""

    manifest = {
        item.attrib["id"]: item.attrib["href"]
        for item in root.find("opf:manifest", ns)
    }
    spine_ids = [i.attrib["idref"] for i in root.find("opf:spine", ns)]
    return {"title": title, "manifest": manifest, "spine": spine_ids}


def _parse_chapter(html: bytes) -> Dict[str, object]:
    ns = {"x": "http://www.w3.org/1999/xhtml"}
    root = ET.fromstring(html)

    title_elem = None
    for tag in ["h1", "h2", "h3"]:
        title_elem = root.find(f".//x:{tag}", ns)
        if title_elem is not None:
            break
    title = title_elem.text if title_elem is not None else ""

    content = [{"text": p.text or ""} for p in root.findall(".//x:p", ns)]
    return {"title": title, "content": content}


def parse_epub(epub_file_path: str) -> Dict[str, object]:
    """Parse an EPUB file and return a structured representation."""

    with zipfile.ZipFile(epub_file_path, "r") as zf:
        rootfile_path = _get_rootfile_path(zf)
        content_info = _parse_content_opf(zf.read(rootfile_path))

        base_path = Path(rootfile_path).parent
        chapters: List[Dict[str, object]] = []
        for idref in content_info["spine"]:
            href = content_info["manifest"].get(idref)
            if not href:
                continue
            chapter_path = str(base_path / href)
            chapter_html = zf.read(chapter_path)
            chapters.append(_parse_chapter(chapter_html))

    return {"title": content_info["title"], "chapters": chapters}
