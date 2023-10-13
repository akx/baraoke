from pydantic import Field
from pydantic.dataclasses import dataclass
from typing import List


@dataclass
class Audio:
    ctx: int
    state: int
    head: int
    layer: int


@dataclass
class Model:
    type: str
    multilingual: bool
    vocab: int
    audio: Audio
    text: Audio
    mels: int
    ftype: int


@dataclass
class Params:
    model: str
    language: str
    translate: bool


@dataclass
class Result:
    language: str


@dataclass
class Timestamp:
    to: str
    from_: str = Field(alias="from")


@dataclass
class Offset:
    to: int
    from_: int = Field(alias="from")


@dataclass
class Token:
    text: str
    p: float
    timestamps: Timestamp | None = None
    offsets: Offset | None = None


@dataclass
class Transcription:
    timestamps: Timestamp
    offsets: Offset
    text: str
    tokens: List[Token]


@dataclass
class WhisperJSON:
    systeminfo: str
    model: Model
    params: Params
    result: Result
    transcription: List[Transcription]
