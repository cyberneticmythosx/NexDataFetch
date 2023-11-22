import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor
import subprocess
import os

# Color codes for cyberpunk-tech style
class TerminalColors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    END = '\033[0m'

# ASCII art banner in cyberpunk-tech style
BANNER = '''
{header}░█▀█░█▀▀░█░█░█▀▄░█▀█░▀█▀░█▀█░█▀▀░█▀▀░▀█▀░█▀▀░█░█{end}
{header}░█░█░█▀▀░▄▀▄░█░█░█▀█░░█░░█▀█░█▀▀░█▀▀░░█░░█░░░█▀█{end}
{header}░▀░▀░▀▀▀░▀░▀░▀▀░░▀░░▀░▀░▀░░░▀▀▀░░▀░░▀▀▀░▀░▀{end}
'''.format(header=TerminalColors.CYAN, end=TerminalColors.END)

# Functions and code from the provided script (excluding the ASCII art and colors)

# Incorporating the banner
def print_banner():
    print(BANNER)

# User-friendly UI messages
def print_success(message):
    print(f"{TerminalColors.GREEN}{message}{TerminalColors.END}")

def print_error(message):
    print(f"{TerminalColors.HEADER}{message}{TerminalColors.END}")

# Modify existing functions to use UI messages
# ...

logging.basicConfig(filename='app.log', level=logging.INFO)

def get_video_info(video_url):
    try:
        response = requests.get(video_url)
        soup = BeautifulSoup(response.content, "html.parser")
        video_src = soup.find("source")["src"]
        audio_src = soup.find("audio")["src"]

        video_df = pd.read_html(response.content, header=None)[0]
        video_df.columns = ["attribute", "value"]
        video_df = video_df.drop_duplicates(subset="value")
        video_df.reset_index(drop=True, inplace=True)

        audio_df = pd.read_html(response.content, header=None)[1]
        audio_df.columns = ["attribute", "value"]
        audio_df = audio_df.drop_duplicates(subset="value")
        audio_df.reset_index(drop=True, inplace=True)

        metadata = {
            "title": soup.find("title").text.strip(),  # Extract video title
            "video_formats": video_df["value"].tolist(),
            "audio_formats": audio_df["value"].tolist()
        }

        return video_src, audio_src, metadata

    except requests.RequestException as e:
        logging.error(f"Request Exception: {e}")
        raise
    except Exception as e:
        logging.error(f"Error occurred in getting video info: {e}")
        raise



def download_stream_with_progress(url, index, progress_callback):
    try:
        response = requests.get(url.split("&")[index], stream=True)
        total_size = int(response.headers.get('content-length', 0))

        downloaded = 0
        with open('temp_file.tmp', 'wb') as file:
            for data in response.iter_content(chunk_size=4096):
                file.write(data)
                downloaded += len(data)
                progress_callback(downloaded, total_size)

        return open('temp_file.tmp', 'rb').read()

    except requests.RequestException as e:
        logging.error(f"Request Exception: {e}")
        raise
    except Exception as e:
        logging.error(f"Error occurred in downloading stream: {e}")
        raise

def download_highest_quality(video_url, video_format, audio_format, output_dir="."):
    try:
        video_src, audio_src, metadata = get_video_info(video_url)
        video_formats = metadata["video_formats"]
        audio_formats = metadata["audio_formats"]

        if video_format not in video_formats or audio_format not in audio_formats:
            raise ValueError("Invalid video or audio format selected")

        def progress_callback(downloaded, total_size):
            if total_size > 0:
                percentage = (downloaded / total_size) * 100
                print(f"Downloading... {percentage:.2f}%")

        with ThreadPoolExecutor(max_workers=2) as executor:
            video_future = executor.submit(download_stream_with_progress, video_src, video_formats.index(video_format), progress_callback)
            audio_future = executor.submit(download_stream_with_progress, audio_src, audio_formats.index(audio_format), progress_callback)

            highest_resolution_video = video_future.result()
            highest_bitrate_audio = audio_future.result()

        video_filename = f"{metadata['title']}_{video_format}_video.{video_format}"
        audio_filename = f"{metadata['title']}_{audio_format}_audio.{audio_format}"

        video_filepath = os.path.join(output_dir, video_filename)
        audio_filepath = os.path.join(output_dir, audio_filename)

        write_to_file(highest_resolution_video, video_filepath)
        write_to_file(highest_bitrate_audio, audio_filepath)

        logging.info("Download and processing completed successfully!")

    except ValueError as ve:
        logging.error(f"Value Error: {ve}")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
    finally:
        if os.path.exists('temp_file.tmp'):
            os.remove('temp_file.tmp')

def download_batch_videos(video_urls, video_format, audio_format, output_dir="."):
    for url in video_urls:
        download_highest_quality(url, video_format, audio_format, output_dir)

def setup_cli():
    parser = argparse.ArgumentParser(description='Download and process highest quality video and audio streams.')
    parser.add_argument('--video_url', nargs='+', type=str, help='URLs of the videos')
    parser.add_argument('--video_format', type=str, help='Desired video format')
    parser.add_argument('--audio_format', type=str, help='Desired audio format')
    parser.add_argument('--output_dir', type=str, default=".", help='Output directory for downloaded files')
    return parser.parse_args()

def main():
    args = setup_cli()

    if args.video_url:
        download_batch_videos(args.video_url, args.video_format, args.audio_format, args.output_dir)
    else:
        download_highest_quality(args.video_url, args.video_format, args.audio_format, args.output_dir)

if __name__ == "__main__":
    main()
