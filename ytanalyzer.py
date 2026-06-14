import os
import sys
import subprocess
import re
import argparse
import time
from yt_dlp import YoutubeDL

def clean_filename(title):
    """Removes characters that aren't allowed in file names."""
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c in ' -_']).strip()

def format_timestamp(total_seconds):
    """Formats seconds into YouTube-clickable MM:SS or HH:MM:SS"""
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def main():
    # COMMAND-LINE ARGUMENTS FOR TUNING
    parser = argparse.ArgumentParser(description="Analyze YouTube videos for track timestamps.")
    parser.add_argument("url", help="The YouTube video URL")
    parser.add_argument("--noise", type=int, default=-22, help="Volume threshold in dB (e.g., -22). Closer to 0 is louder.")
    parser.add_argument("--duration", type=float, default=1.5, help="Minimum duration of silence in seconds (e.g., 1.5)")
    parser.add_argument("--min-mins", type=float, default=0.0, help="Minimum song length in MINUTES (e.g., 2.5). Discards shorter transitions.")
    parser.add_argument("--min-len", type=int, default=45, help="Minimum track length in SECONDS to avoid duplicate triggers")
    parser.add_argument("--intro", type=int, default=15, help="Seconds to ignore at the start of the video")
    parser.add_argument("--cleanup", action="store_true", help="Delete the audio file automatically after a successful run")
    
    args = parser.parse_args()

    # Determine the actual cooldown in seconds (use whichever is larger: min-len or min-mins converted to seconds)
    min_song_seconds = max(args.min_len, int(args.min_mins * 60))

    # Configure yt-dlp to download native audio format using Video ID (stable name)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'cache_%(id)s.%(ext)s',
        'quiet': True,
        'warnings': 'no_warnings'
    }

    audio_file = None
    try:
        print("🔍 Fetching video details...")
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(args.url, download=False)
            raw_title = info.get('title', 'timestamps')
            
            # AUTO-FETCH TITLE FOR OUTPUT FILE
            safe_title = clean_filename(raw_title)
            output_txt_filename = f"{safe_title}_timestamps.txt"
            
            # Determine what the download filename will be
            audio_file = ydl.prepare_filename(info)

        # Only download if this specific video cache file doesn't exist
        if not os.path.exists(audio_file):
            print(f"📥 Downloading native audio track for: {raw_title}")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([args.url])
        else:
            print(f"🔄 Found local audio cache for '{raw_title}', skipping download...")

        print(f"🎧 Analyzing audio (Noise: {args.noise}dB, Min Gap: {args.duration}s, Min Song Time: {min_song_seconds}s)...")
        
        # FFmpeg filter using our command line arguments
        filter_str = f"silencedetect=noise={args.noise}dB:d={args.duration}"
        command = ['ffmpeg', '-y', '-i', audio_file, '-af', filter_str, '-f', 'null', '-']
        
        result = subprocess.run(command, stderr=subprocess.PIPE, text=True)
        output = result.stderr

        # Process results
        results_lines = []
        
        # We don't put the title directly above the timestamps anymore to ensure 
        # YouTube doesn't get confused when reading the description.
        print(f"\n🎵 DETECTED LIVE TRACK TIMESTAMPS FOR:\n# {raw_title}\n" + "="*40)
        
        results_lines.append("00:00 - Track 1")
        
        matches = re.findall(r'silence_end:\s+([\d\.]+)', output)
        track_num = 2
        last_time = 0
        
        for match in matches:
            total_seconds = int(float(match))
            
            # Filter matches using our new calculated track cooldown limit
            if total_seconds > args.intro and (total_seconds - last_time) > min_song_seconds:
                # Use our new YouTube formatting logic
                yt_time = format_timestamp(total_seconds)
                results_lines.append(f"{yt_time} - Track {track_num}")
                
                track_num += 1
                last_time = total_seconds

        # Print to console
        final_output = "\n".join(results_lines)
        print(final_output + "\n")

        # EXPORT TO A TEXT FILE
        with open(output_txt_filename, "w", encoding="utf-8") as f:
            f.write(final_output)
        print(f"💾 Timestamps saved to: {output_txt_filename}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)
        
    # CLEAN UP FUNCTION WITH WINDOWS FIX
    finally:
        if args.cleanup and audio_file and os.path.exists(audio_file):
            print(f"🧹 Cleaning up temporary audio file: {audio_file}")
            try:
                # Give Windows 2 seconds to release the file lock
                time.sleep(2) 
                os.remove(audio_file)
                print("✨ Cleanup complete!")
            except Exception as e:
                print(f"\n⚠️ Could not auto-delete the file. Windows might still be holding it.")
                print(f"Error details: {e}")
                print(f"You can safely delete '{audio_file}' manually.")

if __name__ == "__main__":
    main()