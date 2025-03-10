import sys
import os
import json
import subprocess
import argparse

# Main function

def main(input_audio_file, output_transcript_file=None, whisper_cpp_home=None, duration_sec=None):
    if not whisper_cpp_home:
        whisper_cpp_home = os.getenv('WHISPER_CPP_HOME')
        if whisper_cpp_home:
            print(f"Using WHISPER_CPP_HOME env var: {whisper_cpp_home}")
        else:
            print("Error: --whisper-cpp-home argument or WHISPER_CPP_HOME env var is required.")
            sys.exit(1)

    # Convert duration from seconds to milliseconds
    duration_ms = int(duration_sec) * 1000 if duration_sec else None

    # Generate transcript using whisper-cli
    srt_file = output_transcript_file if output_transcript_file else os.path.splitext(input_audio_file)[0] + '.srt'
    srt_file_for_whisper = srt_file[:-4] if srt_file.endswith('.srt') else srt_file

    # Check if the SRT file already exists
    if os.path.exists(srt_file):
        overwrite = input(f"SRT file '{srt_file}' already exists. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != 'y':
            print("Exiting without overwriting the SRT file.")
            sys.exit(0)

    print(f"Using whisper-cli at: {os.path.join(whisper_cpp_home, 'build/bin/whisper-cli')}")
    print("Launching whisper-cli subprocess...")
    try:
        command = [
            "cpulimit", "-l", "200", "--",
            os.path.join(whisper_cpp_home, "build/bin/whisper-cli"),
            "-m", os.path.join(whisper_cpp_home, "models/ggml-base.en.bin"),
            "-osrt",
            f"-of", srt_file_for_whisper,
            "-oved", "GPU",
            "-f", input_audio_file,
            "-ml", "96"
        ]
        if duration_ms:
            command.extend(["--duration", str(duration_ms)])
        print(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("whisper-cli subprocess done.")
    except subprocess.CalledProcessError as e:
        print(f"Error: whisper-cli subprocess failed with error: {e}")
        sys.exit(1)

    if not os.path.exists(srt_file):
        print(f"Error: SRT file '{srt_file}' not found.")
        sys.exit(1)

    # Output the result
    if output_transcript_file:
        with open(output_transcript_file, 'r', encoding='utf-8') as file:
            print(file.read())
    else:
        with open(srt_file, 'r', encoding='utf-8') as file:
            print(file.read())

    # Save the transcript to a file
    transcript_file = os.path.splitext(input_audio_file)[0] + '_transcript.txt'
    with open(transcript_file, 'w') as file:
        file.write(result.stdout)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate transcripts from audio files using whisper-cli.')
    parser.add_argument('--input-audio-file', required=True, help='Path to the input audio file')
    parser.add_argument('--output-transcript-file', help='Path to the output transcript file')
    parser.add_argument('--whisper-cpp-home', help='Path to the Whisper CPP home directory')
    parser.add_argument('--duration-sec', type=int, help='Duration in seconds for processing')
    args = parser.parse_args()

    main(args.input_audio_file, args.output_transcript_file, args.whisper_cpp_home, args.duration_sec)
