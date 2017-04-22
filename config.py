#!/usr/bin/env python
import os

#------------------------------------------------#
# Path settings.                                 #
#------------------------------------------------#

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
BIN_ROOT = os.path.join(PROJECT_DIR, 'bin')

PANO_ROOT = os.path.join(STATIC_ROOT, 'panos')
PREVIEW_ROOT = os.path.join(STATIC_ROOT, 'previews')
SMALL_ROOT = os.path.join(STATIC_ROOT, 'small')
JSON_ROOT = os.path.join(STATIC_ROOT, 'json')


#------------------------------------------------#
# S3 settings                                    #
#------------------------------------------------#

STATIC_BUCKET = 'bubbles-static'
STATIC_URL = 'https://s3.amazonaws.com/{}'.format(STATIC_BUCKET)


#------------------------------------------------#
# PIL settings.                                  #
#------------------------------------------------#

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'tif', 'png', ]


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

CONTEXT = {'URL_PREFIX': URL_PREFIX, 'ENV': ENV, 'STATIC_PREFIX': STATIC_URL}