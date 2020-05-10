import os
import stat
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[os.getenv('FRONT_URL', '')], supports_credentials=True)


@app.route("/")
def hello_world():
    return 'Hello, please go visit "/stat"'


@app.route("/stat")
def pathstats():
    rootdir = request.args.get("rootdir", os.getcwd())
    maxlevel = int(request.args.get("maxlevel", 1))
    # TODO validation that given rootdir only gives access to permitted directories
    # for that you can probably just use pathlib's .parents or .relative_to(),
    # but don't forget to call .resolve() first on rootdir to prevent relative path abuse
    stats = walktree(rootdir, maxlevel)
    return jsonify(stats)


def walktree(rootdir, maxlevel=None):
    if maxlevel is not None:
        if maxlevel <= 0:
            return None
        maxlevel -= 1

    dirstats = {}
    for f in os.listdir(rootdir):
        pathname = os.path.join(rootdir, f)
        mode = os.stat(pathname).st_mode
        if stat.S_ISDIR(mode):
            dirstats[f] = walktree(pathname, maxlevel)
        elif stat.S_ISREG(mode):
            dirstats[f] = filestats(pathname)
    return dirstats


def filestats(filepath):
    stats = os.stat(filepath)
    return {
        prop: getattr(stats, prop)
        for prop in dir(stats)
        if prop.startswith("st_")
    }


if __name__ == "__main__":
    rootdir = sys.argv[1] if len(sys.argv) == 2 else "."
    from pprint import pprint as pp

    pp(walktree(rootdir, 2))
