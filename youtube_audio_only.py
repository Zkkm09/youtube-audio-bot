"""
YouTube Audio Only Downloader
Downloads only the audio stream from YouTube videos
"""

import os
from pytubefix import YouTube
from pytubefix.cli import on_progress


def download_audio_only(url, output_dir="downloads"):
    """
    Download only audio from YouTube video
    
    Args:
        url: YouTube video URL
        output_dir: Directory to save downloaded files
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"Fetching video information for: {url}")
        
        # Initialize YouTube object with ANDROID client
        yt = YouTube(url, client='ANDROID', on_progress_callback=on_progress)
        
        print(f"\nTitle: {yt.title}")
        print(f"Author: {yt.author}")
        print(f"Duration: {yt.length} seconds")
        
        # Get the 128kbps audio stream (itag=140)
        print("\n" + "="*50)
        print("Available audio streams:")
        print("="*50)
        
        audio_streams = yt.streams.filter(only_audio=True)
        for i, stream in enumerate(audio_streams):
            print(f"{i}. {stream}")
        
        # Get itag 140 specifically (128kbps mp4 audio)
        audio_stream = yt.streams.get_by_itag(140)
        
        if not audio_stream:
            print("\n⚠ itag=140 not found, getting best audio quality...")
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        print("\n" + "="*50)
        print("Downloading audio stream...")
        print("="*50)
        print(f"Selected: {audio_stream}")
        
        # Download audio
        audio_filename = audio_stream.download(output_path=output_dir)
        print(f"\n✓ Audio downloaded successfully!")
        print(f"✓ Location: {audio_filename}")
        
        return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Main function"""
    
    print("="*60)
    print("YouTube Audio Only Downloader")
    print("="*60)
    print()
    
    # Get URL from user
    test_url = input("Enter YouTube URL: ").strip()
    
    if not test_url:
        print("No URL provided!")
        return
    
    # Download audio
    success = download_audio_only(test_url)
    
    if success:
        print("\n" + "="*60)
        print("✓ DOWNLOAD COMPLETED SUCCESSFULLY!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("✗ DOWNLOAD FAILED")
        print("="*60)


if __name__ == "__main__":
    main()
