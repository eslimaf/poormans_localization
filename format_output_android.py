#!/usr/bin/python3
import sys
import os
import errno
import xml.etree.ElementTree as etree
import xml.dom.minidom as dom
from utils import resource_path , Logger, LogLevel

# Constants
OUTPUT_DIR = 'android'
FOLDER_BASENAME = 'values'
XML_FILENAME = 'strings.xml'
FR_QUALIFIER = '-fr'
INDENTATION = '    '
ENCODING = 'utf-8'
TRANSLATABLE_FALSE = 'translatable_false'
EXCLUSION_ID = ''

class AndroidFormatter:
    # Constructor, receives the csv reader

    def __init__(self, reader, add_comment=True):
        self.reader = reader
        self.add_comment = add_comment
        self.logger = Logger(tag = self.__class__.__name__)

    def generate(self):
        en_root = etree.Element("resources")
        fr_root = etree.Element("resources")

        if(self.add_comment):
            comment = etree.Comment(
                "Auto-generated by Poor Man's Localization")
            en_root.insert(1, comment)
            fr_root.insert(1, comment)

        self.logger.info("Parsing Android strings")

        next(self.reader)  # skip the first line

        # iterate csv reader
        for line in self.reader:
            if(line[0] == EXCLUSION_ID):
                continue

            if(line[3] == TRANSLATABLE_FALSE):
                etree.SubElement(en_root, "string",
                                 name="{}".format(line[0]), translatable="false").text = line[2]
            else:
                etree.SubElement(en_root, "string",
                                 name="{}".format(line[0])).text = line[2]
                etree.SubElement(fr_root, "string",
                                 name="{}".format(line[0])).text = line[3]

        # Formatter
        self.logger.info("Formatting xmls")
        en_rough_xml = etree.tostring(en_root, encoding='utf-8', method='xml')
        en_reparsed = dom.parseString(en_rough_xml)
        en_pretty_xml = en_reparsed.toprettyxml(
            indent=INDENTATION, encoding=ENCODING)

        fr_rough_xml = etree.tostring(fr_root, encoding='utf-8', method='xml')
        fr_reparsed = dom.parseString(fr_rough_xml)
        fr_pretty_xml = fr_reparsed.toprettyxml(
            indent=INDENTATION, encoding=ENCODING)

        # Write to file
        en_strings = self.__get_en_xml_file()
        fr_strings = self.__get_fr_xml_file()

        if not os.path.exists(os.path.dirname(en_strings)):
            try:
                os.makedirs(os.path.dirname(en_strings))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        if not os.path.exists(os.path.dirname(fr_strings)):
            try:
                os.makedirs(os.path.dirname(fr_strings))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        en_xml_file = open(en_strings, "w")
        en_xml_file.write(en_pretty_xml)
        en_xml_file.close()
        self.logger.info("Created: %s" % en_strings)

        fr_xml_file = open(fr_strings, "w")
        fr_xml_file.write(fr_pretty_xml)
        fr_xml_file.close()
        self.logger.info("Created: %s" % fr_strings)

    # Helper
    @staticmethod
    def __get_en_xml_file():
        return resource_path(os.path.join(OUTPUT_DIR, FOLDER_BASENAME, XML_FILENAME)) 

    @staticmethod
    def __get_fr_xml_file():
        return resource_path(os.path.join(OUTPUT_DIR, FOLDER_BASENAME + FR_QUALIFIER, XML_FILENAME))
