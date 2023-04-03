"""Module for the run <w:r> element."""

# from functools import cache

from typing import TYPE_CHECKING

from lxml.etree import _Element

from docx_comments.elements.attrib import AttribDict, get_attrib
from docx_comments.elements.element_base import DOCXElement
from docx_comments.elements.properties import Properties
from docx_comments.ooxml_ns import ns

if TYPE_CHECKING:
    from docx_comments.elements.paragraph import Paragraph


# @cache
class Run(DOCXElement):
    """Representation of run <w:r> element."""

    def __init__(self, element: _Element, paragraph: "Paragraph"):
        super().__init__(element)
        self._parent = paragraph
        self.text: str = self.element.xpath("string(w:t)", **ns)
        self._props: AttribDict = get_attrib(self.element.xpath("w:rPr/*", **ns))

    def __str__(self) -> str:
        return self.text

    @property
    def props(self) -> Properties:
        return Properties(self)

    @props.setter
    def props(self, prop_dict: dict) -> dict:
        self._props = prop_dict

    @property
    def footnote(self) -> list:
        note_id = self.element.xpath("string(w:footnoteReference/@w:id)", **ns)
        return self._parent._doc.notes.footnotes.get(note_id, [])

    @property
    def endnote(self) -> list:
        note_id = self.element.xpath("string(w:endnoteReference/@w:id)", **ns)
        return self._parent._doc.notes.endnotes.get(note_id, [])
