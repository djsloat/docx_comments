"""Property attributes"""

from collections import UserDict

from lxml.etree import QName, _Element


class AttribDict(UserDict):
    """UserDict that removes URI from element tag string in key."""

    def __setitem__(self, key, value):
        qkey = QName(key).localname
        self.data[qkey] = value


def get_attrib(prop_element: _Element) -> AttribDict:
    attrib_dict = AttribDict()
    for prop in prop_element:
        prop: _Element
        if len(prop) > 0:
            attrib_dict[prop.tag] = get_attrib(prop)
        else:
            attrib_dict[prop.tag] = AttribDict(prop.attrib)
    return attrib_dict
