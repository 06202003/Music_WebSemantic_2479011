"""Convenience launcher for the FastAPI backend and Streamlit frontend."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def start_backend() -> subprocess.Popen[str]:
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload"],
        cwd=str(ROOT),
    )


def start_frontend() -> subprocess.Popen[str]:
    return subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/streamlit_app.py"],
        cwd=str(ROOT),
    )


def main() -> int:
    backend = start_backend()
    frontend = start_frontend()

    print("Backend:  http://localhost:8000")
    print("Frontend: http://localhost:8501")
    print("Press Ctrl+C to stop both processes.")

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        backend.terminate()
        frontend.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())