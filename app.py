import os
import stat
import sys
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
CORS(app, origins=[os.getenv("FRONT_URL", "")], supports_credentials=True)


@app.route("/")
def hello_world():
    return 'Hello, please go visit "/stat"'


@app.route("/stat")
def pathstats():
    rootdir = request.args.get("rootdir", Path.cwd())
    try:
        maxlevel = int(request.args.get("maxlevel", 1))
        assert maxlevel > 0
        # TODO validation that given rootdir only gives access to permitted directories
        # for that you can probably just use pathlib's .parents or .relative_to(),
        # but don't forget to call .resolve() first on rootdir to prevent relative path abuse
        rootdir = Path(rootdir).resolve()
        stats = walktree(rootdir, maxlevel)
        return jsonify({"name": str(rootdir), "type": "DIR", "content": stats})
    except (ValueError, AssertionError):  # maxlevel can't be converted to int
        raise BadRequest("maxlevel should be a positive int")


def walktree(rootdir, maxlevel=None):
    if maxlevel is not None:
        if maxlevel <= 0:
            return None
        maxlevel -= 1

    dirstats = []
    try:
        for f_path in rootdir.iterdir():
            if not f_path.exists():
                # prevent error by trying to read fd that doesn't exist anymore
                continue
            mode = f_path.stat().st_mode
            if stat.S_ISDIR(mode):
                dirstats.append(
                    {
                        "name": f_path.name,
                        "type": "DIR",
                        "content": walktree(f_path, maxlevel),
                    }
                )
            elif stat.S_ISREG(mode):
                dirstats.append(
                    {"name": f_path.name, "type": "FILE", "props": filestats(f_path)}
                )
        return dirstats
    except FileNotFoundError:
        raise BadRequest(f"rootdir {rootdir} doesn't exists")


def filestats(filepath):
    stats = filepath.stat()
    return {prop: getattr(stats, prop) for prop in dir(stats) if prop.startswith("st_")}


if __name__ == "__main__":
    rootdir = sys.argv[1] if len(sys.argv) == 2 else "."
    rootdir = Path(rootdir).resolve()
    from pprint import pprint as pp

    pp(walktree(rootdir, 2))
