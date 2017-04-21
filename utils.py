import subprocess, os
import simplejson as json

import hashlib

from PIL import Image, ImageFilter

import config



def get_md5(message):    
    """
    Returns MD5 of string passed to it.
    """
    return hashlib.md5(message.encode('utf-8')).hexdigest()



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



def get_panos():
    panos = []
    for directory, directories, files in os.walk(config.PANO_ROOT, topdown=False, followlinks=True):
        for name in files:
            if name.endswith('.jpg'):
                path = os.path.join(directory, name)
                relative_path = os.path.relpath(path, config.PANO_ROOT)

                preview_path = os.path.join(config.PREVIEW_ROOT, relative_path)
                json_path = os.path.join(config.JSON_ROOT, relative_path.replace('.jpg', '.json'))

                pano_url = os.path.join('/static', os.path.relpath(path, config.STATIC_ROOT))
                preview_url = os.path.join('/static', os.path.relpath(preview_path, config.STATIC_ROOT))
                json_url = os.path.join('/static', os.path.relpath(json_path, config.STATIC_ROOT))

                this_pano = {'pano': pano_url, 'preview': preview_url, 'json':json_url, 'id': 'p{}'.format(get_md5(relative_path))}

                panos.append(this_pano)

    return panos

