#!/usr/bin/env python3
"""
Streamlit webapp for SRT file analysis and timestamp finding.

This app combines the functionality of extract_srt_text.py and find_timestamp.py
into a user-friendly web interface.
"""

import streamlit as st
import re
import difflib
import tempfile
import os


def extract_text_from_srt_content(srt_content):
    """
    Extract formatted text content from SRT content.
    
    Args:
        srt_content: Content of the SRT file as string
    
    Returns:
        A string containing formatted subtitle text content with paragraphs
    """
    # Pattern to identify subtitle blocks (number, timestamp, text)
    pattern = r'\d+\s*\n\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}\s*\n(.*?)(?=\n\s*\n\d+\s*\n|\Z)'
    
    # Find all text content, using non-greedy match and DOTALL to match across lines
    matches = re.findall(pattern, srt_content, re.DOTALL)
    
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


def parse_srt_content(srt_content):
    """
    Parse SRT content into a list of subtitle entries.

    Args:
        srt_content: Content of the SRT file as string

    Returns:
        A list of tuples (subtitle_number, timestamp, text)
    """
    # Split the content by double newline to get individual subtitle blocks
    subtitle_blocks = srt_content.split('\n\n')
    
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
    
    if not text_snippet:
        return None, None, None
    
    # Convert all subtitle texts to a single string for searching
    all_text = ' '.join(subtitle[2] for subtitle in subtitles)
    
    # Look for exact match first
    matches = []
    for subtitle_number, timestamp, text in subtitles:
        if text_snippet.lower() in text.lower():
            start_time = timestamp.split(' --> ')[0]
            matches.append((subtitle_number, start_time, text, 1.0))
    
    if matches:
        return matches[0][:3]  # Return the first exact match
    
    # If no exact match, use difflib to find the closest match
    scores = []
    for subtitle_number, timestamp, text in subtitles:
        score = difflib.SequenceMatcher(None, text_snippet.lower(), text.lower()).ratio()
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
    """Main Streamlit app."""
    st.title("SRT Subtitle Analyzer")
    st.markdown("Extract clean text from subtitles and find timestamps for specific content.")
    
    # Search bar at the top with button next to it
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_query = st.text_area("Enter text to find timestamp:", height=100)
    
    with search_col2:
        find_button = st.button("Find Timestamp", use_container_width=True)
    
    # Timestamp search results (placed right below search area)
    if search_query and 'subtitles' in st.session_state and find_button:
        subtitle_number, timestamp, text = find_timestamp_for_text(
            st.session_state.subtitles, search_query
        )
        
        if timestamp:
            st.success(f"Found in subtitle #{subtitle_number} at {timestamp}")
            st.info(f"Full subtitle text: \"{text}\"")
        else:
            st.error("Snippet not found in the SRT file.")
    
    # Add a separator between search area and main content
    st.markdown("---")
    
    # Split the page into two columns for main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input SRT Content")
        srt_content = st.text_area(
            "Paste your SRT file content here:", 
            height=500
        )
        
        process_button = st.button("Process SRT Content")
    
    with col2:
        st.subheader("Formatted Text Output")
        if process_button and srt_content:
            # Process the SRT content
            formatted_text = extract_text_from_srt_content(srt_content)
            
            # Save as a session state to be accessible later
            st.session_state.formatted_text = formatted_text
            st.session_state.srt_content = srt_content
            st.session_state.subtitles = parse_srt_content(srt_content)
            
            # Display the formatted text
            st.text_area("Extracted formatted text:", formatted_text, height=500)
            
            # Offer download of the formatted text
            st.download_button(
                label="Download formatted text",
                data=formatted_text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
    
    # Add some instructions at the bottom
    st.markdown("---")
    st.markdown("""
    ### How to use this app:
    1. Paste your SRT file content in the left text area
    2. Click "Process SRT Content" to extract and format the text
    3. Copy a snippet of text you want to find and paste it in the search box at the top
    4. Click "Find Timestamp" to locate when this text appears in the video
    """)


if __name__ == "__main__":
    main()