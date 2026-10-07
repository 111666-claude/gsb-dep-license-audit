"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "deny":
        out = core.audit({"root": []}, ["root"], {"root": "MIT"},
                         {"MIT"}, {"MIT"}, set(), core.Counter())
        _line({"violations": len(out)})
        return 0
    if name == "exception":
        out = core.audit({"root": []}, ["root"], {"root": "GPL"},
                         set(), {"GPL"}, {"root"}, core.Counter())
        _line({"violations": len(out)})
        return 0
    if name == "dupe":
        graph = {"root": ["a", "b"], "a": ["c"], "b": ["c"], "c": []}
        licenses = {"root": "MIT", "a": "MIT", "b": "MIT", "c": "GPL"}
        out = core.audit(graph, ["root"], licenses,
                         {"MIT"}, {"GPL"}, set(), core.Counter())
        _line({"violations": len(out)})
        return 0
    if name == "trim":
        out = core.audit({"root": []}, ["root"], {"root": " MIT "},
                         {"MIT"}, set(), set(), core.Counter())
        _line({"violations": len(out)})
        return 0
    if name == "work":
        graph = {}
        licenses = {}
        for i in range(800):
            graph["p%04d" % i] = ["p%04d" % (i + 1)] if i + 1 < 800 else []
            licenses["p%04d" % i] = "MIT"
        counter = core.Counter()
        core.audit(graph, ["p0000"], licenses, {"MIT"}, set(), set(), counter)
        _line({"packages": 800, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
