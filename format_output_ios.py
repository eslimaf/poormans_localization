#!/usr/bin/python3
import os
import errno
import plistlib
from utils import resource_path , Logger, LogLevel

OUTPUT_DIR = 'ios'
DIR_LPROJ = '.lproj'
EN_LANG = 'en'
FR_LANG = 'fr'
STRINGS_FILENAME = 'Localizable.strings'
TRANSLATABLE_FALSE = 'translatable_false'


class IosFormatter:
    def __init__(self, reader):
        self.reader = reader
        self.logger = Logger(tag = self.__class__.__name__)

    def generate(self):
        en_strings = ''
        fr_strings = ''

        self.logger.info("Parsing iOS strings")
        
        for line in self.reader:
            en_strings += '"{}" = "{}"\n'.format(line[1], line[2])
            # Use same strings if translatable false is applied
            translated_string = (line[3], line[2])[line[3] == TRANSLATABLE_FALSE]
            fr_strings += '"{}" = "{}"\n'.format(line[1], translated_string)

        en_filename = self.__get_en_strings_file()
        fr_filename = self.__get_fr_strings_file()

        if not os.path.exists(os.path.dirname(en_filename)):
            try:
                os.makedirs(os.path.dirname(en_filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        if not os.path.exists(os.path.dirname(fr_filename)):
            try:
                os.makedirs(os.path.dirname(fr_filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        en_file = open(en_filename, 'w')
        en_file.write(en_strings)
        en_file.close()
        self.logger.info("Created: %s" % en_filename)

        fr_file = open(fr_filename, 'w')
        fr_file.write(fr_strings)
        fr_file.close()
        self.logger.info("Created: %s" % fr_filename)

    @staticmethod
    def __get_en_strings_file():
        return resource_path(os.path.join(OUTPUT_DIR, EN_LANG + DIR_LPROJ, STRINGS_FILENAME))

    @staticmethod
    def __get_fr_strings_file():
        return resource_path(os.path.join(OUTPUT_DIR, FR_LANG + DIR_LPROJ, STRINGS_FILENAME))
