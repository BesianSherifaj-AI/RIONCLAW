#!/usr/bin/env python3
"""
Read-only dashboard viewer on http://localhost:8765/.
No mutations — every view reads a .md file and renders it.
Accessible from Windows browser at http://localhost:8765/.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import html
from lib.schema_config import ROOT, FILES

INDEX_TPL = """<!doctype html><meta charset=utf-8>
<title>openclaw_extension dashboard</title>
<style>
body{{font-family:system-ui;margin:2em;max-width:900px}}
h1{{color:#1864ab}} a{{color:#1864ab;text-decoration:none}}
.group{{margin:1em 0;padding:.8em;border-left:4px solid #1864ab;background:#f1f3f5}}
.file{{display:block;padding:.2em 0;font-family:ui-monospace,Menlo,monospace}}
</style>
<h1>openclaw_extension dashboard</h1>
<p>Read-only view over the active .md tree. Refresh to see changes.</p>
{body}
"""

VIEW_TPL = """<!doctype html><meta charset=utf-8>
<title>{title}</title>
<style>
body{{font-family:ui-monospace,Menlo,monospace;margin:2em;max-width:1100px;
     white-space:pre-wrap;font-size:13px;line-height:1.5}}
h1{{font-family:system-ui;color:#1864ab}}
a{{color:#1864ab}}
.back{{font-family:system-ui;font-size:14px}}
</style>
<p class=back><a href='/'>&larr; back</a></p>
<h1>{title}</h1>
<div>{body}</div>
"""

class H(BaseHTTPRequestHandler):
    def log_message(self, *a, **k): pass

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            self._index(); return
        if u.path.startswith("/view/"):
            self._view(u.path[len("/view/"):]); return
        self.send_response(404); self.end_headers()
        self.wfile.write(b"not found")

    def _index(self):
        groups = {}
        for f in FILES:
            top = f.split("/", 1)[0]
            groups.setdefault(top, []).append(f)
        parts = []
        for top, fs in sorted(groups.items()):
            links = "".join(
                f'<a class=file href="/view/{html.escape(f)}">{html.escape(f)}</a>'
                for f in sorted(fs)
            )
            parts.append(f'<div class=group><b>{html.escape(top)}</b>{links}</div>')
        html_body = INDEX_TPL.format(body="".join(parts))
        self.send_response(200); self.send_header("content-type", "text/html; charset=utf-8"); self.end_headers()
        self.wfile.write(html_body.encode())

    def _view(self, rel):
        p = (ROOT / rel).resolve()
        try:
            p.relative_to(ROOT)
        except ValueError:
            self.send_response(403); self.end_headers(); return
        if not p.exists():
            self.send_response(404); self.end_headers(); return
        body = html.escape(p.read_text(encoding="utf-8"))
        h = VIEW_TPL.format(title=html.escape(rel), body=body)
        self.send_response(200); self.send_header("content-type","text/html; charset=utf-8"); self.end_headers()
        self.wfile.write(h.encode())

if __name__ == "__main__":
    port = 8765
    print(f"dashboard on http://localhost:{port}/  (Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", port), H).serve_forever()
