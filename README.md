## NexDataFetch
"NexDataFetch is a lightning-fast Python script for effortlessly downloading your favorite YouTube videos, designed with a sleek cyber-tech interface."


### Features
- High-Quality Downloads: Fetches and downloads the highest quality video and audio streams from provided URLs.
- Format Flexibility: Supports multiple video and audio formats for download.
- Progress Tracking: Displays download progress percentage for a user-friendly experience.
- Error Handling: Incorporates exception handling and logging for graceful error management.


### Requirements
Python 3.11.6


Required Python libraries: 'requests', 'beautifulsoup4', 'pandas'


### Installation
Clone the Repository:

```bash
git clone https://github.com/CipherXenon/NexDataFetch.git
cd NexDataFetch
```

### Install Dependencies:

```bash
pip install -r requirements.txt
```

### Usage

## Download Single Video
```bash
python fetcher.py --video_url <VIDEO_URL> --video_format <VIDEO_FORMAT> --audio_format <AUDIO_FORMAT> --output_dir <OUTPUT_DIRECTORY>
```

## Download Multiple Videos
```bash
python fetcher.py --video_url <VIDEO_URL1> <VIDEO_URL2> ... --video_format <VIDEO_FORMAT> --audio_format <AUDIO_FORMAT> --output_dir <OUTPUT_DIRECTORY>
```

- --video_url: URL(s) of the video(s) to be downloaded.
- --video_format: Desired video format (e.g., mp4, mkv).
- --audio_format: Desired audio format (e.g., mp3, m4a).
- --output_dir: Output directory for downloaded files (default: current directory).


### Example

## Download a single video:

``` bash
python fetcher.py --video_url https://example.com/video --video_format mp4 --audio_format mp3 --output_dir ./downloads
```

## Download multiple videos:

``` bash
python fetcher.py --video_url https://example.com/video1 https://example.com/video2 --video_format mkv --audio_format m4a --output_dir ./downloads
```

## License
This project is licensed under the GNU GPL V3 License - see the LICENSE file for details.
