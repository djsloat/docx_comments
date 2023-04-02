"""Comments combined"""

from lxml.etree import _Element

from docx_comments.comments.comment import Comment
from docx_comments.docx import Document
from docx_comments.logger import log_comments
from docx_comments.ooxml_ns import ns


@log_comments
class Comments:
    """Comments contained within document. Only top-level comments are included.
    Replies of comments are not."""

    def __init__(self, document: Document):
        self._doc = document
        self._document_root: _Element = self._doc.xml["word/document.xml"]
        self._comment_metadata_root: _Element = self._doc.xml.get("word/comments.xml")
        self._comment_ext_root: _Element = self._doc.xml.get(
            "word/commentsExtended.xml"
        )
        self.comment_ids: list = self._document_root.xpath(
            "./w:body//w:commentRangeStart/@w:id",
            **ns,
        )
        self._all_comments = [Comment(_id, self) for _id in self.comment_ids]
        self.comments = [
            comment for comment in self._all_comments if not comment._is_reply
        ]

    def __repr__(self):
        return f"Comments(file='{self._doc.file}',count={len(self.comments)})"

    def __getitem__(self, key):
        return self.comments[key]

    def __iter__(self):
        return iter(self.comments)

    def __len__(self):
        return len(self.comments)
