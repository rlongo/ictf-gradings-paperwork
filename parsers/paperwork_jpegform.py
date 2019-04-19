import os
import xml.etree.ElementTree as ET

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from data_models import Paperwork
import parsers.helpers as helpers

class PaperworkJPEGForm(Paperwork):
    '''Template form take a template and generates the same file with annotations super-imposed'''

    def __init__(self, name, template_file, config_file):
        assert helpers.verify_file(template_file)
        assert helpers.verify_file(config_file)

        self.name = name
        self._template_file = template_file
        self._config = self._parse_config(config_file)

    def generate(self, output_file, sub_map):
        helpers.create_file_dirs(output_file)

        img = Image.open(self._template_file)
        draw = ImageDraw.Draw(img)

        for config in self._config:
            afont = ImageFont.truetype(config.font, int(config.font_size))
            ink = self._hex_as_rgb(config.font_colour)
            val = self._get_config_val(config.field_name, sub_map)
            draw.text((int(config.x), int(config.y)), val, ink, font=afont)
        
        img.save(output_file)

    def _get_config_val(self, key, sub_map):
        keys = key.split('.')
        val = sub_map
        for k in keys:
            if isinstance(val,dict):
                val = val[k]
            else:
                val = getattr(val, k)

        return str(val)

    def _parse_config(self, config_file):
        tree = ET.parse(config_file)
        root = tree.getroot()

        config = []

        for tag in root.findall("./field"):
            field_name = tag.attrib["name"]
            x, y = tag.attrib["x"], tag.attrib["y"]
            font = tag.attrib["font"]
            font_colour = tag.attrib["font_colour"]
            font_size = tag.attrib["font_size"]
            config.append(_TemplateConfig(field_name, x, y, font, font_colour, font_size))

        return config

    def _hex_as_rgb(self, hex_colour):
        hex_colour = hex_colour.strip('#')
        r = int(hex_colour[ :2], 16)
        g = int(hex_colour[2:4], 16)
        b = int(hex_colour[4: ], 16)
        return (r, g, b)


class _TemplateConfig:
    '''Config entry for a template'''

    def __init__(self, field_name, x, y, font, font_colour, font_size):
        self.field_name = field_name
        self.x, self.y = x, y
        self.font = font
        self.font_colour = font_colour
        self.font_size = font_size