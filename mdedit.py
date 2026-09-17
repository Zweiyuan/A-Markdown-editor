from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import webview


APP_NAME = "mdedit"
MARKDOWN_TYPES = ("Markdown (*.md;*.markdown;*.txt)", "All files (*.*)")


def resource_path(name: str) -> Path:
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base_path / name


def read_document(path: Path) -> dict[str, Any]:
    try:
        content = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        content = path.read_text(encoding="gb18030")
    return {"content": content, "name": path.name, "path": str(path)}


class Api:
    def __init__(self, initial_path: Path | None = None) -> None:
        self._window: webview.Window | None = None
        self._current_path = initial_path

    def get_initial_document(self) -> dict[str, Any] | None:
        if self._current_path is None:
            return None
        try:
            return read_document(self._current_path)
        except OSError as error:
            return {"error": str(error)}

    def new_document(self) -> None:
        self._current_path = None
        if self._window is not None:
            self._window.set_title(f"未命名.md - {APP_NAME}")

    def open_file(self) -> dict[str, Any] | None:
        if self._window is None:
            return {"error": "窗口尚未准备完成"}
        selected = self._window.create_file_dialog(
            webview.FileDialog.OPEN,
            allow_multiple=False,
            file_types=MARKDOWN_TYPES,
        )
        if not selected:
            return None
        try:
            self._current_path = Path(selected[0])
            document = read_document(self._current_path)
            self._window.set_title(f"{self._current_path.name} - {APP_NAME}")
            return document
        except OSError as error:
            return {"error": str(error)}

    def save_file(
        self, content: str, save_as: bool, suggested_name: str
    ) -> dict[str, Any] | None:
        if self._window is None:
            return {"error": "窗口尚未准备完成"}
        if save_as or self._current_path is None:
            selected = self._window.create_file_dialog(
                webview.FileDialog.SAVE,
                save_filename=suggested_name or "未命名.md",
                file_types=MARKDOWN_TYPES,
            )
            if not selected:
                return None
            self._current_path = Path(selected[0])
            if not self._current_path.suffix:
                self._current_path = self._current_path.with_suffix(".md")
        try:
            self._current_path.write_text(content, encoding="utf-8")
            self._window.set_title(f"{self._current_path.name} - {APP_NAME}")
            return {"name": self._current_path.name, "path": str(self._current_path)}
        except OSError as error:
            return {"error": str(error)}


def command_line_document() -> Path | None:
    if len(sys.argv) < 2:
        return None
    candidate = Path(sys.argv[1]).expanduser().resolve()
    if candidate.is_file() and candidate.suffix.lower() in {".md", ".markdown", ".txt"}:
        return candidate
    return None


def main() -> None:
    initial_path = command_line_document()
    api = Api(initial_path)
    title = f"{initial_path.name if initial_path else '未命名.md'} - {APP_NAME}"
    window = webview.create_window(
        title,
        resource_path("mdedit.html").as_uri(),
        js_api=api,
        width=1200,
        height=780,
        min_size=(720, 480),
        text_select=True,
    )
    api._window = window
    webview.start(gui="edgechromium", debug=False, private_mode=False)


if __name__ == "__main__":
    main()