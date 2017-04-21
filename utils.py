import subprocess
import simplejson as json
from PIL import Image, ImageFilter

import config


def metadata_to_json(image_file, json_file):
    try:
        exiftool_output = json.loads(subprocess.check_output([config.EXIFTOOL_PATH, '-m', '-G', '-struct', '-s', '-s', '-g', '-json', image_file]))[0]
        with open(json_file, 'w') as open_json_file:
            open_json_file.write(json.dumps(exiftool_output, sort_keys=True, indent=2))
        return exiftool_output
    except:
        return None


def preview_image(original, output):

    im = Image.open(original)
    width, height = im.size   # Get dimensions
    new_height = width / 3

    left = 0
    top = (height - new_height)/2
    right = width
    bottom = (height + new_height)/2

    output_im = im.crop((left, top, right, bottom))
    output_im.thumbnail((900,300))
    output_im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=125, threshold=3))
    output_im.save(output)