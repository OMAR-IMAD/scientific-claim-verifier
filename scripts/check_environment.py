"""Print local environment details needed before model training."""

from __future__ import annotations

import platform
import shutil
import subprocess
import sys


def command_output(command: list[str]) -> str:
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
        output = (completed.stdout or completed.stderr).strip()
        return output if output else "No output"
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return f"Unavailable: {exc}"


def main() -> None:
    print("=== Scientific Claim Verifier: Environment Check ===")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Executable: {sys.executable}")
    print(f"Operating system: {platform.platform()}")
    print(f"Machine architecture: {platform.machine()}")
    print(f"Git path: {shutil.which('git') or 'Not found'}")
    print(f"NVIDIA SMI path: {shutil.which('nvidia-smi') or 'Not found'}")

    if shutil.which("nvidia-smi"):
        print("\n=== NVIDIA GPU ===")
        print(command_output([
            "nvidia-smi",
            "--query-gpu=name,memory.total,driver_version",
            "--format=csv,noheader",
        ]))

    try:
        import torch
        print("\n=== PyTorch ===")
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
    except ImportError:
        print("\nPyTorch: Not installed yet (expected at this stage).")


if __name__ == "__main__":
    main()
