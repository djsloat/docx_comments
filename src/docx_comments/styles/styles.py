"""Styles for DOCX
    STYLE INHERITANCE
        PARAGRAPHS
            Use default paragraph properties (docDefaults)
            Append paragraph style properties
                [Local paragraph properties are only used for list formats and bullets]

        RUNS
            Use default run properties (docDefaults)
            Append run style properties
            Append local run properties

        COMBINE PARAGRAPHS AND RUN FORMATTING
            Append result run properties over paragraph properties

    Styles can also be based on other styles, and 'inherit' those styles' format
    attributes. And that inherited style may itself be based on another style - and so
    on until the 'base style'.
"""

from lxml.etree import _Element

from docx_comments.elements.attrib import AttribDict, get_attrib
from docx_comments.ooxml_ns import ns
from docx_comments.styles.style import Style


class Styles:
    """Represents styles data in OOXML document."""

    def __init__(self, style_xml: _Element):
        self.xml = style_xml

    @property
    def style_ids(self):
        return self.xml.xpath("w:style/@w:styleId", **ns)

    @property
    def doc_default_props_para(self) -> AttribDict:
        xpath = "w:docDefaults/w:pPrDefault/w:pPr/*"
        return get_attrib(self.xml.xpath(xpath, **ns))

    @property
    def doc_default_props_run(self) -> AttribDict:
        xpath = "w:docDefaults/w:rPrDefault/w:rPr/*"
        return get_attrib(self.xml.xpath(xpath, **ns))

    def style(self, style_id: str):
        return Style(
            self.xml.xpath("w:style[@w:styleId=$_style_id]", _style_id=style_id, **ns)
        )
