from typing import TYPE_CHECKING

from lxml.etree import _Element

from docx_comments.elements.paragraph import Paragraph
from docx_comments.elements.paragraph_group import ParagraphGroup
from docx_comments.ooxml_ns import ns

if TYPE_CHECKING:
    from docx_comments.notes.notes import Notes


class Note(ParagraphGroup):
    def __init__(self, _id: str, notes: "Notes"):
        self._id = _id
        self._parent = notes

    def __repr__(self):
        return f"{self.__class__.__name__}(_id='{self._id}')"


class FootNote(Note):
    def __init__(self, _id: str, notes: "Notes"):
        super().__init__(_id, notes)
        self.element: _Element = self._parent._footnotes_xml.xpath(
            "w:footnote[@w:id=$_id]", _id=self._id, **ns
        )[0]
        self.paragraphs: list[Paragraph] = [
            Paragraph(para, self._parent._doc)
            for para in self.element.xpath("w:p", **ns)
        ]


class EndNote(Note):
    def __init__(self, _id: str, notes: "Notes"):
        super().__init__(_id, notes)
        self.element: _Element = self._parent._endnotes_xml.xpath(
            "w:endnote[@w:id=$_id]", _id=self._id, **ns
        )[0]
        self.paragraphs: list[Paragraph] = [
            Paragraph(para, self._parent._doc)
            for para in self.element.xpath("w:p", **ns)
        ]
