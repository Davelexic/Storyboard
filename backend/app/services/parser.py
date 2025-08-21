"""Utilities for parsing EPUB files into structured content."""

from __future__ import annotations

import xml.etree.ElementTree as ET
import zipfile
import re
from pathlib import Path
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


def _get_rootfile_path(zf: zipfile.ZipFile) -> str:
    """Extract the root file path from container.xml."""
    try:
        container = ET.fromstring(zf.read("META-INF/container.xml"))
        ns = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
        rootfile = container.find("c:rootfiles/c:rootfile", ns)
        if rootfile is None:
            raise ValueError("No rootfile found in container.xml")
        return rootfile.attrib["full-path"]
    except Exception as e:
        logger.error(f"Error parsing container.xml: {e}")
        raise


def _parse_content_opf(content: bytes) -> Dict[str, Any]:
    """Parse the content.opf file to extract metadata and manifest."""
    ns = {
        "opf": "http://www.idpf.org/2007/opf",
        "dc": "http://purl.org/dc/elements/1.1/",
    }
    
    try:
        root = ET.fromstring(content)
        
        # Extract metadata
        metadata = {}
        title_elem = root.find("opf:metadata/dc:title", ns)
        metadata["title"] = title_elem.text if title_elem is not None else "Unknown Title"
        
        author_elem = root.find("opf:metadata/dc:creator", ns)
        metadata["author"] = author_elem.text if author_elem is not None else "Unknown Author"
        
        language_elem = root.find("opf:metadata/dc:language", ns)
        metadata["language"] = language_elem.text if language_elem is not None else "en"
        
        identifier_elem = root.find("opf:metadata/dc:identifier", ns)
        metadata["identifier"] = identifier_elem.text if identifier_elem is not None else None
        
        # Extract manifest
        manifest = {}
        manifest_elem = root.find("opf:manifest", ns)
        if manifest_elem is not None:
            for item in manifest_elem.findall("opf:item", ns):
                item_id = item.attrib.get("id")
                item_href = item.attrib.get("href")
                item_type = item.attrib.get("media-type", "")
                if item_id and item_href:
                    manifest[item_id] = {
                        "href": item_href,
                        "type": item_type
                    }
        
        # Extract spine
        spine_ids = []
        spine_elem = root.find("opf:spine", ns)
        if spine_elem is not None:
            for itemref in spine_elem.findall("opf:itemref", ns):
                idref = itemref.attrib.get("idref")
                if idref:
                    spine_ids.append(idref)
        
        return {
            "metadata": metadata,
            "manifest": manifest,
            "spine": spine_ids
        }
        
    except Exception as e:
        logger.error(f"Error parsing content.opf: {e}")
        raise


def _clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    
    return text


def _parse_chapter(html: bytes) -> Dict[str, Any]:
    """Parse a chapter HTML file into structured content."""
    ns = {"x": "http://www.w3.org/1999/xhtml"}
    
    try:
        root = ET.fromstring(html)
        
        # Extract title
        title = ""
        for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            title_elem = root.find(f".//x:{tag}", ns)
            if title_elem is not None and title_elem.text:
                title = _clean_text(title_elem.text)
                break
        
        # Extract content
        content = []
        
        # Find all paragraph and div elements
        for elem in root.findall(".//x:p", ns) + root.findall(".//x:div", ns):
            if elem.text:
                text = _clean_text(elem.text)
                if text:
                    content.append({
                        "type": "paragraph",
                        "text": text
                    })
        
        # If no paragraphs found, try to extract any text content
        if not content:
            text_elements = root.findall(".//*", ns)
            for elem in text_elements:
                if elem.text and elem.text.strip():
                    text = _clean_text(elem.text)
                    if text and len(text) > 10:  # Only meaningful text
                        content.append({
                            "type": "paragraph",
                            "text": text
                        })
        
        return {
            "title": title,
            "content": content
        }
        
    except Exception as e:
        logger.error(f"Error parsing chapter HTML: {e}")
        return {
            "title": "Error",
            "content": [{"type": "paragraph", "text": "Error parsing chapter content"}]
        }


def parse_epub(epub_file_path: str) -> Dict[str, Any]:
    """Parse an EPUB file and return a structured representation."""
    
    try:
        with zipfile.ZipFile(epub_file_path, "r") as zf:
            # Validate EPUB structure
            if "META-INF/container.xml" not in zf.namelist():
                raise ValueError("Invalid EPUB: missing container.xml")
            
            # Get root file path
            rootfile_path = _get_rootfile_path(zf)
            
            # Parse content.opf
            content_info = _parse_content_opf(zf.read(rootfile_path))
            
            # Extract base path
            base_path = Path(rootfile_path).parent
            
            # Parse chapters
            chapters = []
            for idref in content_info["spine"]:
                if idref in content_info["manifest"]:
                    item_info = content_info["manifest"][idref]
                    href = item_info["href"]
                    
                    # Skip non-HTML files
                    if not item_info["type"].startswith("text/html"):
                        continue
                    
                    chapter_path = str(base_path / href)
                    try:
                        chapter_html = zf.read(chapter_path)
                        chapter_data = _parse_chapter(chapter_html)
                        if chapter_data["content"]:  # Only add non-empty chapters
                            chapters.append(chapter_data)
                    except Exception as e:
                        logger.warning(f"Error parsing chapter {chapter_path}: {e}")
                        continue
            
            return {
                "title": content_info["metadata"]["title"],
                "author": content_info["metadata"]["author"],
                "language": content_info["metadata"]["language"],
                "identifier": content_info["metadata"]["identifier"],
                "chapters": chapters,
                "total_chapters": len(chapters),
                "parsing_metadata": {
                    "format": "epub",
                    "version": "3.0",
                    "parsed_at": "2024-01-15T00:00:00Z"
                }
            }
            
    except Exception as e:
        logger.error(f"Error parsing EPUB file {epub_file_path}: {e}")
        raise ValueError(f"Failed to parse EPUB file: {str(e)}")
