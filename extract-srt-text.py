#!/usr/bin/env python3
"""
Extract plain text from SRT subtitle files.

This script reads an SRT subtitle file and extracts only the actual content text, 
removing timestamps, subtitle numbers, and other formatting elements.
The text is organized into sensible paragraphs.
"""

# Renamed file to extract-srt-text.py

import re
import sys
import os


def extract_text_from_srt(srt_file_path):
    """
    Extract text content from SRT file and organize into paragraphs.
    
    Args:
        srt_file_path: Path to the SRT file
    
    Returns:
        A string containing just the subtitle text content, organized in paragraphs
    """
    if not os.path.exists(srt_file_path):
        print(f"Error: File not found - {srt_file_path}")
        return None

    # Read the content of the SRT file
    with open(srt_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to identify subtitle blocks (number, timestamp, text)
    pattern = r'\d+\s*\n\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}\s*\n(.*?)(?=\n\s*\n\d+\s*\n|\Z)'
    
    # Find all text content, using non-greedy match and DOTALL to match across lines
    matches = re.findall(pattern, content, re.DOTALL)
    
    # Process each subtitle line
    lines = [match.strip().replace('\n', ' ') for match in matches]
    
    # Group subtitle lines into sensible segments first
    segments = []
    current_segment = []
    speaker_pattern = re.compile(r'^- ')
    
    for line in lines:
        # Skip music and sound effect indicators
        if any(indicator in line for indicator in ['[MUSIC', '[LAUGHS]', '[MUSIC]', '[MUSIC PLAYING]']):
            continue
        
        # Check if this line starts with a new speaker (indicated by "- ")
        new_speaker = speaker_pattern.match(line)
        
        # Start a new segment if:
        # 1. The current line indicates a new speaker
        # 2. The previous line ended with sentence-ending punctuation
        # 3. There's a significant pause (we'd need timestamps for this, using length as proxy)
        if (new_speaker or 
            (current_segment and current_segment[-1].rstrip().endswith(('.', '?', '!'))) or
            len(line) > 50) and current_segment:
            segments.append(' '.join(current_segment))
            current_segment = [line]
        # Otherwise, continue the current segment
        else:
            current_segment.append(line)
    
    # Add any remaining segment
    if current_segment:
        segments.append(' '.join(current_segment))
    
    # Now group segments into paragraphs (about 12 segments per paragraph)
    paragraphs = []
    current_paragraph = []
    paragraph_size = 0
    topic_change_words = ['welcome', 'so tell us', 'let\'s talk about', 'moving on', 'speaking of', 
                         'NASA', 'physics', 'data science', 'decision science', 'research', 'industry']
    
    for segment in segments:
        current_paragraph.append(segment)
        paragraph_size += 1
        
        # Start a new paragraph if:
        # 1. We've reached about 12 segments
        # 2. There appears to be a topic change (checking for specific words)
        if (paragraph_size >= 12 or 
            any(word.lower() in segment.lower() for word in topic_change_words)):
            paragraphs.append(' '.join(current_paragraph))
            current_paragraph = []
            paragraph_size = 0
    
    # Add any remaining text as a paragraph
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))
    
    # Join paragraphs with double newlines to create visible paragraph breaks
    return '\n\n'.join(paragraphs)


def main():
    """Process SRT file and save the extracted text."""
    if len(sys.argv) < 2:
        print("Usage: python extract_srt_text.py <srt_file> [output_file]")
        print("If output_file is not specified, it will use the same name with .txt extension")
        return

    srt_file = sys.argv[1]
    
    # Determine output file name
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        # Use the same name but with .txt extension
        base_name = os.path.splitext(srt_file)[0]
        output_file = f"{base_name}.txt"
    
    # Extract text and save to file
    extracted_text = extract_text_from_srt(srt_file)
    if extracted_text:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        print(f"Extracted text saved to {output_file}")


if __name__ == "__main__":
    main()