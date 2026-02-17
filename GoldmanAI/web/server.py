"""Minimal web frontend/backend for Goldman AI with Terms of Service page."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from GoldmanAI.engine.pipeline import GoldmanPipeline
from GoldmanAI.safety.filter import SafeGenerationError
from GoldmanAI.utils.loader import prepare_environment

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
ALLOWED_DURATIONS = {6, 10, 15, 20}


class GoldmanWebHandler(BaseHTTPRequestHandler):
    """Serves frontend pages and JSON generation endpoint."""

    pipeline = GoldmanPipeline(prepare_environment())

    def _serve_html(self, name: str) -> None:
        path = TEMPLATES_DIR / name
        if not path.exists():
            self.send_error(HTTPStatus.NOT_FOUND, "Page not found")
            return
        payload = path.read_text(encoding="utf-8").encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _serve_static(self, relative_path: str) -> None:
        path = (STATIC_DIR / relative_path).resolve()
        if STATIC_DIR.resolve() not in path.parents or not path.exists() or path.is_dir():
            self.send_error(HTTPStatus.NOT_FOUND, "Asset not found")
            return

        content_type = "text/plain; charset=utf-8"
        if path.suffix == ".css":
            content_type = "text/css; charset=utf-8"
        elif path.suffix == ".js":
            content_type = "application/javascript; charset=utf-8"

        payload = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _serve_media(self, filename: str) -> None:
        media_path = (self.pipeline.config.assets_output_dir / filename).resolve()
        output_root = self.pipeline.config.assets_output_dir.resolve()
        if output_root not in media_path.parents or not media_path.exists() or media_path.is_dir():
            self.send_error(HTTPStatus.NOT_FOUND, "Media not found")
            return

        content_type = "application/octet-stream"
        if media_path.suffix == ".mp4":
            content_type = "video/mp4"
        elif media_path.suffix == ".wav":
            content_type = "audio/wav"
        elif media_path.suffix == ".txt":
            content_type = "text/plain; charset=utf-8"

        payload = media_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Content-Disposition", f'inline; filename="{media_path.name}"')
        self.end_headers()
        self.wfile.write(payload)

    def _read_json(self) -> dict[str, Any] | None:
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length) if content_length else b"{}"
        try:
            return json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON payload."}, HTTPStatus.BAD_REQUEST)
            return None

    def send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._serve_html("index.html")
            return
        if parsed.path == "/terms":
            self._serve_html("terms.html")
            return
        if parsed.path.startswith("/static/"):
            self._serve_static(parsed.path.removeprefix("/static/"))
            return
        if parsed.path.startswith("/media/"):
            self._serve_media(parsed.path.removeprefix("/media/"))
            return
        if parsed.path == "/api/health":
            self.send_json({"status": "ok"})
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/api/generate":
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return

        data = self._read_json()
        if data is None:
            return

        prompt = str(data.get("prompt", "")).strip()
        source_image = str(data.get("source_image", "")).strip() or None
        parental_mode = bool(data.get("parental_education_mode", True))
        audio_enabled = bool(data.get("audio_enabled", True))
        multi_shot_enabled = bool(data.get("multi_shot_enabled", False))
        lip_sync_enabled = bool(data.get("lip_sync_enabled", False))
        lip_sync_focus = bool(data.get("lip_sync_focus", False))
        if lip_sync_focus and not lip_sync_enabled:
            lip_sync_enabled = True
        duration_seconds = int(data.get("duration_seconds", 10))

        if duration_seconds not in ALLOWED_DURATIONS:
            self.send_json({"error": "Duration must be one of: 6, 10, 15, 20 seconds."}, HTTPStatus.BAD_REQUEST)
            return

        self.pipeline.config.safety.parental_education_mode = parental_mode

        if not prompt:
            self.send_json({"error": "Prompt is required."}, HTTPStatus.BAD_REQUEST)
            return

        try:
            result = self.pipeline.safe_generate(
                prompt,
                source_image=source_image,
                duration_seconds=duration_seconds,
                audio_enabled=audio_enabled,
                multi_shot_enabled=multi_shot_enabled,
                lip_sync_enabled=lip_sync_enabled,
                lip_sync_focus=lip_sync_focus,
            )
        except SafeGenerationError as exc:
            self.send_json({"error": str(exc), "blocked": True}, HTTPStatus.FORBIDDEN)
            return
        except Exception as exc:  # pragma: no cover
            self.send_json({"error": f"Generation failed: {exc}"}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return

        audio_url = f"/media/{result.audio_path.name}" if result.audio_path else None
        self.send_json(
            {
                "video_path": str(result.video_path),
                "audio_path": str(result.audio_path) if result.audio_path else None,
                "mix_path": str(result.mix_path),
                "video_url": f"/media/{result.video_path.name}",
                "audio_url": audio_url,
                "mix_url": f"/media/{result.mix_path.name}",
                "duration_seconds": result.duration_seconds,
                "audio_enabled": result.audio_enabled,
                "multi_shot_enabled": result.multi_shot_enabled,
                "lip_sync_enabled": result.lip_sync_enabled,
                "lip_sync_focus": result.lip_sync_focus,
                "parsed_prompt": result.parsed_prompt,
                "using_gpu": self.pipeline.state.using_gpu,
            }
        )


def run_server(host: str = "0.0.0.0", port: int = 8080) -> None:
    server = ThreadingHTTPServer((host, port), GoldmanWebHandler)
    print(f"Goldman AI web server running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
