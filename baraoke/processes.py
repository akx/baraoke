import json
import re
import subprocess

from baraoke import config

silence_info_re = re.compile("silence_(start|end): ([0-9.]+)")


def download_song(url, orig_wav_path):
    subprocess.check_call(
        [
            config.yt_dlp,
            "-x",
            "--audio-format=wav",
            "-o",
            str(orig_wav_path),
            url,
        ]
    )


def demucs_song(orig_wav_path):
    subprocess.check_call(
        [
            config.demucs_python,
            "-m",
            "demucs",
            "-d",
            "mps",
            "-o",
            config.demucs_cache_path,
            orig_wav_path,
        ]
    )


def remux(demucsed_path, remuxed_path, *, levels: dict[str, float]):
    sources = [p for p in demucsed_path.glob("*.wav")]
    inputs = []
    weights = []
    for input in sources:
        inputs.extend(["-i", input])
        weights.append(str(levels.get(input.name, 1.0)))
    weights_str = " ".join(weights)
    print(inputs, weights)
    subprocess.check_call(
        [
            config.ffmpeg,
            "-hide_banner",
            *inputs,
            "-filter_complex",
            f"amix=inputs={len(sources)}:duration=longest:weights={weights_str}",
            remuxed_path,
        ]
    )


def convert_vocals(demucsed_path, vocal_input_path):
    subprocess.check_call(
        [
            config.ffmpeg,
            "-hide_banner",
            "-i",
            demucsed_path / "vocals.wav",
            "-ar",
            "16k",
            "-ac",
            "1",
            vocal_input_path,
        ]
    )


def find_silence_infos(vocal_input_path, silence_infos_json_path):
    result = subprocess.run(
        [
            config.ffmpeg,
            "-hide_banner",
            "-i",
            vocal_input_path,
            "-af",
            "silencedetect=noise=-30dB:d=0.5",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    silence_infos = []
    for line in result.stderr.splitlines():
        match = silence_info_re.search(line)
        if match:
            silence_infos.append((match.group(1), float(match.group(2))))
    silence_infos_json_path.write_text(json.dumps(silence_infos))


def transcribe_vocals(vocal_input_path, json_path, language):
    subprocess.check_call(
        [
            config.whisper_cpp_main,
            "-m",
            config.whisper_cpp_model_path,
            "-of",
            json_path.with_suffix(""),
            "-pc",
            "-pp",
            "-ps",
            "-ocsv",
            "-oj",
            "-ojf",
            "-olrc",
            "-osrt",
            "-otxt",
            "-ovtt",
            "-l",
            language,
            vocal_input_path,
        ]
    )
