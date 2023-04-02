"""Comment bubble."""

from lxml.etree import _Element

from docx_comments.docx import Document
from docx_comments.elements.paragraph import Paragraph
from docx_comments.elements.paragraph_group import ParagraphGroup


class Bubble(ParagraphGroup):
    """Comment bubble."""

    def __init__(self, paragraphs: _Element, document: Document):
        self._doc = document
        self.paragraphs = [Paragraph(el, self._doc) for el in paragraphs]
        super().__init__(self.paragraphs)
