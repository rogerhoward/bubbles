#!/usr/bin/env python
import os, sys
import PIL.Image
import config



#------------------------------------------------#
# Path settings.                                 #
#------------------------------------------------#

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(config.PROJECT_DIR, 'static')
BIN_ROOT = os.path.join(PROJECT_DIR, 'bin')
PANO_ROOT = os.path.join(config.PROJECT_DIR, STATIC_ROOT, 'panos')
PREVIEW_ROOT = os.path.join(config.PROJECT_DIR, STATIC_ROOT, 'previews')


#------------------------------------------------#
# PIL settings.                                  #
#------------------------------------------------#

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'tif', 'png', ]

RESIZE_FILTERS = {
    'cubic': PIL.Image.CUBIC,
    'bilinear': PIL.Image.BILINEAR,
    'bicubic': PIL.Image.BICUBIC,
    'nearest': PIL.Image.NEAREST,
    'antialias': PIL.Image.ANTIALIAS,
    }


#------------------------------------------------#
# Metadata settings                              #
#------------------------------------------------#

EXTRACT_METADATA = True
EXIFTOOL_PATH = os.path.join(BIN_ROOT, 'exiftool/exiftool')


#------------------------------------------------#
# ENV settings.                                 #
#------------------------------------------------#

ENV = dict(os.environ)

if ENV.get('STAGE'):
    URL_PREFIX = '/{}'.format(ENV.get('STAGE'))
else:
    URL_PREFIX = ''


#------------------------------------------------#
# Sanitize ENV                                   #
#------------------------------------------------#

if 'AWS_SECURITY_TOKEN' in ENV:
    del ENV['AWS_SECURITY_TOKEN']
if 'AWS_SECRET_ACCESS_KEY' in ENV:
    del ENV['AWS_SECRET_ACCESS_KEY']


#------------------------------------------------#
# Context dict for passing to templates          #
#------------------------------------------------#

CONTEXT = {'URL_PREFIX': URL_PREFIX, 'ENV': ENV}