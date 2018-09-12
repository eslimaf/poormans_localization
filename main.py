import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import csv
from format_output_android import AndroidFormatter

# File csv file structure
# index_0, index_1, index_2, index_3
# android_id, ios_id, en, fr

# File to be read passed as argument
filename = sys.argv[1]

with open(filename, 'r') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # skip the first line

    androidFormatter = AndroidFormatter(reader)
    androidFormatter.generate()
