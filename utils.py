import subprocess, os
import simplejson as json

import hashlib

from PIL import Image, ImageFilter

import config
import boto3


s3 = boto3.resource('s3')


def get_md5(message):    
    """
    Returns MD5 of string passed to it.
    """
    return hashlib.md5(message.encode('utf-8')).hexdigest()



def metadata_to_json(image_file, json_file):
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    try:
        exiftool_output = json.loads(subprocess.check_output([config.EXIFTOOL_PATH, '-m', '-G', '-struct', '-s', '-s', '-g', '-json', image_file]))[0]
        with open(json_file, 'w') as open_json_file:
            open_json_file.write(json.dumps(exiftool_output, sort_keys=True, indent=2))
        return exiftool_output
    except:
        return None


def preview_image(original, output):
    os.makedirs(os.path.dirname(output), exist_ok=True)


    im = Image.open(original)
    width, height = im.size   # Get dimensions
    new_height = width / 3

    left = 0
    top = (height - new_height)/2
    right = width
    bottom = (height + new_height)/2

    output_im = im.crop((left, top, right, bottom))
    output_im.thumbnail((900, 300))
    output_im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=125, threshold=3))
    output_im.save(output)


def small_image(original, output):
    os.makedirs(os.path.dirname(output), exist_ok=True)
    im = Image.open(original)
    width, height = im.size
    im.thumbnail((1024, 512))
    im.save(output)


def make_pano_record(pano_key):
    base_key = pano_key.replace('panos/','').replace(' ', '+')

    pano_url = '{}/panos/{}'.format(config.STATIC_URL, base_key)
    preview_url = '{}/previews/{}'.format(config.STATIC_URL, base_key)
    small_url = '{}/small/{}'.format(config.STATIC_URL, base_key)
    json_url = '{}/json/{}'.format(config.STATIC_URL, base_key.replace('.jpg', '.json'))

    this_pano = {'pano': pano_url, 'preview': preview_url, 'small': small_url, 'json': json_url, 'id': 'p{}'.format(get_md5(base_key))}
    return this_pano


def get_panos_for(gallery=None):
    s3 = boto3.resource('s3')
    this_bucket = s3.Bucket(config.STATIC_BUCKET)
    pano_images = [x.key for x in this_bucket.objects.filter(Prefix='panos/{}'.format(gallery)) if x.key.endswith('.jpg')]

    panos = [make_pano_record(x) for x in pano_images]
    return panos


def get_panos():
    panos = []
    for directory, directories, files in os.walk(config.PANO_ROOT, topdown=False, followlinks=True):
        for name in files:
            if name.endswith('.jpg'):
                path = os.path.join(directory, name)
                relative_path = os.path.relpath(path, config.PANO_ROOT)

                preview_path = os.path.join(config.PREVIEW_ROOT, relative_path)
                small_path = os.path.join(config.SMALL_ROOT, relative_path)
                json_path = os.path.join(config.JSON_ROOT, relative_path.replace('.jpg', '.json'))

                pano_url = os.path.join('/static', os.path.relpath(path, config.STATIC_ROOT))
                preview_url = os.path.join('/static', os.path.relpath(preview_path, config.STATIC_ROOT))
                small_url = os.path.join('/static', os.path.relpath(small_path, config.STATIC_ROOT))
                json_url = os.path.join('/static', os.path.relpath(json_path, config.STATIC_ROOT))

                this_pano = {'pano': pano_url, 'preview': preview_url, 'small': small_url, 'json':json_url, 'id': 'p{}'.format(get_md5(relative_path))}

                panos.append(this_pano)

    return panos


def get_galleries():
    s3 = boto3.resource('s3')
    this_bucket = s3.Bucket(config.STATIC_BUCKET)
    galleries = [x.key.strip('/').replace('panos/','') for x in this_bucket.objects.filter(Prefix='panos/') if ( not x.key.endswith('.jpg') and not x.key =='panos/')]
    return galleries