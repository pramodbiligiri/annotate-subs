import subprocess
import sys

# Main function
def main(input_image, input_audio, input_srt, start_time, end_time, output_file):
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
    if len(sys.argv) < 7:
        print("Usage: python generate-short-video.py --input-image <input_image> --input-audio <input_audio> --input-srt <input_srt> --start-time <start_time> --end-time <end_time> --output-file <output_file>")
        sys.exit(1)
    input_image = None
    input_audio = None
    input_srt = None
    start_time = None
    end_time = None
    output_file = None
    for arg in sys.argv[1:]:
        if arg.startswith('--input-image='):
            input_image = arg.split('=')[1]
        elif arg.startswith('--input-audio='):
            input_audio = arg.split('=')[1]
        elif arg.startswith('--input-srt='):
            input_srt = arg.split('=')[1]
        elif arg.startswith('--start-time='):
            start_time = arg.split('=')[1]
        elif arg.startswith('--end-time='):
            end_time = arg.split('=')[1]
        elif arg.startswith('--output-file='):
            output_file = arg.split('=')[1]
    if not input_image:
        print("Error: --input-image parameter is required.")
    if not input_audio:
        print("Error: --input-audio parameter is required.")
    if not input_srt:
        print("Error: --input-srt parameter is required.")
    if not start_time:
        print("Error: --start-time parameter is required.")
    if not end_time:
        print("Error: --end-time parameter is required.")
    if not output_file:
        print("Error: --output-file parameter is required.")
    if not input_image or not input_audio or not input_srt or not start_time or not end_time or not output_file:
        sys.exit(1)
    main(input_image, input_audio, input_srt, start_time, end_time, output_file)