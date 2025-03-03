# SRT Subtitle Analyzer

A toolkit for working with SRT subtitle files, featuring text extraction, paragraph formatting, and timestamp lookup.

![SRT Subtitle Analyzer Interface](srt-app-4.png)

## Features

- **Clean Text Extraction**: Extract readable text from SRT files, removing timestamps and formatting
- **Smart Paragraph Formation**: Automatically organize text into logical paragraphs based on content
- **Timestamp Lookup**: Find the exact timestamp where a specific quote appears in the video
- **Interactive Web Interface**: User-friendly Streamlit app for processing SRT files
- **Standalone CLI Tools**: Use the Python scripts directly from the command line

## Installation

### Prerequisites

- Python 3.8 or higher

### Option 1: Using a virtual environment (recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/annotate-subs.git
cd annotate-subs

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Linux/Mac
# or
# venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Global installation

```bash
# Clone the repository
git clone https://github.com/yourusername/annotate-subs.git
cd annotate-subs

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Web Application

The easiest way to use the SRT Subtitle Analyzer is through the Streamlit web interface:

```bash
streamlit run srt_analyzer_app.py
```

This will open a web interface in your browser where you can:
1. Paste your SRT file content
2. Process it to extract clean text
3. Search for specific snippets to find their timestamps

### Command Line Tools

#### Extract Clean Text

```bash
python extract_srt_text.py input.srt [output.txt]
```

This will extract the text content from `input.srt` and save it to `output.txt` (or `input.txt` if not specified), with proper paragraph formatting.

#### Find Timestamp for Text

```bash
python find_timestamp.py input.srt "text to find"
```

This will search for the quoted text in the SRT file and display the corresponding timestamp.

You can also use the interactive mode:

```bash
python find_timestamp.py input.srt input.txt
```

This will prompt you to enter text snippets to look up.

## How It Works

### Text Extraction and Formatting

The SRT text extraction:
1. Parses the SRT file structure
2. Extracts only the actual subtitle text content
3. Removes sound effect indicators (like `[MUSIC]` or `[LAUGHS]`)
4. Groups text into logical segments based on punctuation and speaker changes
5. Forms paragraphs at natural topic boundaries or after approximately 12 segments

### Timestamp Lookup

The timestamp finder:
1. Takes a text snippet as input
2. Searches through all subtitles for exact or close matches
3. Uses fuzzy matching for approximate matches
4. Returns the subtitle number, timestamp, and full text of the match

## Project Structure

- `srt_analyzer_app.py` - Streamlit web application
- `extract_srt_text.py` - CLI tool to extract formatted text from SRT files
- `find_timestamp.py` - CLI tool to find timestamps for text snippets
- `requirements.txt` - Python dependencies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web application framework
- Created with assistance from [Claude AI](https://claude.ai/)