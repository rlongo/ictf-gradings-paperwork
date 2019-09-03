from ictf_pipeline.data_models import BeltLevel, BeltLookup

import os
import xml.etree.ElementTree as ET

import ictf_pipeline.parsers.helpers as helpers


class BeltLookupXML(BeltLookup):
    def __init__(self, config_file):
        assert helpers.verify_file(config_file)
        self._belt_levels = self._parse_xml(config_file)

    def _get_belt_levels(self):
        return self._belt_levels

    def _parse_xml(self, config_file):
        tree = ET.parse(config_file)
        root = tree.getroot()

        belt_levels = []

        config = dict()
        lookup = dict()

        for tag in root.findall("./belt"):
            belt_id, next_id, belt_level = self._parse_belt_xml(tag)
            config[belt_id] = belt_level
            lookup[belt_id] = next_id

        for belt_id, belt in config.items():
            try:
                belt.next_level = config[lookup[belt_id]]
            except BaseException:
                pass  # Ignore any exceptions here... next can be none
            belt_levels.append(belt)
        return belt_levels

    def _parse_belt_xml(self, tag):
        '''Parses and returns a belt level.
        Note that this method does not connect the next field of belt level
        :return belt_id, next_id, belt_level
        '''
        belt_name = tag.attrib["name"]
        belt_id = tag.attrib["id"]
        next_belt_id = None
        match_pattern = tag.findtext(".//match_pattern")
        try:
            next_belt_id = tag.attrib["next_belt"]
        except BaseException:
            pass  # This is optional

        paperwork = []
        attributes = dict()

        for target in tag.findall(".//attributes/attribute"):
            attributes[target.attrib["name"]] = target.text
        for target in tag.findall(".//paperworks/paperwork"):
            name = None
            try:
                name = target.attrib["name"]
            except BaseException:
                name = os.path.splitext(os.path.basename(target.text))[0]
            paperwork.append((name, target.text))

        return belt_id, next_belt_id, BeltLevel(
            belt_name, match_pattern, None, paperwork, attributes)
