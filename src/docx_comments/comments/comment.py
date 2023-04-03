"""Comment data container"""

from functools import cache
from reprlib import Repr
from typing import TYPE_CHECKING

from lxml.etree import _Element

from docx_comments.elements.bubble import Bubble
from docx_comments.elements.paragraph import CommentParagraph
from docx_comments.elements.paragraph_group import ParagraphGroup
from docx_comments.ooxml_ns import ns

if TYPE_CHECKING:
    from docx_comments.comments.comments import Comments


class Comment(ParagraphGroup):
    """Representation of comment."""

    def __init__(self, /, _id: str | int, comments: "Comments", **attrs):
        self._id = _id
        self._parent = comments
        self._attrs = attrs
        self.paragraphs = [
            CommentParagraph(el, self._parent._doc, self)
            for el in list(self.get_paragraphs())
        ]
        super().__init__(self.paragraphs)

    def __repr__(self):
        return f"Comment(_id='{self._id}',text={Repr().repr(self.text)})"

    @property
    def _bounds(self) -> list[_Element]:
        return self._parent._document_root.xpath(
            ".//w:commentRangeStart[@w:id=$_id]|" ".//w:commentRangeEnd[@w:id=$_id]",
            _id=self._id,
            **ns,
        )

    @cache
    def get_paragraphs(self):
        start, end = self._bounds
        start_paragraph: _Element = start.xpath(
            "parent::w:p|following-sibling::w:p[1]", **ns
        )[0]
        end_paragraph: _Element = end.xpath(
            "parent::w:p|preceding-sibling::w:p[1]", **ns
        )[0]
        xpath = (
            "(self::w:p|following::w:p)"
            r"[(not(re:test(string(.),'^\s*$')) or w:commentRangeEnd)]"
        )
        paragraphs = (x for x in start_paragraph.xpath(xpath, **ns))
        for para in paragraphs:
            yield para
            if para == end_paragraph:
                break

    def insert_paragraph(self, position, element):
        self.paragraphs.insert(
            position, CommentParagraph(element, self._parent._doc, self)
        )

    @property
    def _is_reply(self) -> bool | None:
        if (
            self._parent._comment_metadata_root is not None
            and self._parent._comment_ext_root is not None
        ):
            comment_paraid_code = self._parent._comment_metadata_root.xpath(
                "string(w:comment[@w:id=$_id]/w:p[last()]/@w14:paraId)",
                _id=self._id,
                **ns,
            )
            return self._parent._comment_ext_root.xpath(
                "boolean(w15:commentEx[@w15:paraId=$_paraid_parent]/@w15:paraIdParent)",
                _paraid_parent=comment_paraid_code,
                **ns,
            )

    @property
    def reply(self) -> "Comment" or None:
        if (
            self._parent._comment_metadata_root is not None
            and self._parent._comment_ext_root is not None
        ):
            comment_paraid_code = self._parent._comment_metadata_root.xpath(
                "string(w:comment[@w:id=$_id]/w:p[last()]/@w14:paraId)",
                _id=self._id,
                **ns,
            )
            reply_paraid_code = self._parent._comment_ext_root.xpath(
                "string(w15:commentEx[@w15:paraIdParent=$_paraid_parent]/@w15:paraId)",
                _paraid_parent=comment_paraid_code,
                **ns,
            )
            reply_comment_id = self._parent._comment_metadata_root.xpath(
                "string(w:comment[w:p[last()]/@w14:paraId=$_reply_paraid]/@w:id)",
                _reply_paraid=reply_paraid_code,
                **ns,
            )
            if reply_comment_id:
                return Comment(reply_comment_id, self._parent)

    @property
    def author(self) -> str:
        if self._parent._comment_metadata_root is not None:
            return self._parent._comment_metadata_root.xpath(
                "string(w:comment[@w:id=$_id]/@w:author)", _id=self._id, **ns
            )
        return ""

    @property
    def date(self) -> str:
        if self._parent._comment_metadata_root is not None:
            return self._parent._comment_metadata_root.xpath(
                "string(w:comment[@w:id=$_id]/@w:date)", _id=self._id, **ns
            )
        return ""

    @property
    def initials(self) -> str:
        if self._parent._comment_metadata_root is not None:
            return self._parent._comment_metadata_root.xpath(
                "string(w:comment[@w:id=$_id]/@w:initials)", _id=self._id, **ns
            )
        return ""

    @property
    def bubble(self) -> Bubble:
        return Bubble(
            self._parent._comment_metadata_root.xpath(
                "w:comment[@w:id=$_id]/w:p", _id=self._id, **ns
            ),
            self._parent._doc,
        )
