#!/usr/bin/env python
import os
import flask
import config
import utils
import boto3

application = flask.Flask(__name__)
app = application
s3 = boto3.resource('s3')

#------------------------------------------------#
#  UI endpoints                                  #
#------------------------------------------------#

@app.route('/')
def index(path=None):
    """
    UI homepage.
    """
    return flask.render_template('home.html', context=config.CONTEXT, galleries=utils.get_galleries())


# @app.route('/aframe/')
@app.route('/gallery/<path:path>')
def gallery(path=None):
    """
    Dual routes which support browsing a list of zoomable images on your S3 bucket,
    and viewing each one in an Open Seadragon viewer.
    """
    return flask.render_template('gallery.html', context=config.CONTEXT, gallery=path, panos=utils.get_panos_for(path))



# @app.route('/aframe/')
@app.route('/aframe/<path:path>')
def aframe(path=None):
    """
    Dual routes which support browsing a list of zoomable images on your S3 bucket,
    and viewing each one in an Open Seadragon viewer.
    """
    if path:
        return flask.render_template('aframe.html', context=config.CONTEXT, pano=path)
    else:
        return flask.render_template('index.html', context=config.CONTEXT, panos=utils.get_panos())


@app.route('/panos.json')
@app.route('/panos/<path:path>')
def panojson(path=None):
    """
    Dual routes which support browsing a list of zoomable images on your S3 bucket,
    and viewing each one in an Open Seadragon viewer.
    """
    if path:
        return flask.send_from_directory(config.STATIC_ROOT, path)
    else:
        return flask.jsonify(utils.get_panos())


@app.route('/reactvr/')
@app.route('/reactvr/<path:path>')
def reactvr(path=None):
    """
    Dual routes which support browsing a list of zoomable images on your S3 bucket,
    and viewing each one in an Open Seadragon viewer.
    """
    if path:
        return flask.render_template('pano_reactvr.html', context=config.CONTEXT, pano=path)
    else:
        return flask.render_template('index_reactvr.html', context=config.CONTEXT, panos=utils.get_panos())


#------------------------------------------------#
# REST endpoints                                 #
#------------------------------------------------#


@app.route('/info/')
def info():
    """
    Route which returns all environment variables as a JSON object.
    """
    return flask.jsonify({'env': dict(os.environ)})


#------------------------------------------------#
# Supporting endpoints                           #
#------------------------------------------------#

@app.route('/static/<path:filepath>')
def serve_static(filepath):
    """
    Route for serving static assets directly, rather than using S3.
    Used for CSS, JS and other assets needed for the application.
    """
    return flask.send_from_directory(config.STATIC_ROOT, filepath)


#------------------------------------------------#
#  Command line options                          #
#------------------------------------------------#

def run():
    app.run(processes=3, host='0.0.0.0', port=8000, debug=True)


if __name__ == '__main__':
    run()

