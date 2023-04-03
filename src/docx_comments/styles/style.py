from collections import ChainMap
from functools import cached_property
from typing import TYPE_CHECKING

from lxml.etree import _Element

from docx_comments.elements.attrib import AttribDict, get_attrib
from docx_comments.ooxml_ns import ns

if TYPE_CHECKING:
    from docx_comments.styles.styles import Styles


class Style:
    """Representation of <w:style> OOXML document element."""

    def __init__(self, _id: str, styles: "Styles"):
        self._id = _id
        self._parent = styles
        self.element: _Element = self._parent._style_xml.xpath(
            "w:style[@w:styleId=$_id]", _id=self._id, **ns
        )[0]
        self.basedon: str = self.element.xpath("string(w:basedOn/@w:val)", **ns)

    def __repr__(self):
        return f"Style(_id='{self._id}',type='{self._type}')"

    @property
    def _name(self) -> str:
        return self.element.xpath("string(w:name/@w:val)", **ns)

    @property
    def _type(self) -> str:
        return self.element.xpath("string(@w:type)", **ns)

    @property
    def _paragraph(self) -> AttribDict:
        return get_attrib(self.element.xpath("w:pPr/*", **ns))

    @property
    def _run(self) -> AttribDict:
        return get_attrib(self.element.xpath("w:rPr/*", **ns))

    def _style_inheritance(self) -> list[str]:
        based_on_list = []
        based_on = self.basedon
        while based_on:
            based_on_list.append(based_on)
            following_style = self._parent[based_on].basedon
            based_on = following_style
        return based_on_list

    @cached_property
    def paragraph(self) -> ChainMap:
        props = (
            self._parent[based_on_style]._paragraph
            for based_on_style in self._style_inheritance()
        )
        return ChainMap(self._paragraph, *props, self._parent.doc_default_props_para)

    @cached_property
    def run(self) -> ChainMap:
        props = (
            self._parent[based_on_style]._run
            for based_on_style in self._style_inheritance()
        )
        return ChainMap(self._run, *props, self._parent.doc_default_props_run)
