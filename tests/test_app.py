from operator import itemgetter
from pathlib import Path

import pytest
from werkzeug.exceptions import BadRequest

from app import walktree


def check_dummy_folder(stats):
    assert stats and len(stats) == 3
    # ensure list content will always be in same order, which is not a guarantee of Path.iterdir()
    stats.sort(key=itemgetter("name"))

    assert stats[0]["name"] == "dummy"
    assert stats[0]["type"] == "FILE"
    assert stats[0].get("content") is None
    assert "props" in stats[0]

    assert stats[1]["name"] == "empty_folder"
    assert stats[1]["type"] == "DIR"
    assert stats[1].get("props") is None

    assert stats[2]["name"] == "other_folder"
    assert stats[2]["type"] == "DIR"
    assert stats[2].get("props") is None


def test_one_level():
    rootdir = "./tests/dummy_folder"
    rootdir = Path(rootdir).resolve()
    stats = walktree(rootdir, 1)

    check_dummy_folder(stats)
    assert stats[1]["content"] is None
    assert stats[2]["content"] is None


def test_two_levels():
    rootdir = "./tests/dummy_folder"
    rootdir = Path(rootdir).resolve()
    stats = walktree(rootdir, 2)

    check_dummy_folder(stats)
    assert stats[1]["content"] == []
    assert len(stats[2]["content"]) == 2


def test_exception_path_not_found():
    rootdir = "./tests/unexistant_folder"
    rootdir = Path(rootdir).resolve()
    with pytest.raises(
        BadRequest, match=r"rootdir .+/tests/unexistant_folder doesn't exists"
    ):
        walktree(rootdir)
