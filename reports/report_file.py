import json

from config import REPORT_FILE_NAME


def write_on_file(result):
    f = open(REPORT_FILE_NAME, 'w')
    f.write(json.dumps(result))
    f.close()