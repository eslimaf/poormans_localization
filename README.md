# Poor man's Localization Tool

Simple parser for csv file with format:

| android_id | ios_id | en    | fr      |
|------------|--------|-------|---------|
| str_id_0   | strId0 | Hello | Bonjour |
| str_id_1   | strId1 | World | Monde   |

## Usage
* Make sure you have python installed

`$ python lokalize.py <path to csv file>`

The output will be:
* android/values/strings.xml
* android/values-fr/strings.xml
* ios/en.lproj/Localizable.strings
* ios/fr.lproj/Localizable.strings
