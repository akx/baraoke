import os
import shutil
from pathlib import Path

whisper_cpp_path = Path(os.environ.get("WHISPER_CPP_PATH", "~/build/whisper.cpp")).expanduser()
whisper_cpp_model_path = whisper_cpp_path / "models" / "ggml-medium.bin"
for _alt in (
    whisper_cpp_path / "whisper-cli",
    whisper_cpp_path / "bin" / "whisper-cli",
    whisper_cpp_path / "build" / "bin" / "whisper-cli",
):
    if _alt.is_file():
        whisper_cli = _alt
        break
else:
    whisper_cli = None
yt_dlp = shutil.which("yt-dlp")
ffmpeg = shutil.which("ffmpeg")
cache_path = Path("./cache")
cache_path.mkdir(exist_ok=True, parents=True)
proc_path = cache_path / "proc"
proc_path.mkdir(exist_ok=True, parents=True)
demucs_cache_path = cache_path / "demucs"
demucs_model = "htdemucs"

assert whisper_cli and whisper_cli.is_file(), f"whisper-cli not found at {whisper_cli}"
assert yt_dlp, f"yt-dlp not found in PATH"
assert ffmpeg, f"ffmpeg not found in PATH"
