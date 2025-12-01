import argparse

from baraoke.job import Job
from baraoke.play import play


def main():
    ap = argparse.ArgumentParser(prog="baraoke")
    ap.add_argument("youtube_id")
    ap.add_argument("--language", "-l", default="auto")
    args = ap.parse_args()
    job = Job(id=args.youtube_id, language=args.language)
    job.prepare()
    try:
        play(job)
    except ImportError as ie:
        raise RuntimeError("Make sure pygame is installed to use the baraoke player.") from ie


if __name__ == "__main__":
    main()
