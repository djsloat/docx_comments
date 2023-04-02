"""Class Document"""

from functools import cached_property
from pathlib import Path
from zipfile import ZipFile

from lxml import etree
from lxml.etree import _Element

from docx_comments.comments.comments import Comments
from docx_comments.notes.notes import Notes
from docx_comments.styles.styles import Styles
from docx_comments.logger import log_filename


@log_filename
class Document:
    """Opens docx document and creates XML file tree"""

    def __init__(self, filename):
        self.file = Path(filename)
        self.styles = Styles(self)
        self.notes = Notes(self)
        self.comments = Comments(self)

    def __repr__(self):
        return f"Document(file='{self.file}')"

    @cached_property
    def xml(self) -> dict[str, _Element]:
        with ZipFile(self.file, "r") as z:
            return {
                filename: etree.fromstring(z.read(filename))
                for filename in z.namelist()
                if filename
                in (
                    "word/document.xml",
                    "word/styles.xml",
                    "word/comments.xml",
                    "word/commentsExtended.xml",
                    "word/footnotes.xml",
                    "word/endnotes.xml",
                )
            }
