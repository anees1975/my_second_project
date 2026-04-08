"""youtubedn.py — Download YouTube audio as MP3 using yt-dlp."""

import argparse
import os
import sys

import yt_dlp

__all__ = ["download_mp3_with_ytdlp"]

_YOUTUBE_DOMAINS = ("youtube.com", "youtu.be", "www.youtube.com", "m.youtube.com")


def _validate_url(url: str) -> None:
    """Raise ValueError if *url* is empty or does not look like a YouTube URL."""
    if not url:
        raise ValueError("URL must not be empty.")
    if not any(domain in url for domain in _YOUTUBE_DOMAINS):
        raise ValueError(f"URL does not appear to be a YouTube link: {url!r}")


def _progress_hook(d: dict) -> None:
    """Print a one-line progress indicator to stdout."""
    if d["status"] == "downloading":
        filename = os.path.basename(d.get("filename", ""))
        downloaded = d.get("_downloaded_bytes_str", "?")
        total = d.get("_total_bytes_str") or d.get("_total_bytes_estimate_str", "?")
        speed = d.get("_speed_str", "?")
        print(f"\r  {filename}: {downloaded} / {total}  @ {speed}   ", end="", flush=True)
    elif d["status"] == "finished":
        print()  # newline after the progress line


def download_mp3_with_ytdlp(
    url: str,
    output_dir: str = ".",
    quality: str = "192",
) -> None:
    """Download the audio track of a YouTube video and save it as an MP3.

    Args:
        url: Full YouTube video URL.
        output_dir: Directory where the MP3 file will be saved. Defaults to the
            current working directory.
        quality: Preferred MP3 bitrate (e.g. ``"192"``, ``"320"``). Defaults to
            ``"192"``.

    Raises:
        ValueError: If *url* is empty or does not look like a YouTube URL.
        yt_dlp.utils.DownloadError: Re-raised after printing a friendly message.
    """
    _validate_url(url)

    os.makedirs(output_dir, exist_ok=True)
    outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": quality,
            }
        ],
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0 Safari/537.36"
            ),
            "Referer": "https://www.youtube.com/",
        },
        # Uncomment to support age-restricted videos:
        # "cookiefile": "cookies.txt",
        "quiet": True,
        "progress_hooks": [_progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Download complete. File saved to: {os.path.abspath(output_dir)}")
    except yt_dlp.utils.DownloadError as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        raise
    except Exception as exc:  # noqa: BLE001
        print(f"An unexpected error occurred: {exc}", file=sys.stderr)
        raise


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download YouTube audio as an MP3 file."
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-o", "--output-dir",
        default=".",
        metavar="DIR",
        help="Directory to save the MP3 (default: current directory)",
    )
    parser.add_argument(
        "-q", "--quality",
        default="192",
        metavar="KBPS",
        help="MP3 bitrate in kbps (default: 192)",
    )
    return parser


if __name__ == "__main__":
    args = _build_arg_parser().parse_args()
    try:
        download_mp3_with_ytdlp(args.url, output_dir=args.output_dir, quality=args.quality)
    except (ValueError, yt_dlp.utils.DownloadError):
        sys.exit(1)
    except Exception:
        sys.exit(2)