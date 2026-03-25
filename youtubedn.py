import yt_dlp

def download_mp3_with_ytdlp(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # Add browser-like headers if server rejects plain requests
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36',
            'Referer': 'https://www.youtube.com/'
        },
        # If you need cookies (age-restricted), write path to browser-exported cookies file
        # 'cookiefile': 'cookies.txt',
        'quiet': False,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    url = input("YouTube URL: ").strip()
    download_mp3_with_ytdlp(url)