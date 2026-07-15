"""
run_server.py — Launch the Street Vendor Digitalization Agent
Usage:  python run_server.py
"""
import os
import sys
import socket
import subprocess

# Force UTF-8 for Windows terminal
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def find_free_port(preferred: int = 8000) -> int:
    """Return preferred port if free, otherwise find next available port."""
    for port in range(preferred, preferred + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return preferred  # fallback


port = find_free_port(8000)

print("=" * 52)
print("  Street Vendor Digitalization Agent")
print("  AICTE-IBM SkillsBuild Internship 2026 - PS 29")
print("=" * 52)
print()
print("  Generation : meta-llama/llama-3-3-70b-instruct")
print("  Embeddings : intfloat/multilingual-e5-large")
print()
print(f"  Server     : http://localhost:{port}")
print(f"  Agent      : http://localhost:{port}/agent")
print(f"  API Docs   : http://localhost:{port}/docs")
print()
print("  Press Ctrl+C to stop.")
print()

subprocess.run([
    sys.executable, "-m", "uvicorn",
    "backend.main:app",
    "--reload",
    "--port", str(port),
    "--host", "127.0.0.1",
    "--log-level", "info",
])
