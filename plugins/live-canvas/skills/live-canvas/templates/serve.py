#!/usr/bin/env python3
"""Lightweight dev server for Live Canvas — static files + canvas JSON API."""

import json
import os
import re
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path

PORT = int(os.environ.get("PORT", 8888))

# Always serve static files relative to this script's directory,
# regardless of where the process was launched from.
os.chdir(Path(__file__).parent)

CANVASES_DIR = Path(__file__).parent / "canvases"
CANVASES_DIR.mkdir(exist_ok=True)

# Only allow safe canvas names (alphanumeric, hyphens, underscores)
SAFE_NAME = re.compile(r"^[a-zA-Z0-9_-]+$")

# Allowed file extensions for token updates
TOKEN_FILE_EXTENSIONS = {".css", ".scss", ".less", ".json", ".js", ".ts", ".yaml", ".yml"}

# Image file extensions (served as binary with correct Content-Type)
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".bmp"}

# Video file extensions (served with Range request support)
VIDEO_EXTENSIONS = {".mov", ".mp4", ".webm", ".ogg", ".m4v", ".avi"}

# Audio file extensions (served with Range request support)
AUDIO_EXTENSIONS = {".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg"}

# Text file extensions that can be read/written via the file API
TEXT_FILE_EXTENSIONS = TOKEN_FILE_EXTENSIONS | {
    ".md", ".txt", ".html", ".jsx", ".tsx", ".py", ".rb", ".go",
    ".rs", ".toml", ".xml", ".sh", ".bash", ".zsh", ".env",
    ".gitignore", ".sql", ".graphql", ".prisma", ".svelte",
    ".vue", ".astro", ".mdx",
}

# Content-Type mapping for binary extensions
CONTENT_TYPE_MAP = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".svg": "image/svg+xml", ".webp": "image/webp",
    ".ico": "image/x-icon", ".bmp": "image/bmp",
    ".mov": "video/quicktime", ".mp4": "video/mp4", ".webm": "video/webm",
    ".ogg": "video/ogg", ".m4v": "video/x-m4v", ".avi": "video/x-msvideo",
    ".mp3": "audio/mpeg", ".wav": "audio/wav", ".aac": "audio/aac",
    ".m4a": "audio/mp4", ".flac": "audio/flac",
}

def _normalize_path(path: str) -> str:
    """Normalize user-supplied file paths to handle common paste quirks."""
    if not path:
        return path
    path = path.strip()
    # Strip wrapping quotes (macOS Cmd+Option+C adds them)
    if len(path) >= 2 and path[0] == path[-1] and path[0] in ("'", '"'):
        path = path[1:-1]
    # Strip file:// URL prefix (Finder drag, some apps)
    if path.startswith("file://"):
        path = path[7:]  # file:///Users/... → /Users/...
    # Expand ~ to home directory
    path = os.path.expanduser(path)
    # If file not found, try normalizing Unicode spaces (macOS uses U+202F
    # narrow no-break space and U+00A0 non-breaking space in screenshot
    # filenames before AM/PM — but users paste regular spaces)
    if not os.path.isfile(path):
        normalized = path.replace("\u202f", " ").replace("\u00a0", " ")
        if normalized != path and os.path.isfile(normalized):
            return normalized
        # Reverse: user pasted regular space but file has Unicode space
        for uchar in ("\u202f", "\u00a0"):
            for variant in _space_variants(path, uchar):
                if os.path.isfile(variant):
                    return variant
    return path


def _space_variants(path: str, uchar: str):
    """Try replacing spaces adjacent to AM/PM with a Unicode space."""
    import re
    # Replace the space right before AM/PM with the Unicode variant
    return [re.sub(r" (?=[AP]M)", uchar, path)]

