import os
import shutil
from pathlib import Path

whisper_cpp_path = Path(os.environ.get("WHISPER_CPP_PATH", "~/build/whisper.cpp")).expanduser()
whisper_cpp_model_path = whisper_cpp_path / "models" / "ggml-medium.bin"
whisper_cpp_main = whisper_cpp_path / "main"
demucs_python = Path(os.environ.get("DEMUCS_PYTHON", "~/envs/demucs/bin/python")).expanduser()
demucs_path = Path(os.environ.get("DEMUCS_PATH", "~/build/demucs")).expanduser()
yt_dlp = shutil.which("yt-dlp")
ffmpeg = shutil.which("ffmpeg")
cache_path = Path("./cache")
cache_path.mkdir(exist_ok=True, parents=True)
proc_path = cache_path / "proc"
proc_path.mkdir(exist_ok=True, parents=True)
demucs_cache_path = cache_path / "demucs"
demucs_model = "htdemucs"

assert whisper_cpp_main.is_file()
assert demucs_python.is_file()
assert yt_dlp
assert ffmpeg
