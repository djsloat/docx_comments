import re

from docx_comments.elements.attrib import AttribDict


class PropDecode:
    """Decodes OOXML format properties."""

    def __init__(self, props: AttribDict):
        self._props = props

    def _toggled(self, prop: str) -> bool:
        # b, i, strike, dstrike (among others) are 'toggled'
        try:
            toggle1 = not self._props.get(prop)  # {"b": {}}
            toggle2 = self._props.get(prop, {}).get("val", "") in ("1", "on", "true")
        except KeyError:
            return False
        else:
            return toggle1 or toggle2

    @property
    def bold(self) -> bool:
        return self._toggled("b")

    @property
    def italic(self) -> bool:
        return self._toggled("i")

    @property
    def underline(self) -> bool:
        return "u" in self._props and not re.search(
            "[D|d]ouble|^none$", self._props.get("u", {}).get("val", "")
        )

    @property
    def strike(self) -> bool:
        return self._toggled("strike")

    @property
    def d_underline(self) -> bool:
        return re.search("[D|d]ouble", self._props.get("u", {}).get("val", ""))

    @property
    def d_strike(self) -> bool:
        return self._toggled("dstrike")

    @property
    def subscript(self) -> bool:
        return self._props.get("vertAlign", {}).get("val", "") == "subscript"

    @property
    def superscript(self) -> bool:
        return self._props.get("vertAlign", {}).get("val", "") == "superscript"

    @property
    def caps(self) -> bool:
        return self._toggled("caps")

    @property
    def color(self) -> bool:
        return self._props.get("color", {}).get("val", "")

    @property
    def emboss(self) -> bool:
        return self._toggled("emboss")

    @property
    def imprint(self) -> bool:
        return self._toggled("imprint")

    @property
    def outline(self) -> bool:
        return self._toggled("outline")

    @property
    def shadow(self) -> bool:
        return self._toggled("shadow")

    @property
    def smallcaps(self) -> bool:
        return self._toggled("smallCaps")

    @property
    def size(self) -> bool:
        return self._props.get("sz", {}).get("val", "")

    @property
    def vanish(self) -> bool:
        return self._toggled("vanish")