# Regex to match a CSS custom property declaration: --name: value;
TOKEN_PATTERN = re.compile(r"(--{name}\s*:\s*)[^;]+(;)")


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/canvases":
            canvases = []
            for f in sorted(CANVASES_DIR.glob("*.json")):
                try:
                    data = json.loads(f.read_text())
                    canvases.append({"id": f.stem, "name": data.get("name", f.stem)})
                except (json.JSONDecodeError, OSError):
                    continue
            self._json_response(200, canvases)
        elif self.path.startswith("/api/canvases/"):
            name = self.path.split("/api/canvases/", 1)[1]
            if not SAFE_NAME.match(name):
                self._json_response(400, {"error": "invalid canvas name"})
                return
            path = CANVASES_DIR / f"{name}.json"
            if not path.exists():
                self._json_response(404, {"error": "not found"})
                return
            self._json_response(200, json.loads(path.read_text()))
        elif self.path.startswith("/api/file?"):
            self._handle_file_serve()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/tokens/read":
            self._handle_token_read()
        elif self.path == "/api/tokens":
            self._handle_token_update()
        elif self.path == "/api/file/read":
            self._handle_file_read()
        elif self.path == "/api/file":
            self._handle_file_write()
        elif self.path.startswith("/api/canvases/"):
            name = self.path.split("/api/canvases/", 1)[1]
            if not SAFE_NAME.match(name):
                self._json_response(400, {"error": "invalid canvas name"})
                return
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self._json_response(400, {"error": "invalid JSON"})
                return
            (CANVASES_DIR / f"{name}.json").write_text(
                json.dumps(data, indent=2) + "\n"
            )
            self._json_response(200, {"ok": True})
        else:
            self._json_response(404, {"error": "not found"})

    def _handle_token_read(self):
        """Read current token values from a CSS source file."""
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._json_response(400, {"error": "invalid JSON"})
            return

        source = data.get("source")
        names = data.get("names")

        if not source or not isinstance(names, list) or len(names) == 0:
            self._json_response(400, {"error": "missing 'source' or 'names' fields"})
            return

        filepath = Path(_normalize_path(source))

        if filepath.suffix not in TOKEN_FILE_EXTENSIONS:
            self._json_response(422, {
                "error": f"unrecognized file extension '{filepath.suffix}'",
                "allowed": sorted(TOKEN_FILE_EXTENSIONS),
            })
            return

        if not filepath.is_file():
            self._json_response(404, {"error": f"file not found: {source}"})
            return

        try:
            content = filepath.read_text()
        except OSError as exc:
            self._json_response(500, {"error": f"read error: {exc}"})
            return

        tokens = {}
        for name in names:
            if not name:
                continue
            escaped_name = re.escape(name.lstrip("-"))
            pattern = re.compile(
                re.escape("--") + escaped_name + r"\s*:\s*([^;]+);"
            )
            match = pattern.search(content)
            if match:
                tokens[name] = match.group(1).strip()

        self._json_response(200, {"ok": True, "tokens": tokens, "file": str(filepath)})

    def _handle_token_update(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._json_response(400, {"error": "invalid JSON"})
            return

        source = data.get("source")
        changes = data.get("changes")

        if not source or not isinstance(changes, list) or len(changes) == 0:
            self._json_response(400, {"error": "missing 'source' or 'changes' fields"})
            return

        filepath = Path(source)

        if filepath.suffix not in TOKEN_FILE_EXTENSIONS:
            self._json_response(422, {
                "error": f"unrecognized file extension '{filepath.suffix}'",
                "allowed": sorted(TOKEN_FILE_EXTENSIONS),
            })
            return

        if not filepath.is_file():
            self._json_response(404, {"error": f"file not found: {source}"})
            return

        try:
            content = filepath.read_text()
        except OSError as exc:
            self._json_response(500, {"error": f"read error: {exc}"})
            return

        updated = 0
        for change in changes:
            name = change.get("name", "")
            value = change.get("value", "")
            if not name:
                continue
            # Escape the token name for use in regex, then build the pattern
            escaped_name = re.escape(name.lstrip("-"))
            pattern = re.compile(
                r"(" + re.escape("--") + escaped_name + r"\s*:\s*)[^;]+(;)"
            )
            new_content, count = pattern.subn(r"\g<1>" + value + r"\2", content)
            if count > 0:
                content = new_content
                updated += count

        try:
            filepath.write_text(content)
        except OSError as exc:
            self._json_response(500, {"error": f"write error: {exc}"})
            return

        self._json_response(200, {"ok": True, "updated": updated, "file": str(filepath)})

    def _handle_file_serve(self):
        """Serve an allowed file by absolute path with correct Content-Type."""
        import traceback
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        file_path = params.get("path", [None])[0]

        if not file_path:
            self._json_response(400, {"error": "missing 'path' query parameter"})
            return

        filepath = Path(_normalize_path(file_path))

        allowed_extensions = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS | AUDIO_EXTENSIONS | TEXT_FILE_EXTENSIONS

        if filepath.suffix.lower() not in allowed_extensions:
            self._json_response(422, {
                "error": f"unrecognized file extension '{filepath.suffix}'",
                "allowed": sorted(allowed_extensions),
            })
            return

        if not filepath.is_file():
            self._json_response(404, {"error": f"file not found: {file_path}"})
            return

        try:
            if filepath.suffix.lower() in VIDEO_EXTENSIONS | AUDIO_EXTENSIONS:
                self._serve_video(filepath)
            elif filepath.suffix.lower() in IMAGE_EXTENSIONS:
                content_type = CONTENT_TYPE_MAP.get(filepath.suffix.lower(), "application/octet-stream")
                data = filepath.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)
            else:
                content = filepath.read_text(encoding="utf-8")
                body = content.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
        except PermissionError as exc:
            print(f"[file-serve] PERMISSION DENIED: {filepath}")
            self._json_response(403, {
                "error": f"Permission denied: {filepath.name}",
                "hint": "Grant Full Disk Access to your terminal app in System Settings > Privacy & Security",
            })
        except Exception as exc:
            print(f"[file-serve] ERROR: {type(exc).__name__}: {exc}")
            traceback.print_exc()
            self._json_response(500, {"error": f"read error: {exc}"})

    def _serve_video(self, filepath: Path):
        """Serve a video file with HTTP Range request support for seeking."""
        content_type = CONTENT_TYPE_MAP.get(filepath.suffix.lower(), "application/octet-stream")
        file_size = filepath.stat().st_size
        range_header = self.headers.get("Range")

        if range_header:
            # Parse "bytes=START-END" (END is optional)
            range_spec = range_header.replace("bytes=", "")
            parts = range_spec.split("-")
            start = int(parts[0]) if parts[0] else 0
            end = int(parts[1]) if parts[1] else file_size - 1
            end = min(end, file_size - 1)
            length = end - start + 1

            self.send_response(206)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(length))
            self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            with open(filepath, "rb") as f:
                f.seek(start)
                remaining = length
                while remaining > 0:
                    chunk = f.read(min(remaining, 64 * 1024))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
        else:
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(file_size))
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            with open(filepath, "rb") as f:
                while True:
                    chunk = f.read(64 * 1024)
                    if not chunk:
                        break
                    self.wfile.write(chunk)

    def _handle_file_read(self):
        """Read full text content of a file."""
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._json_response(400, {"error": "invalid JSON"})
            return

        source = data.get("source")
        if not source:
            self._json_response(400, {"error": "missing 'source' field"})
            return

        filepath = Path(_normalize_path(source))

        if filepath.suffix.lower() not in TEXT_FILE_EXTENSIONS:
            self._json_response(422, {
                "error": f"unrecognized file extension '{filepath.suffix}'",
                "allowed": sorted(TEXT_FILE_EXTENSIONS),
            })
            return

        if not filepath.is_file():
            self._json_response(404, {"error": f"file not found: {source}"})
            return

        try:
            content = filepath.read_text(encoding="utf-8")
        except OSError as exc:
            self._json_response(500, {"error": f"read error: {exc}"})
            return

        self._json_response(200, {"ok": True, "content": content, "file": str(filepath)})

    def _handle_file_write(self):
        """Write text content to an existing file."""
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._json_response(400, {"error": "invalid JSON"})
            return

        source = data.get("source")
        content = data.get("content")

        if not source:
            self._json_response(400, {"error": "missing 'source' field"})
            return

        if content is None:
            self._json_response(400, {"error": "missing 'content' field"})
            return

        filepath = Path(_normalize_path(source))

        if filepath.suffix.lower() not in TEXT_FILE_EXTENSIONS:
            self._json_response(422, {
                "error": f"unrecognized file extension '{filepath.suffix}'",
                "allowed": sorted(TEXT_FILE_EXTENSIONS),
            })
            return

        if not filepath.is_file():
            self._json_response(404, {"error": f"file not found: {source}"})
            return

        try:
            filepath.write_text(content, encoding="utf-8")
        except OSError as exc:
            self._json_response(500, {"error": f"write error: {exc}"})
            return

        self._json_response(200, {"ok": True, "file": str(filepath)})

    def do_DELETE(self):
        if self.path.startswith("/api/canvases/"):
            name = self.path.split("/api/canvases/", 1)[1]
            if not SAFE_NAME.match(name):
                self._json_response(400, {"error": "invalid canvas name"})
                return
            path = CANVASES_DIR / f"{name}.json"
            if path.exists():
                path.unlink()
            self._json_response(200, {"ok": True})
        else:
            self._json_response(404, {"error": "not found"})

    def _json_response(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, fmt, *args):
        # Quieter logs — only non-200 or API calls
        if args and (str(args[1]) != "200" or "/api/" in str(args[0])):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    print(f"Serving on http://localhost:{PORT}")
    HTTPServer(("", PORT), Handler).serve_forever()
