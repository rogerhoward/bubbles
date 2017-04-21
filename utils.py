import subprocess
import simplejson as json

import config


def metadata_to_json(image_file, json_file):
    try:
        exiftool_output = json.loads(subprocess.check_output([config.EXIFTOOL_PATH, '-m', '-G', '-struct', '-s', '-s', '-g', '-json', image_file]))[0]
        with open(json_file, 'w') as open_json_file:
            open_json_file.write(json.dumps(exiftool_output, sort_keys=True, indent=2))
        return exiftool_output
    except:
        return None