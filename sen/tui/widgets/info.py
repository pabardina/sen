"""
Info widgets:
 * display detailed info about an object
"""
import logging

from sen.tui.widgets.list.base import VimMovementListBox

import urwid

from sen.util import humanize_bytes

logger = logging.getLogger(__name__)


class ImageInfoItemWidget(urwid.AttrMap):
    def __init__(self, key, value=None):
        attr_map = "main_list_dg"
        focus_map = "main_list_white"
        if value:
            w = urwid.Columns([
                urwid.AttrMap(urwid.Text(key, align="left", wrap="any"), attr_map, focus_map),
                urwid.AttrMap(urwid.Text(value, align="left", wrap="any"), attr_map, focus_map),
            ])
        else:
            w = urwid.Text(key, align="left", wrap="any")
        super().__init__(w, attr_map, focus_map=focus_map)


class ImageInfoWidget(VimMovementListBox):
    """
    display info about image
    """
    def __init__(self, docker_image):
        self.docker_image = docker_image
        l = self._basic_data() + self._labels()
        self.walker = urwid.SimpleFocusListWalker(l)
        super().__init__(self.walker)

    def _basic_data(self):
        l = [
            ImageInfoItemWidget("Id", self.docker_image.image_id),
            ImageInfoItemWidget("Created", "{0}, {1}".format(self.docker_image.display_formal_time_created(),
                                                       self.docker_image.display_time_created())),
            ImageInfoItemWidget("Size", humanize_bytes(self.docker_image.size)),
        ]
        return l

    def _labels(self):
        if not self.docker_image.labels:
            return []
        l = [ImageInfoItemWidget("Labels")]
        for label_key, label_value in self.docker_image.labels.items():
            l.append(ImageInfoItemWidget(label_key, label_value))

        return l
