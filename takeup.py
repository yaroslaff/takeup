#!/usr/bin/python3

import os
import time
import datetime
import json
import logging

from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/",methods=['GET'])
def index():
    return "TakeUp server"

@app.route('/', methods=['POST'])
def submit():
    global count
    # check if the post request has the file part
    if 'package' not in request.files:
        return "No file"

    # if user does not select file, browser also
    # submit a empty part without filename

    # print(request.form["aaa"])

    upname = 'u{}.p{}.c{}'.format(started, os.getpid(), count)
    log.info("process {}".format(upname))
    count += 1

    uptmpdir = os.path.join(tmpdir, upname)
    upnewdir = os.path.join(newdir, upname)
    os.mkdir(uptmpdir)


    files = dict()
    for field, file in request.files.items():

        filename = secure_filename(file.filename)
        if file.filename == '':
            return 'No filename'

        file.save(os.path.join(uptmpdir, filename))
        files[field] = filename


    meta = dict()
    meta['ip'] = request.remote_addr
    meta['unixtime'] = int(time.time())
    meta['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    meta['files'] = files

    with open(os.path.join(uptmpdir,"_meta.json"),"w") as f:
        json.dump(meta, f, indent=4)

    with open(os.path.join(uptmpdir,"_fields.json"),"w") as f:
        json.dump(dict(request.form), f, indent=4)

    os.rename(uptmpdir, upnewdir)
    log.info("accepted {} from {}".format(upnewdir, request.remote_addr))
    return "OK"

#def application(env, start_response):
#    start_response('200 OK', [('Content-Type','text/html')])
#    return [b"Hello World"]

def startup():
    global tmpdir, newdir, started, count, log

    print ("starting up...")

    # app.config.from_envvar('TAKEUP_SETTINGS')

    updir = os.getenv("UPDIR",'/tmp')
    logfile = os.getenv("LOGFILE",'/tmp/takeup.log')

    print("up dir: {}".format(updir))
    print("logfile : {}".format(logfile))

    log = logging.getLogger()
    log.setLevel(logging.INFO)
    fh = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    log.addHandler(fh)
    log.info("TakeUp started")

    print("uid: {}".format(os.getuid()))

    tmpdir = os.path.join(updir, "tmp")
    newdir = os.path.join(updir, "new")
    started = int(time.time())
    count = 0


    if not os.path.exists(updir):
        os.mkdir(updir)

    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)

    if not os.path.exists(newdir):
        os.mkdir(newdir)

startup()

