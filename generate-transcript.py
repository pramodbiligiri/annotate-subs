import sys
import os
import json
import subprocess

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
    if len(sys.argv) < 2:
        print("Usage: python generate_transcript.py --input-audio-file <input_audio_file> [--output-transcript-file <output_transcript_file>] [--whisper-cpp-home <whisper_cpp_home>] [--duration-sec <duration_sec>]")
        sys.exit(1)
    input_audio_file = None
    output_transcript_file = None
    whisper_cpp_home = None
    duration_sec = None
    for arg in sys.argv[1:]:
        if arg.startswith('--input-audio-file='):
            input_audio_file = arg.split('=')[1]
        elif arg.startswith('--output-transcript-file='):
            output_transcript_file = arg.split('=')[1]
        elif arg.startswith('--whisper-cpp-home='):
            whisper_cpp_home = arg.split('=')[1]
        elif arg.startswith('--duration-sec='):
            duration_sec = arg.split('=')[1]
    if not input_audio_file:
        print("Error: --input-audio-file is required.")
        sys.exit(1)
    main(input_audio_file, output_transcript_file, whisper_cpp_home, duration_sec)

# Renamed file to generate-transcript.py
