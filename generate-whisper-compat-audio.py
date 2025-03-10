import subprocess
import sys
import argparse

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
    parser = argparse.ArgumentParser(description='Convert the audio of a podcast into a Whisper CPP compatible WAV file.')
    parser.add_argument('--input-audio', required=True, help='Path to the input audio file')
    parser.add_argument('--output-file', required=True, help='Path to the output WAV file')
    args = parser.parse_args()

    main(args.input_audio, args.output_file)