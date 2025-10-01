#!/usr/bin/env python3
"""Batch convert MP4 files to compressed MP3 files using ffmpeg."""

from __future__ import annotations

import argparse
import logging
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert every MP4 in the input folder to a compressed MP3 in the output folder."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("input mp4"),
        help="Folder containing .mp4 files to convert (default: ./input mp4)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output mp3"),
        help="Destination folder for converted .mp3 files (default: ./output mp3)",
    )
    parser.add_argument(
        "--bitrate",
        default="192k",
        help="Target audio bitrate for MP3 (e.g. 128k, 192k, 256k).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing MP3 files instead of skipping them.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search for MP4 files recursively inside the input directory.",
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=[".mp4", ".m4v", ".mov"],
        help="List of video file extensions to convert (default: .mp4 .m4v .mov).",
    )
    return parser.parse_args()


def ensure_ffmpeg_available() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            "ffmpeg is not installed or not found on PATH. "
            "Install it from https://ffmpeg.org/download.html and try again."
        )


def find_videos(directory: Path, extensions: Iterable[str], recursive: bool) -> Iterable[Path]:
    normalized_exts = {ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions}
    if recursive:
        yield from (
            path
            for path in directory.rglob("*")
            if path.is_file() and path.suffix.lower() in normalized_exts
        )
    else:
        yield from (
            path
            for path in directory.glob("*")
            if path.is_file() and path.suffix.lower() in normalized_exts
        )


def convert_video_to_mp3(
    source: Path,
    destination: Path,
    bitrate: str,
    overwrite: bool,
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists() and not overwrite:
        logging.info("Skipping %s (destination already exists)", destination.name)
        return

    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y" if overwrite else "-n",
        "-i",
        str(source),
        "-vn",
        "-acodec",
        "libmp3lame",
        "-b:a",
        bitrate,
        str(destination),
    ]

    logging.debug("Running command: %s", " ".join(command))

    try:
        subprocess.run(command, check=True)
        logging.info("Converted %s -> %s", source.name, destination.name)
    except subprocess.CalledProcessError as exc:
        logging.error("Failed to convert %s (exit code %s)", source, exc.returncode)
    except FileNotFoundError:
        logging.error("ffmpeg executable not found. Ensure it is installed and on PATH.")


def main() -> None:
    args = parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    ensure_ffmpeg_available()

    input_dir: Path = args.input_dir
    output_dir: Path = args.output_dir

    if not input_dir.exists() or not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory '{input_dir}' does not exist or is not a directory.")

    logging.info("Searching for video files in %s", input_dir)
    videos = list(find_videos(input_dir, args.extensions, args.recursive))

    if not videos:
        logging.warning("No matching video files found in %s", input_dir)
        return

    logging.info("Found %d video file(s) to convert", len(videos))

    total = len(videos)

    def render_progress(current: int) -> None:
        bar_width = 30
        filled = int(bar_width * current / total) if total else bar_width
        bar = "#" * filled + "-" * (bar_width - filled)
        sys.stdout.write(f"\r[{bar}] {current}/{total} files\n")
        sys.stdout.flush()

    for index, video in enumerate(videos, start=1):
        relative_path = video.relative_to(input_dir)
        destination = output_dir / relative_path.with_suffix(".mp3")
        convert_video_to_mp3(video, destination, args.bitrate, args.overwrite)
        render_progress(index)

    if total:
        sys.stdout.write("\n")

    logging.info("Conversion complete.")


if __name__ == "__main__":
    main()
