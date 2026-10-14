"""Local web server for the live viewer (architecture/13). Display only; Python standard library.

Usage (from Simulations/BLA/simulation), in its own terminal, while runs are going:
    python -m bla_sim.viewer_server            # http://localhost:8765, this laptop only
    python -m bla_sim.viewer_server --lan      # also other devices on the home network
                                               # (Windows Firewall asks once)
Serves viewer/index.html and, read-only, the live/ snapshots of every broadcasting run:
    /api/runs                          live runs (status.json of each) + launcher status files
    /api/cells?run=<block_dir>/seed<k>
    /api/status?run=...
    /api/chunks?run=...&from=a&to=b    chunks a..b that still exist (at most 400)
It never writes anything and never talks to the simulation.
"""
import argparse
import json
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .nrn import OUTPUT_DIR, SIM_DIR

PAGE = SIM_DIR / "viewer" / "index.html"
RUN_RE = re.compile(r"^[A-Za-z0-9_.]+/seed\d+$")
MAX_CHUNKS = 400


def _read(path):
    for _ in range(3):                      # the run may be renaming the file right now
        try:
            return path.read_bytes()
        except (PermissionError, FileNotFoundError):
            time.sleep(0.02)
    return None


def live_dir(run):
    if not run or not RUN_RE.match(run):
        return None
    d = (OUTPUT_DIR / run / "live").resolve()
    return d if d.is_dir() and OUTPUT_DIR.resolve() in d.parents else None


def list_runs():
    runs = []
    for st in OUTPUT_DIR.glob("*/seed*/live/status.json"):
        raw = _read(st)
        if raw:
            try:
                s = json.loads(raw)
            except ValueError:
                continue
            s["age_s"] = time.time() - s.get("updated", 0)
            runs.append(s)
    runs.sort(key=lambda s: (s.get("done", False), s["age_s"] > 600, s.get("run", "")))
    launch = {}
    for f in (OUTPUT_DIR / "launcher").glob("*_status.json"):
        raw = _read(f)
        if raw:
            try:
                launch[f.stem] = json.loads(raw)
            except ValueError:
                pass
    return {"runs": runs, "launcher": launch, "now": time.time()}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, separators=(",", ":")).encode())

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        if u.path in ("/", "/index.html"):
            body = _read(PAGE)
            return self._send(200, body, "text/html; charset=utf-8") if body else self._json({"error": "no page"}, 500)
        if u.path == "/api/runs":
            return self._json(list_runs())
        d = live_dir(q.get("run"))
        if u.path in ("/api/cells", "/api/status"):
            raw = _read(d / (u.path[5:] + ".json")) if d else None
            return self._send(200, raw) if raw else self._json({"error": "not found"}, 404)
        if u.path == "/api/chunks":
            if not d:
                return self._json({"error": "not found"}, 404)
            try:
                a, b = int(q.get("from", 1)), int(q.get("to", 1))
            except ValueError:
                return self._json({"error": "bad range"}, 400)
            a = max(a, b - MAX_CHUNKS + 1, 1)
            parts = []
            for k in range(a, b + 1):
                raw = _read(d / f"chunk_{k}.json")
                if raw:
                    parts.append(raw)
            return self._send(200, b'{"chunks":[' + b",".join(parts) + b"]}")
        self._json({"error": "not found"}, 404)

    def log_message(self, *a):          # keep the terminal quiet
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--lan", action="store_true", help="allow other devices on the home network")
    args = ap.parse_args()
    host = "0.0.0.0" if args.lan else "127.0.0.1"
    srv = ThreadingHTTPServer((host, args.port), Handler)
    print(f"Live viewer: http://localhost:{args.port}  (Ctrl+C to stop; runs are not affected)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
