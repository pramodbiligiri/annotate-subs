import subprocess
import sys
import argparse

# Main function
def main(input_image, input_audio, input_srt, start_time, end_time, output_file):
    # Replace comma with dot in start_time and end_time
    start_time = start_time.replace(',', '.')
    end_time = end_time.replace(',', '.')
    command = [
        "ffmpeg",
        "-r", "1",
        "-loop", "1",
        "-i", input_image,
        "-i", input_audio,
        "-c:a", "aac",
        "-r", "10",
        "-shortest",
        "-pix_fmt", "yuv420p",
        "-b:v", "5M",
        "-preset", "slow",
        "-ss", start_time,
        "-to", end_time,
        "-vf", f"subtitles={input_srt}:force_style='Fontname=Open Sans Semibold,Fontsize=16,Bold=1',setdar=9/16",
        "-movflags", "+faststart",
        output_file
    ]
    print(f"Running command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
        print("Video generation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: ffmpeg subprocess failed with error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a short video from an image, audio, and subtitle file.')
    parser.add_argument('--input-image', required=True, help='Path to the input image file')
    parser.add_argument('--input-audio', required=True, help='Path to the input audio file')
    parser.add_argument('--input-srt', required=True, help='Path to the input subtitle file')
    parser.add_argument('--start-time', required=True, help='Start time for the video segment')
    parser.add_argument('--end-time', required=True, help='End time for the video segment')
    parser.add_argument('--output-file', required=True, help='Path to the output video file')
    args = parser.parse_args()

    main(args.input_image, args.input_audio, args.input_srt, args.start_time, args.end_time, args.output_file)