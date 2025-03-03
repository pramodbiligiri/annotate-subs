#!/usr/bin/env python3
"""
Find the timestamp in an SRT file for a given snippet of text.

This script takes a text snippet and finds where it appears in the original SRT file,
returning the corresponding timestamp.
"""

import re
import sys
import os
import difflib


def parse_srt_file(srt_file_path):
    """
    Parse an SRT file into a list of subtitle entries.

    Args:
        srt_file_path: Path to the SRT file

    Returns:
        A list of tuples (subtitle_number, timestamp, text)
    """
    if not os.path.exists(srt_file_path):
        print(f"Error: SRT file not found - {srt_file_path}")
        return None

    # Read the content of the SRT file
    with open(srt_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split the content by double newline to get individual subtitle blocks
    subtitle_blocks = content.split('\n\n')
    
    subtitles = []
    for block in subtitle_blocks:
        if not block.strip():
            continue
        
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue
            
        subtitle_number = lines[0].strip()
        timestamp = lines[1].strip()
        text = ' '.join(lines[2:]).strip()
        
        subtitles.append((subtitle_number, timestamp, text))
    
    return subtitles


def find_timestamp_for_text(subtitles, text_snippet):
    """
    Find the timestamp for a given text snippet.

    Args:
        subtitles: List of subtitle entries
        text_snippet: The text snippet to search for

    Returns:
        The timestamp for the closest matching subtitle
    """
    # Clean up the text snippet (remove extra spaces, newlines)
    text_snippet = ' '.join(text_snippet.strip().split())
    
    # Convert all subtitle texts to a single string for searching
    all_text = ' '.join(subtitle[2] for subtitle in subtitles)
    
    # Look for exact match first
    if text_snippet in all_text:
        # Find which subtitle contains this text
        for subtitle_number, timestamp, text in subtitles:
            if text_snippet in text:
                start_time = timestamp.split(' --> ')[0]
                return subtitle_number, start_time, text
    
    # If no exact match, use difflib to find the closest match
    scores = []
    for subtitle_number, timestamp, text in subtitles:
        score = difflib.SequenceMatcher(None, text_snippet, text).ratio()
        scores.append((score, subtitle_number, timestamp, text))
    
    # Sort by score (highest first)
    scores.sort(reverse=True)
    
    # Get the best match
    if scores:
        best_score, subtitle_number, timestamp, text = scores[0]
        if best_score > 0.3:  # Threshold to consider a reasonable match
            start_time = timestamp.split(' --> ')[0]
            return subtitle_number, start_time, text
    
    return None, None, None


def main():
    """Find timestamps in an SRT file for given text snippets."""
    if len(sys.argv) < 3:
        print("Usage: python find_timestamp.py <srt_file> <text_file>")
        print("Or: python find_timestamp.py <srt_file> <text_snippet>")
        return

    srt_file = sys.argv[1]
    
    # Determine if we're using a text file or a direct snippet
    if os.path.exists(sys.argv[2]):
        # It's a file path
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            text_file_content = f.read()
            
        # Ask user for the snippet to search
        print("Enter the text snippet to search (Ctrl+D to exit):")
        try:
            while True:
                snippet = input("> ")
                if not snippet:
                    continue
                
                subtitles = parse_srt_file(srt_file)
                if not subtitles:
                    break
                    
                subtitle_number, timestamp, text = find_timestamp_for_text(subtitles, snippet)
                
                if timestamp:
                    print(f"\nFound in subtitle #{subtitle_number} at {timestamp}:")
                    print(f"Full subtitle text: \"{text}\"\n")
                else:
                    print("Snippet not found in the SRT file.")
        except EOFError:
            print("\nExiting.")
    else:
        # It's a direct text snippet
        snippet = ' '.join(sys.argv[2:])
        
        subtitles = parse_srt_file(srt_file)
        if not subtitles:
            return
            
        subtitle_number, timestamp, text = find_timestamp_for_text(subtitles, snippet)
        
        if timestamp:
            print(f"Found in subtitle #{subtitle_number} at {timestamp}:")
            print(f"Full subtitle text: \"{text}\"")
        else:
            print("Snippet not found in the SRT file.")


if __name__ == "__main__":
    main()