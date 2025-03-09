import subprocess
import sys

# Main function
def main(input_audio, output_file):
    command = [
        "ffmpeg",
        "-nostdin",
        "-threads", "0",
        "-i", input_audio,
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        "-f", "wav",
        output_file
    ]
    print(f"Running command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
        print("Audio conversion completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: ffmpeg subprocess failed with error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python generate-whisper-compat-audio.py --input-audio <input_audio> --output-file <output_file>")
        sys.exit(1)
    input_audio = None
    output_file = None
    for arg in sys.argv[1:]:
        if arg.startswith('--input-audio='):
            input_audio = arg.split('=')[1]
        elif arg.startswith('--output-file='):
            output_file = arg.split('=')[1]
    if not input_audio:
        print("Error: --input-audio parameter is required.")
    if not output_file:
        print("Error: --output-file parameter is required.")
    if not input_audio or not output_file:
        sys.exit(1)
    main(input_audio, output_file)