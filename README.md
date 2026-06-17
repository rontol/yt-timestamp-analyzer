Markdown

# 🎵 YouTube Timestamp Analyzer

A Python script that automatically generates clickable YouTube timestamps for music mixes, DJ sets, and albums. It downloads the audio directly via `yt-dlp` and uses `ffmpeg` silence detection to find track transitions, saving the results directly to a text file.

## ✨ Features
* **Smart Audio Analysis:** Uses FFmpeg's `silencedetect` filter to accurately pinpoint track transitions.
* **YouTube-Ready Formatting:** Automatically converts timestamps into clickable `MM:SS` or `HH:MM:SS` formats.
* **Auto-Export:** Saves the final timestamps to a clean `.txt` file named after the YouTube video.
* **Smart Caching:** Keeps the downloaded native audio locally so you can quickly re-run the analyzer with different tuning parameters without re-downloading.
* **Windows-Safe Cleanup:** Includes a delayed file-lock release to safely auto-delete temporary files on Windows systems.

---

## 📋 Prerequisites

To run this script, you need the following installed on your system:

1. **Python 3.x**
2. **yt-dlp:** Install via Python package manager:
   ```bash
   pip install yt-dlp

```

3. **FFmpeg:** Must be installed and added to your system's PATH variable so Python can call it.
* *Mac:* `brew install ffmpeg`
* *Windows:* Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or use `winget install ffmpeg`
* *Linux:* `sudo apt install ffmpeg`



---

## 🚀 Basic Usage

Open your terminal or command prompt and run the script with a YouTube URL:

```bash
python analyzer.py "[https://www.youtube.com/watch?v=YOUR_LINK_HERE](https://www.youtube.com/watch?v=YOUR_LINK_HERE)"

```

The script will download the audio, run the analysis, print the timestamps to your console, and save them to a file like `Video_Title_timestamps.txt`.

---

## ⚙️ Advanced Tuning

You can tweak the analysis by adding optional arguments to fit different types of audio (like live shows vs. clean studio albums).

| Argument | Default | Description |
| --- | --- | --- |
| `--noise` | `-22` | Volume threshold in dB. Closer to 0 is louder. Determines what the script considers "silence". |
| `--duration` | `1.5` | Minimum duration of silence in seconds to trigger a track split. |
| `--min-mins` | `0.0` | Minimum song length in MINUTES. Discards shorter transitions. |
| `--min-len` | `45` | Minimum track length in SECONDS to avoid duplicate triggers. |
| `--intro` | `15` | Seconds to ignore at the start of the video. |
| `--cleanup` | `False` | Add this flag to automatically delete the downloaded audio file after generating timestamps. |

**Example of a fully tuned command:**

```bash
python analyzer.py "[https://www.youtube.com/watch?v=YOUR_LINK_HERE](https://www.youtube.com/watch?v=YOUR_LINK_HERE)" --noise -20 --duration 2.0 --cleanup

```

---

## 🎛️ Recommended Settings (Cookbook)

Different types of videos require slightly different detection logic. Here are some good starting points:

### 1. Clean Studio Albums

Studio albums usually have absolute silence between tracks and no crowd noise.

```bash
python analyzer.py "URL" --noise -25 --duration 1.5 --min-mins 2.0

```

* **Why?** Dropping the noise threshold to `-25` tells the script to look for *true* silence, which prevents it from accidentally marking a quiet acoustic breakdown mid-song as a new track. Assuming most songs are at least 2 minutes long (`--min-mins 2.0`) prevents false positives.

### 2. Live DJ Sets / Mixes

Transitions in DJ sets rarely reach true silence, and the gaps are very fast.

```bash
python analyzer.py "URL" --noise -15 --duration 0.5 --min-mins 3.0

```

* **Why?** Raising the noise threshold to `-15` catches the slight dips in volume during a crossfade. Dropping the duration to `0.5` catches very fast mixing.

### 3. Concept Albums (Hidden Tracks / Long Intros)

```bash
python analyzer.py "URL" --intro 60 --min-len 90

```

* **Why?** Uses `--intro 60` to completely skip analyzing a cinematic intro or skit at the start of the video, and `--min-len 90` ensures that brief interludes aren't flagged as full songs.

```

By the way, to unlock the full functionality of all Apps, enable [Gemini Apps Activity](https://myactivity.google.com/product/gemini).

```
