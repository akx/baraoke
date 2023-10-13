import dataclasses
import json

from baraoke import config
from baraoke.processes import download_song, demucs_song, convert_vocals, transcribe_vocals, remux, find_silence_infos
from baraoke.whisper_json import WhisperJSON


@dataclasses.dataclass
class Job:
    def __init__(self, id: str, language: str):
        self.id = id
        self.language = language
        self.youtube_url = f"https://youtu.be/{id}"
        self.orig_wav_path = config.cache_path / f"{id}.wav"
        self.demucsed_path = config.demucs_cache_path / config.demucs_model / id
        self.vocal_input_path = config.proc_path / f"{id}.wav"
        self.whisper_json_path = config.proc_path / f"{id}.{language}.json"
        self.silence_infos_path = config.proc_path / f"{id}.silence_infos.json"
        self.remuxed_path = config.proc_path / f"{id}.remuxed.wav"
        self.remuxed_low_vox_path = config.proc_path / f"{id}.remuxed.low_vox.wav"

    def prepare(self):
        if not self.orig_wav_path.is_file():
            download_song(self.youtube_url, self.orig_wav_path)
        if not self.demucsed_path.is_dir():
            demucs_song(self.orig_wav_path)
        if not self.vocal_input_path.is_file():
            convert_vocals(self.demucsed_path, self.vocal_input_path)
        if not self.whisper_json_path.is_file():
            transcribe_vocals(self.vocal_input_path, self.whisper_json_path, self.language)
        if not self.remuxed_path.is_file():
            remux(self.demucsed_path, self.remuxed_path, levels={"vocals.wav": 0.0})
        if not self.remuxed_low_vox_path.is_file():
            remux(self.demucsed_path, self.remuxed_low_vox_path, levels={"vocals.wav": 0.2})
        if not self.silence_infos_path.is_file():
            find_silence_infos(self.vocal_input_path, self.silence_infos_path)

    def read_whisper_json(self) -> WhisperJSON:
        return WhisperJSON(**json.loads(self.whisper_json_path.read_text()))

    def read_silence_infos_json(self) -> list[tuple[str, float]]:
        return json.loads(self.silence_infos_path.read_text())
