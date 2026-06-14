# YouTube Timestamp Analyzer 🎵

A Python script that automatically generates clickable YouTube timestamps for music mixes, DJ sets, and albums. It downloads the audio directly via `yt-dlp` and uses `ffmpeg` silence detection to find track transitions.

## Prerequisites
To run this script, you need to have the following installed on your system:
* **Python 3.x**
* **yt-dlp:** `pip install yt-dlp`
* **FFmpeg:** Must be installed and added to your system's PATH.

## How to Use
Open your terminal or command prompt and run the script with a YouTube URL:

```bash
python analyzer.py "[https://www.youtube.com/watch?v=YOUR_LINK_HERE](https://www.youtube.com/watch?v=YOUR_LINK_HERE)"




## Advanced Tuning
You can tweak the analysis by adding optional arguments. For example:

python analyzer.py "URL" --noise -20 --duration 2.0 --cleanup


--noise: Volume threshold in dB (Default: -22). Closer to 0 is louder.

--duration: Minimum duration of silence in seconds to trigger a split (Default: 1.5).

--min-mins: Minimum song length in minutes. Discards shorter transitions (Default: 0.0).

--min-len: Minimum track length in seconds to avoid duplicate triggers (Default: 45).

--intro: Seconds to ignore at the start of the video (Default: 15).

--cleanup: Automatically deletes the downloaded audio file after generating timestamps.



--noise -25: Studio albums don't have crowd noise or amp feedback. Dropping this to -25 tells the script to look for true silence, which prevents it from accidentally marking a quiet acoustic breakdown mid-song as a new track.

--duration 1.5: A standard 1.5-second gap is perfect for studio albums.

--min-mins 2.0: Assuming most songs on this album are at least 2 minutes long, this will filter out any weird pauses or skits.