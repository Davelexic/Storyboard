import zipfile

from backend.app.services.converter import generate_cinematic_markup
from backend.app.services.parser import parse_epub


def _create_sample_epub(tmp_path):
    """Create a simple EPUB book for testing and return its path."""

    epub_path = tmp_path / "sample.epub"
    with zipfile.ZipFile(epub_path, "w") as zf:
        # Required mimetype file must be stored without compression
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)

        container_xml = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<container version='1.0' xmlns='urn:oasis:names:tc:opendocument:xmlns:container'>"
            "<rootfiles><rootfile full-path='OEBPS/content.opf' "
            "media-type='application/oebps-package+xml'/></rootfiles></container>"
        )
        zf.writestr("META-INF/container.xml", container_xml)

        content_opf = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<package xmlns='http://www.idpf.org/2007/opf' version='3.0'>"
            "<metadata xmlns:dc='http://purl.org/dc/elements/1.1/'>"
            "<dc:title>Sample Book</dc:title></metadata>"
            "<manifest><item id='ch1' href='ch1.xhtml' media-type='application/xhtml+xml'/></manifest>"
            "<spine><itemref idref='ch1'/></spine></package>"
        )
        zf.writestr("OEBPS/content.opf", content_opf)

        chapter_html = (
            "<html xmlns='http://www.w3.org/1999/xhtml'><head><title>Chapter 1</title></head>"
            "<body><h1>Chapter 1</h1><p>Hello world.</p><p>Second paragraph.</p></body></html>"
        )
        zf.writestr("OEBPS/ch1.xhtml", chapter_html)

    return epub_path


def test_parse_epub(tmp_path):
    epub_path = _create_sample_epub(tmp_path)
    parsed = parse_epub(str(epub_path))

    assert parsed["title"] == "Sample Book"
    assert len(parsed["chapters"]) == 1
    chapter = parsed["chapters"][0]
    assert chapter["title"] == "Chapter 1"
    assert chapter["paragraphs"] == ["Hello world.", "Second paragraph."]


def test_generate_cinematic_markup():
    parsed_book = {
        "title": "Sample Book",
        "chapters": [
            {
                "title": "Chapter 1",
                "paragraphs": ["Hello world.", "Second paragraph."],
            }
        ],
    }

    markup = generate_cinematic_markup(parsed_book)

    assert markup["bookTitle"] == "Sample Book"
    assert markup["theme"] == "default"
    assert len(markup["chapters"]) == 1
    chapter_markup = markup["chapters"][0]
    assert chapter_markup["chapterTitle"] == "Chapter 1"
    assert chapter_markup["content"][0] == {
        "type": "paragraph",
        "text": "Hello world.",
        "effects": [],
    }
    assert chapter_markup["content"][1]["text"] == "Second paragraph."

