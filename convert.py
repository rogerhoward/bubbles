#!/usr/bin/env python
import os, sys
import config
import utils
from pprint import pprint

#------------------------------------------------#
#  Command line options                          #
#------------------------------------------------#

def main():
    utils.preview_image('/Users/rogerhoward/repos/bubbles/static/panos/20040324getty01sphere.jpg', '/Users/rogerhoward/repos/bubbles/static/previews/20040324getty01sphere.jpg')

if __name__ == '__main__':
    # main()

    for directory, directories, files in os.walk(config.PANO_ROOT, topdown=False, followlinks=True):
            for name in files:
                if name.endswith('.jpg'):
                    path = os.path.join(directory, name)
                    relative_path = os.path.relpath(path, config.PANO_ROOT)

                    preview_path = os.path.join(config.PREVIEW_ROOT, relative_path)
                    json_path = os.path.join(config.JSON_ROOT, relative_path.replace('.jpg', '.json'))

                    utils.preview_image(path, preview_path)
                    utils.metadata_to_json(path, json_path)

                    pprint((path, preview_path, json_path))

