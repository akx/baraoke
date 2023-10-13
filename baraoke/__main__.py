import argparse

from baraoke.job import Job
from baraoke.play import play


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("youtube_id")
    ap.add_argument("--language", "-l", default="auto")
    args = ap.parse_args()
    job = Job(id=args.youtube_id, language=args.language)
    job.prepare()
    play(job)


if __name__ == "__main__":
    main()
